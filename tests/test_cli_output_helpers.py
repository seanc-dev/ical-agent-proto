import pytest
from utils.cli_output import format_events, format_reminders, print_events_and_reminders


def test_format_events_empty():
    assert format_events([]) == "\n📅 Events:\n  (none)"


def test_format_events_multiple():
    events = ["E1", "E2"]
    expected = "\n📅 Events:\n  - E1\n  - E2"
    assert format_events(events) == expected


def test_format_reminders_empty():
    assert format_reminders([]) == "\n⏰ Reminders:\n  (none)"


def test_format_reminders_multiple():
    reminders = ["R1", "R2"]
    expected = "\n⏰ Reminders:\n  - R1\n  - R2"
    assert format_reminders(reminders) == expected


def test_print_events_and_reminders(capsys):
    events = ["E1"]
    reminders = ["R1"]
    print_events_and_reminders(events, reminders)
    captured = capsys.readouterr()
    assert captured.out == "\n📅 Events:\n  - E1\n\n⏰ Reminders:\n  - R1\n"
