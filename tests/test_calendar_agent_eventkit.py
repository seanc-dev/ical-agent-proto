import pytest
from datetime import datetime
from calendar_agent_eventkit import (
    list_events_and_reminders,
    create_event,
    delete_event,
    move_event,
)


def test_list_events_and_reminders_defaults():
    result = list_events_and_reminders()
    assert isinstance(result, dict)
    assert "events" in result and isinstance(result["events"], list)
    assert "reminders" in result and isinstance(result["reminders"], list)
    assert result["events"] == []
    assert result["reminders"] == []


def test_list_events_and_reminders_invalid_date():
    result = list_events_and_reminders("invalid", "invalid")
    assert "error" in result


def test_create_event_missing_duration():
    details = {
        "title": "Test",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": "10:00",
    }
    result = create_event(details)
    assert result == {"success": False, "error": "Missing duration"}


def test_create_event_not_implemented():
    details = {
        "title": "Test",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": "10:00",
        "duration": 60,
    }
    result = create_event(details)
    assert result == {"success": False, "error": "Not implemented"}


def test_delete_event_not_implemented():
    result = delete_event({})
    assert result == {"success": False, "error": "Not implemented"}


def test_move_event_not_implemented():
    result = move_event({})
    assert result == {"success": False, "error": "Not implemented"}
