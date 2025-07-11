import sys
from unittest.mock import patch
import pytest
from pathlib import Path

from dotask import cli  # Import your cli module


@pytest.mark.parametrize(
    "argv, expected_action, expected_file",
    [
        (["prog", "list"], "list_tasks", Path.home() / ".dotask" / "tasks.json"),
        (
            ["prog", "add", "My task"],
            "add_task",
            Path.home() / ".dotask" / "tasks.json",
        ),
        (
            ["prog", "update", "1", "done"],
            "update_task",
            Path.home() / ".dotask" / "tasks.json",
        ),
        (
            ["prog", "-f", "/tmp/tasks.json", "delete", "2"],
            "delete_task",
            Path("/tmp/tasks.json"),
        ),
    ],
)
def test_cli_invokes_main_with_correct_params(argv, expected_action, expected_file):
    with patch("dotask.cli.run_main") as mock_main:
        with patch.object(sys, "argv", argv):
            cli.main()

            assert mock_main.call_count == 1

            call_args = mock_main.call_args[0]
            action_callable = call_args[0]
            file_path = call_args[1]

            assert Path(file_path) == expected_file
            assert action_callable.func.__name__ == expected_action


def test_cli_handles_task_not_found_error(monkeypatch):
    from dotask.dotask import TaskNotFoundError

    def raise_not_found(*args, **kwargs):
        raise TaskNotFoundError(99)

    monkeypatch.setattr("dotask.cli.run_main", raise_not_found)

    with patch.object(sys, "argv", ["prog", "delete", "99"]):
        with pytest.raises(SystemExit) as exc_info:
            cli.main()
        assert exc_info.value.code == 1


def test_cli_handles_invalid_task_file_error(monkeypatch):
    from dotask.dotask import InvalidTaskFileError

    def raise_invalid_file(*args, **kwargs):
        raise InvalidTaskFileError("badfile.json")

    monkeypatch.setattr("dotask.cli.run_main", raise_invalid_file)

    with patch.object(sys, "argv", ["prog", "list"]):
        with pytest.raises(SystemExit) as exc_info:
            cli.main()
        assert exc_info.value.code == 1
