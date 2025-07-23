import pytest
from datetime import datetime
from calendar_agent_eventkit import (
    create_event,
    delete_event,
    move_event,
    add_notification,
    list_events_and_reminders,
)

# Tests for create_event


def test_create_event_missing_fields():
    res = create_event({})
    assert res["success"] is False
    # Missing title should be reported first
    assert "Missing title" in res.get("error", "")


def test_create_event_success():
    details = {
        "title": "Test Event",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": "10:00",
        "duration": 60,
    }
    res = create_event(details)
    assert res.get("success") is True


# Tests for delete_event


def test_delete_event_missing_fields():
    res = delete_event({})
    assert res["success"] is False
    assert "title" in res.get("error", "") or "date" in res.get("error", "")


def test_delete_event_success():
    details = {"title": "Test Event", "date": datetime.now().strftime("%Y-%m-%d")}
    res = delete_event(details)
    assert res.get("success") is True


# Tests for move_event


def test_move_event_missing_fields():
    res = move_event({})
    assert res["success"] is False
    assert "old_date" in res.get("error", "") or "new_date" in res.get("error", "")


def test_move_event_success():
    details = {
        "title": "Test Event",
        "old_date": datetime.now().strftime("%Y-%m-%d"),
        "new_date": datetime.now().strftime("%Y-%m-%d"),
        "new_time": "11:00",
    }
    res = move_event(details)
    assert res.get("success") is True


# Tests for add_notification


def test_add_notification_missing_fields():
    res = add_notification({})
    assert res["success"] is False
    assert "minutes_before" in res.get("error", "")


def test_add_notification_success():
    details = {
        "title": "Test Event",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "minutes_before": 15,
    }
    res = add_notification(details)
    assert res.get("success") is True


# Tests for list_events_and_reminders


def test_list_events_default():
    res = list_events_and_reminders()
    assert isinstance(res, dict)
    assert "events" in res and isinstance(res["events"], list)
    assert "reminders" in res and isinstance(res["reminders"], list)


def test_list_events_invalid_date():
    res = list_events_and_reminders("invalid", "invalid")
    assert "error" in res
