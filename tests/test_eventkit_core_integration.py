import pytest
from datetime import datetime
from calendar_agent_eventkit import (
    create_event,
    delete_event,
    move_event,
    add_notification,
)

# Tests for create_event


def test_create_event_missing_fields():
    res = create_event({})
    assert res["success"] is False
    assert "duration" in res.get("error", "")


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
