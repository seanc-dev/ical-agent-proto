"""Tests for CLI output formatting helpers."""

import pytest
from datetime import datetime
from utils.cli_output import (
    format_events,
    format_reminders,
    print_events_and_reminders,
    format_error_message,
    format_success_message,
    format_clarification_question,
)


class TestFormatEvents:
    """Test event formatting functionality."""

    def test_format_events_empty_list(self):
        """Test formatting empty events list."""
        result = format_events([])
        assert result == "📅 No events found"

    def test_format_events_single_event(self):
        """Test formatting a single event."""
        events = [
            {
                "title": "Team Meeting",
                "start_date": "2024-01-15T10:00:00",
                "end_date": "2024-01-15T11:00:00",
            }
        ]
        result = format_events(events)
        assert "📅 Team Meeting" in result
        assert "(10:00 AM)" in result

    def test_format_events_multiple_events(self):
        """Test formatting multiple events."""
        events = [
            {
                "title": "Team Meeting",
                "start_date": "2024-01-15T10:00:00",
                "end_date": "2024-01-15T11:00:00",
            },
            {
                "title": "Lunch",
                "start_date": "2024-01-15T12:00:00",
                "end_date": "2024-01-15T13:00:00",
            },
        ]
        result = format_events(events)
        assert "📅 Team Meeting" in result
        assert "📅 Lunch" in result
        assert "(10:00 AM)" in result
        assert "(12:00 PM)" in result

    def test_format_events_with_duration(self):
        """Test formatting events with duration display."""
        events = [
            {
                "title": "Short Meeting",
                "start_date": "2024-01-15T10:00:00",
                "end_date": "2024-01-15T10:30:00",
            }
        ]
        result = format_events(events)
        assert "(30min)" in result

    def test_format_events_no_duration_for_hour(self):
        """Test that 60-minute events don't show duration."""
        events = [
            {
                "title": "Hour Meeting",
                "start_date": "2024-01-15T10:00:00",
                "end_date": "2024-01-15T11:00:00",
            }
        ]
        result = format_events(events)
        assert "(60min)" not in result

    def test_format_events_invalid_date_handling(self):
        """Test handling of invalid date formats."""
        events = [
            {
                "title": "Meeting with Invalid Date",
                "start_date": "invalid-date",
                "end_date": "invalid-date",
            }
        ]
        result = format_events(events)
        assert "📅 Meeting with Invalid Date" in result
        # Should not crash and should show title without time

    def test_format_events_missing_fields(self):
        """Test handling of events with missing fields."""
        events = [
            {
                "title": "Meeting with Missing Fields",
                # Missing start_date and end_date
            }
        ]
        result = format_events(events)
        assert "📅 Meeting with Missing Fields" in result


class TestFormatReminders:
    """Test reminder formatting functionality."""

    def test_format_reminders_empty_list(self):
        """Test formatting empty reminders list."""
        result = format_reminders([])
        assert result == "✅ No reminders found"

    def test_format_reminders_single_reminder(self):
        """Test formatting a single reminder."""
        reminders = [
            {
                "title": "Review Budget",
                "due_date": "2024-01-15T00:00:00",
            }
        ]
        result = format_reminders(reminders)
        assert "✅ Review Budget" in result
        assert "(Due: Jan 15)" in result

    def test_format_reminders_multiple_reminders(self):
        """Test formatting multiple reminders."""
        reminders = [
            {
                "title": "Review Budget",
                "due_date": "2024-01-15T00:00:00",
            },
            {
                "title": "Submit Report",
                "due_date": "2024-01-16T00:00:00",
            },
        ]
        result = format_reminders(reminders)
        assert "✅ Review Budget" in result
        assert "✅ Submit Report" in result
        assert "(Due: Jan 15)" in result
        assert "(Due: Jan 16)" in result

    def test_format_reminders_invalid_date_handling(self):
        """Test handling of invalid date formats."""
        reminders = [
            {
                "title": "Reminder with Invalid Date",
                "due_date": "invalid-date",
            }
        ]
        result = format_reminders(reminders)
        assert "✅ Reminder with Invalid Date" in result
        # Should not crash and should show title without due date

    def test_format_reminders_missing_fields(self):
        """Test handling of reminders with missing fields."""
        reminders = [
            {
                "title": "Reminder with Missing Fields",
                # Missing due_date
            }
        ]
        result = format_reminders(reminders)
        assert "✅ Reminder with Missing Fields" in result


