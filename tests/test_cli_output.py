"""Test CLI output formatting and integration."""

from unittest.mock import patch
import runpy


def test_cli_output_formatting():
    """Test that CLI output is properly formatted."""
    with patch("builtins.input", side_effect=["exit"]):
        with patch("builtins.print") as mock_print:
            runpy.run_module("main", run_name="__main__")
            # Check that welcome message was printed
            mock_print.assert_called_with(
                "Welcome to the Terminal Calendar Assistant! Type 'exit' to quit."
            )


def test_cli_output_error_handling():
    """Test CLI output for error conditions."""
    with patch(
        "openai_client.interpret_command",
        return_value={"action": "error", "details": "Test error"},
    ):
        with patch("builtins.input", side_effect=["invalid command", "exit"]):
            with patch("builtins.print") as mock_print:
                runpy.run_module("main", run_name="__main__")
                # Verify that error handling doesn't crash
                mock_print.assert_called()


def test_cli_output_unknown_action():
    """Test CLI output for unknown actions."""
    with patch(
        "openai_client.interpret_command",
        return_value={"action": "unknown", "details": {}},
    ):
        with patch("builtins.input", side_effect=["unknown command", "exit"]):
            with patch("builtins.print") as mock_print:
                runpy.run_module("main", run_name="__main__")
                # Verify that unknown action handling doesn't crash
                mock_print.assert_called()


# Fallback map for testing
fallback_map = {
    "show my events": {"action": "list_all", "details": {}},
    "schedule meeting": {"action": "create_event", "details": {"title": "meeting"}},
    "delete meeting": {"action": "delete_event", "details": {"title": "meeting"}},
}


def run_cli(inputs):
    """Helper function to run CLI with given inputs and capture output."""
    printed = []

    def fake_print(*args, **kwargs):
        printed.append(" ".join(str(a) for a in args))

    def fake_input(prompt=""):
        return inputs.pop(0) if inputs else "exit"

    def fake_interpret_command(cmd, context=""):
        return fallback_map.get(cmd, {"action": "unknown", "details": {}})

    with patch("builtins.print", fake_print):
        with patch("builtins.input", fake_input):
            with patch("openai_client.interpret_command", fake_interpret_command):
                try:
                    runpy.run_module("main", run_name="__main__")
                except SystemExit:
                    pass
    return printed


def test_list_events_only_empty():
    """Test listing empty events."""
    outputs = run_cli(["show my events", "exit"])
    assert any("📅 Events:" in line for line in outputs)
    # Should show '(none)'
    assert any("(none)" in line for line in outputs)


def test_list_reminders_only_empty():
    """Test listing empty reminders."""
    outputs = run_cli(["show my reminders", "exit"])
    assert any("⏰ Reminders:" in line for line in outputs)
    assert any("(none)" in line for line in outputs)


def test_list_all_empty():
    """Test listing all empty."""
    outputs = run_cli(["what's on today?", "exit"])
    assert any("📅 Events:" in line for line in outputs)
    assert any("⏰ Reminders:" in line for line in outputs)


def test_invalid_date_error():
    """Test invalid date error handling."""
    outputs = run_cli(["list events from invalid to invalid", "exit"])
    assert any("❌ Error:" in line for line in outputs)
    # Should not list events or reminders
    assert not any("📅 Events:" in line for line in outputs)
    assert not any("⏰ Reminders:" in line for line in outputs)


def test_create_event_success():
    """Test successful event creation."""
    outputs = run_cli(["schedule meeting", "exit"])
    assert any("✅ Event created successfully" in line for line in outputs)


def test_delete_event_success():
    """Test successful event deletion."""
    outputs = run_cli(["delete meeting", "exit"])
    assert any("✅ Event deleted successfully" in line for line in outputs)


def test_move_event_success():
    """Test successful event moving."""
    outputs = run_cli(["move meeting", "exit"])
    assert any("✅ Event moved successfully" in line for line in outputs)


def test_add_notification_success():
    """Test successful notification addition."""
    outputs = run_cli(["add notification", "exit"])
    assert any("✅ Notification added successfully" in line for line in outputs)


def test_unknown_action():
    """Test unknown action handling."""
    outputs = run_cli(["unknown command", "exit"])
    assert any("[Not implemented yet]" in line for line in outputs)
