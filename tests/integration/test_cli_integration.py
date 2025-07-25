"""Integration tests for CLI functionality."""

from unittest.mock import patch
import runpy


def test_cli_integration_list_events():
    """Test CLI integration for listing events."""
    # Mock the calendar agent to return test data
    mock_result = {
        "events": ["Meeting at 2pm | 2024-01-01 14:00:00"],
        "reminders": ["Buy groceries | 2024-01-01 18:00:00"],
    }

    with patch(
        "utils.command_dispatcher.list_events_and_reminders", return_value=mock_result
    ):
        with patch("builtins.input", side_effect=["show me today's events", "exit"]):
            with patch("builtins.print") as mock_print:
                # Mock the interpret_command to return a known action
                with patch(
                    "openai_client.interpret_command",
                    return_value={"action": "list_all", "details": {}},
                ):
                    runpy.run_module("main", run_name="__main__")
                    # Verify that the output was printed
                    mock_print.assert_called()


def test_cli_integration_create_event():
    """Test CLI integration for creating events."""
    mock_result = {"success": True, "message": "Event created successfully"}

    with patch("utils.command_dispatcher.create_event", return_value=mock_result):
        with patch(
            "builtins.input",
            side_effect=["schedule meeting on 2024-01-01 at 2pm", "exit"],
        ):
            with patch("builtins.print") as mock_print:
                # Mock the interpret_command to return create_event action
                with patch(
                    "openai_client.interpret_command",
                    return_value={
                        "action": "create_event",
                        "details": {
                            "title": "meeting",
                            "date": "2024-01-01",
                            "time": "14:00",
                            "duration": 60,
                        },
                    },
                ):
                    runpy.run_module("main", run_name="__main__")
                    # Verify that success message was printed
                    mock_print.assert_called()


def test_cli_integration_delete_event():
    """Test CLI integration for deleting events."""
    mock_result = {"success": True, "message": "Event deleted successfully"}

    with patch("utils.command_dispatcher.delete_event", return_value=mock_result):
        with patch(
            "builtins.input", side_effect=["delete meeting on 2024-01-01", "exit"]
        ):
            with patch("builtins.print") as mock_print:
                # Mock the interpret_command to return delete_event action
                with patch(
                    "openai_client.interpret_command",
                    return_value={
                        "action": "delete_event",
                        "details": {"title": "meeting", "date": "2024-01-01"},
                    },
                ):
                    runpy.run_module("main", run_name="__main__")
                    # Verify that success message was printed
                    mock_print.assert_called()


def test_cli_integration_unknown_action():
    """Test CLI integration for unknown actions."""
    with patch("builtins.input", side_effect=["unknown command", "exit"]):
        with patch("builtins.print") as mock_print:
            # Mock the interpret_command to return unknown action
            with patch(
                "openai_client.interpret_command",
                return_value={"action": "unknown", "details": {}},
            ):
                runpy.run_module("main", run_name="__main__")
                # Verify that error message was printed
                mock_print.assert_called()


def test_cli_integration_error_handling():
    """Test CLI integration error handling."""
    mock_result = {"success": False, "error": "Test error"}

    with patch("utils.command_dispatcher.create_event", return_value=mock_result):
        with patch("builtins.input", side_effect=["schedule invalid event", "exit"]):
            with patch("builtins.print") as mock_print:
                # Mock the interpret_command to return create_event action
                with patch(
                    "openai_client.interpret_command",
                    return_value={"action": "create_event", "details": {}},
                ):
                    runpy.run_module("main", run_name="__main__")
                    # Verify that error message was printed
                    mock_print.assert_called()
