# pylint: skip-file
# type: ignore
import pytest  # noqa: E0401
from datetime import datetime, timedelta
from calendar_agent_eventkit import (
    create_event,
    list_events_and_reminders,
    delete_event,
)


@pytest.mark.recurring
class TestRecurringEvents:
    def test_create_recurring_daily_event_missing_rule(self):
        # Missing recurrence_rule should succeed as a single event
        details = {
            "title": "Daily Standup",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": "09:00",
            "duration": 15,
        }
        res = create_event(details)
        assert res["success"]

    def test_create_recurring_daily_event_success(self):
        # Create event with daily recurrence for 3 days
        details = {
            "title": "Daily Standup",
            "date": "2025-07-23",
            "time": "09:00",
            "duration": 15,
            "recurrence_rule": "FREQ=DAILY;COUNT=3",
        }
        res = create_event(details)
        assert res["success"]

    def test_list_recurring_daily(self):
        # List occurrences over 3-day range
        start = "2025-07-23"
        end = "2025-07-25"
        res = list_events_and_reminders(start, end)
        # Expect 3 occurrences
        assert len(res.get("events", [])) == 3

    def test_delete_one_occurrence(self):
        # Delete only the second occurrence
        details = {
            "title": "Daily Standup",
            "date": "2025-07-24",
            "delete_series": False,
        }
        res = delete_event(details)
        assert res["success"]

    def test_delete_series(self):
        # Delete entire series
        details = {
            "title": "Daily Standup",
            "date": "2025-07-24",
            "delete_series": True,
        }
        res = delete_event(details)
        assert res["success"]