class TestFormatMessages:
    """Test message formatting functionality."""

    def test_format_error_message(self):
        """Test error message formatting."""
        result = format_error_message("Invalid date format")
        assert result == "❌ Error: Invalid date format"

    def test_format_error_message_with_suggestion(self):
        """Test error message formatting with suggestion."""
        result = format_error_message("Invalid date format", "Use YYYY-MM-DD")
        assert "❌ Error: Invalid date format" in result
        assert "💡 Suggestion: Use YYYY-MM-DD" in result

    def test_format_success_message(self):
        """Test success message formatting."""
        result = format_success_message("Event created successfully")
        assert result == "✅ Event created successfully"

    def test_format_clarification_question(self):
        """Test clarification question formatting."""
        result = format_clarification_question("Which Monday?")
        assert result == "🤔 Which Monday?"

    def test_format_clarification_question_with_context(self):
        """Test clarification question formatting with context."""
        result = format_clarification_question(
            "Which Monday?", "There are multiple Mondays this month"
        )
        assert "🤔 Which Monday?" in result
        assert "📝 Context: There are multiple Mondays this month" in result


class TestPrintEventsAndReminders:
    """Test the combined print function."""

    def test_print_events_and_reminders_with_both(self, capsys):
        """Test printing both events and reminders."""
        events = [
            {
                "title": "Team Meeting",
                "start_date": "2024-01-15T10:00:00",
                "end_date": "2024-01-15T11:00:00",
            }
        ]
        reminders = [
            {
                "title": "Review Budget",
                "due_date": "2024-01-15T00:00:00",
            }
        ]

        print_events_and_reminders(events, reminders)
        captured = capsys.readouterr()

        assert "📅 Today's Schedule:" in captured.out
        assert "📅 Team Meeting" in captured.out
        assert "✅ Today's Reminders:" in captured.out
        assert "✅ Review Budget" in captured.out

    def test_print_events_and_reminders_events_only(self, capsys):
        """Test printing only events."""
        events = [
            {
                "title": "Team Meeting",
                "start_date": "2024-01-15T10:00:00",
                "end_date": "2024-01-15T11:00:00",
            }
        ]
        reminders = []

        print_events_and_reminders(events, reminders)
        captured = capsys.readouterr()

        assert "📅 Today's Schedule:" in captured.out
        assert "📅 Team Meeting" in captured.out
        assert "✅ Today's Reminders:" not in captured.out

    def test_print_events_and_reminders_reminders_only(self, capsys):
        """Test printing only reminders."""
        events = []
        reminders = [
            {
                "title": "Review Budget",
                "due_date": "2024-01-15T00:00:00",
            }
        ]

        print_events_and_reminders(events, reminders)
        captured = capsys.readouterr()

        assert "📅 Today's Schedule:" in captured.out
        assert "📅 No events found" in captured.out
        assert "✅ Today's Reminders:" in captured.out
        assert "✅ Review Budget" in captured.out

    def test_print_events_and_reminders_empty(self, capsys):
        """Test printing when both lists are empty."""
        events = []
        reminders = []

        print_events_and_reminders(events, reminders)
        captured = capsys.readouterr()

        assert "📅 Today's Schedule:" in captured.out
        assert "📅 No events found" in captured.out
        assert "✅ Today's Reminders:" not in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
