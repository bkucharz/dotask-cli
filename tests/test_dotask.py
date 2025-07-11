import json
from pathlib import Path
import tempfile
from unittest.mock import mock_open, patch
import pytest
from dotask.dotask import (
    InvalidTaskFileError, Task, TaskNotFoundError, add_task, TaskStatus, DATETIME_FORMAT, delete_task, list_tasks, load_file, update_task
)
from datetime import datetime


def test_add_task_adds_new_task():
    tasks = []
    description = "Write unit tests"

    add_task(tasks, description)

    assert len(tasks) == 1
    task = tasks[0]
    assert task.id == 1
    assert task.description == description
    assert task.status == TaskStatus.TODO.value

    # Validate datetime format
    datetime.strptime(task.createdAt, DATETIME_FORMAT)
    datetime.strptime(task.updatedAt, DATETIME_FORMAT)


def test_delete_task_removes_task():
    tasks = [Task(1, "Test task", "todo",
                  "2025-01-01 10:00:00", "2025-01-01 10:00:00")]
    delete_task(tasks, 1)
    assert len(tasks) == 0


def test_delete_task_raises_error_for_missing_task():
    tasks = []
    with pytest.raises(TaskNotFoundError) as exc_info:
        delete_task(tasks, 99)
    assert "No task found with ID 99" in str(exc_info.value)


def test_update_task_changes_status():
    task = Task(1, "Learn pytest", "todo",
                "2025-01-01 10:00:00", "2025-01-01 10:00:00")
    tasks = [task]

    update_task(tasks, 1, TaskStatus.DONE)
    assert task.status == TaskStatus.DONE.value
    assert task.updatedAt != "2025-01-01 10:00:00"  # updated timestamp


def test_update_task_raises_error_for_missing_task():
    tasks = []
    with pytest.raises(TaskNotFoundError):
        update_task(tasks, 42, TaskStatus.DONE)


def test_list_tasks_prints_all_tasks_sorted_by_createdAt(capsys):
    tasks = [
        Task(2, "Second", "todo", "2025-01-02 10:00:00", "2025-01-02 10:00:00"),
        Task(1, "First", "todo", "2025-01-01 10:00:00", "2025-01-01 10:00:00"),
    ]
    list_tasks(tasks, status="all", order_by="createdAt")

    captured = capsys.readouterr()
    assert "First" in captured.out
    assert "Second" in captured.out
    assert captured.out.find("First") < captured.out.find("Second")


def test_list_tasks_filters_by_status(capsys):
    tasks = [
        Task(1, "First", "done", "2025-01-01 10:00:00", "2025-01-01 10:00:00"),
        Task(2, "Second", "todo", "2025-01-02 10:00:00", "2025-01-02 10:00:00"),
    ]
    list_tasks(tasks, status="done", order_by="id")

    captured = capsys.readouterr()
    assert "First" in captured.out
    assert "Second" not in captured.out


def test_load_file_returns_empty_list_for_empty_file():
    mock_data = ''  # Simulate empty file
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("pathlib.Path.exists", return_value=True), \
                patch("pathlib.Path.stat") as mock_stat:
            mock_stat.return_value.st_size = 0  # file size = 0
            result = load_file("fake_tasks.json")
            assert result == []


def test_load_file_raises_error_on_bad_json():
    mock_data = 'not valid json'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("pathlib.Path.exists", return_value=True), \
                patch("pathlib.Path.stat") as mock_stat:
            mock_stat.return_value.st_size = 10  # non-zero size
            with pytest.raises(InvalidTaskFileError):
                load_file("fake_tasks.json")


def test_load_file_returns_tasks_from_valid_json():
    tasks_json = json.dumps([
        {
            "id": 1,
            "description": "Test Task",
            "status": "todo",
            "createdAt": "2024-07-10 10:00:00",
            "updatedAt": "2024-07-10 10:00:00"
        }
    ])
    with patch("builtins.open", mock_open(read_data=tasks_json)):
        with patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.stat") as mock_stat:
            mock_stat.return_value.st_size = 100
            result = load_file("fake_tasks.json")
            assert len(result) == 1
            assert isinstance(result[0], Task)
            assert result[0].description == "Test Task"
            
            
from dotask.dotask import save_file

def test_save_file_writes_json():
    tasks = [
        Task(1, "Task 1", "todo", "2024-07-10 10:00:00", "2024-07-10 10:00:00")
    ]
    m = mock_open()
    with patch("builtins.open", m):
        save_file("fake_tasks.json", tasks)
        m.assert_called_once_with(Path("fake_tasks.json"), "w+")
        handle = m()
        handle.write.assert_called()  # Check that something was written
        written_data = ''.join(call.args[0] for call in handle.write.call_args_list)
        assert '"description": "Task 1"' in written_data
        


def test_save_file_creates_missing_directories():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a path with non-existent parent directory
        test_file = Path(temp_dir) / "nonexistent_dir" / "tasks.json"
        
        # Ensure the directory doesn't exist
        assert not test_file.parent.exists()
        
        # Test saving
        tasks = [Task(1, "Test", "todo", "2024-01-01", "2024-01-01")]
        save_file(str(test_file), tasks)
        
        # Verify directory and file were created
        assert test_file.parent.exists()
        assert test_file.exists()

def test_load_file_handles_missing_file():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = Path(temp_dir) / "missing_tasks.json"
        assert not test_file.exists()
        
        result = load_file(str(test_file))
        assert result == []
