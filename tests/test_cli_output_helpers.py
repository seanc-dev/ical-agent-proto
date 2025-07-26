"""Unit tests for CLI output formatting helpers."""

from utils.cli_output import format_events, format_reminders, print_events_and_reminders


def test_format_events_empty():
    """Test formatting empty events list."""
    result = format_events([])
    assert "📅 Events:" in result
    assert "(none)" in result


def test_format_events_with_items():
    """Test formatting events list with items."""
    events = ["Meeting at 2pm", "Lunch at noon"]
    result = format_events(events)
    assert "📅 Events:" in result
    assert "Meeting at 2pm" in result
    assert "Lunch at noon" in result
    assert "  - Meeting at 2pm" in result
    assert "  - Lunch at noon" in result


def test_format_reminders_empty():
    """Test formatting empty reminders list."""
    result = format_reminders([])
    assert "⏰ Reminders:" in result
    assert "(none)" in result


def test_format_reminders_with_items():
    """Test formatting reminders list with items."""
    reminders = ["Buy groceries", "Call mom"]
    result = format_reminders(reminders)
    assert "⏰ Reminders:" in result
    assert "Buy groceries" in result
    assert "Call mom" in result
    assert "  - Buy groceries" in result
    assert "  - Call mom" in result


def test_print_events_and_reminders():
    """Test the combined print function."""
    events = ["Meeting"]
    reminders = ["Task"]
    # This test just ensures the function doesn't raise an error
    # In a real test, we'd mock print and verify the output
    print_events_and_reminders(events, reminders)
