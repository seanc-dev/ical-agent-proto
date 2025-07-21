import types
import calendar_agent


def test_date_parts():
    assert calendar_agent._date_parts("2024-07-28") == (2024, 7, 28)


def test_create_event_requires_date():
    result = calendar_agent.create_event({"title": "Test"})
    assert not result["success"]
    assert "Date is required" in result["error"]


def test_delete_event_requires_fields():
    result = calendar_agent.delete_event({"date": "2024-01-01"})
    assert not result["success"]


def test_move_event_requires_fields():
    result = calendar_agent.move_event({"title": "t"})
    assert not result["success"]


def test_warm_up_calendar(monkeypatch):
    def fake_run(*args, **kwargs):
        return types.SimpleNamespace(stdout="WARMUP_OK")
    monkeypatch.setattr(calendar_agent.subprocess, "run", fake_run)
    assert calendar_agent._warm_up_calendar()


def test_list_events_and_reminders(monkeypatch):
    def fake_warm():
        return True
    monkeypatch.setattr(calendar_agent, "_warm_up_calendar", fake_warm)

    fake_output = "DEBUG:stuff EVENTS:event1\\nREMINDERS:rem1"

    def fake_run(*args, **kwargs):
        return types.SimpleNamespace(stdout=fake_output, stderr="")

    monkeypatch.setattr(calendar_agent.subprocess, "run", fake_run)
    result = calendar_agent.list_events_and_reminders("2024-01-01", "2024-01-01")
    assert any("event1" in e for e in result["events"])
    assert any("rem1" in r for r in result["reminders"])


def test_create_event_default_duration_warning(monkeypatch):
    captured = {}

    def fake_run(cmd, capture_output=True, text=True, check=False):
        captured["script"] = cmd[2]
        return types.SimpleNamespace(stdout="SUCCESS: Event created", stderr="")

    monkeypatch.setattr(calendar_agent.subprocess, "run", fake_run)
    result = calendar_agent.create_event({"title": "Test", "date": "2024-08-01", "time": "10:00"})
    assert result["success"]
    assert "warning" in result and "defaulting to 60 minutes" in result["warning"]


def test_create_event_includes_location(monkeypatch):
    captured = {}

    def fake_run(cmd, capture_output=True, text=True, check=False):
        captured["script"] = cmd[2]
        return types.SimpleNamespace(stdout="SUCCESS: Event created", stderr="")

    monkeypatch.setattr(calendar_agent.subprocess, "run", fake_run)
    result = calendar_agent.create_event({
        "title": "Meeting",
        "date": "2024-08-01",
        "time": "10:00",
        "duration": 30,
        "location": "Office",
    })
    assert result["success"]
    assert "set location of newEvent to \"Office\"" in captured["script"]


def test_create_event_invalid_date(monkeypatch):
    result = calendar_agent.create_event({"title": "Bad", "date": "2024-13-01", "time": "10:00"})
    assert not result["success"]
    assert "Date must be in YYYY-MM-DD format" in result["error"]


def test_create_event_invalid_time(monkeypatch):
    result = calendar_agent.create_event({"title": "Bad", "date": "2024-08-01", "time": "25:00"})
    assert not result["success"]
    assert "Time must be in HH:MM 24-hour format" in result["error"]


def test_move_event_invalid_time(monkeypatch):
    result = calendar_agent.move_event({
        "title": "Meet",
        "old_date": "2024-08-01",
        "new_date": "2024-08-02",
        "new_time": "99:99",
    })
    assert not result["success"]
    assert "Time must be in HH:MM 24-hour format" in result["error"]


def test_add_notification_builds_script(monkeypatch):
    captured = {}

    def fake_run(cmd, capture_output=True, text=True, check=False):
        captured["script"] = cmd[2]
        return types.SimpleNamespace(stdout="SUCCESS: Notification added", stderr="")

    monkeypatch.setattr(calendar_agent.subprocess, "run", fake_run)
    result = calendar_agent.add_notification({
        "title": "Meet",
        "date": "2024-08-01",
        "minutes_before": 30,
    })
    assert result["success"]
    assert "display alarm" in captured["script"] and "30" in captured["script"]


def test_add_notification_invalid_date(monkeypatch):
    result = calendar_agent.add_notification({"title": "t", "date": "2024-13-01"})
    assert not result["success"]
    assert "Date must be in YYYY-MM-DD format" in result["error"]

def test_delete_event_builds_script(monkeypatch):
    captured = {}
    def fake_run(cmd, capture_output=True, text=True, check=False):
        captured['script'] = cmd[2]
        return types.SimpleNamespace(stdout="SUCCESS: Event deleted", stderr="")
    monkeypatch.setattr(calendar_agent.subprocess, "run", fake_run)
    result = calendar_agent.delete_event({"title": "Meet", "date": "2024-08-01"})
    assert result["success"]
    assert "Event deleted successfully" in result["message"]
    assert "delete evt" in captured["script"]


def test_move_event_success(monkeypatch):
    captured = {}
    def fake_run(cmd, capture_output=True, text=True, check=False):
        captured['script'] = cmd[2]
        return types.SimpleNamespace(stdout="SUCCESS: Event moved", stderr="")
    monkeypatch.setattr(calendar_agent.subprocess, "run", fake_run)
    result = calendar_agent.move_event({
        "title": "Meet",
        "old_date": "2024-08-01",
        "new_date": "2024-08-02",
        "new_time": "10:00",
    })
    assert result["success"]
    assert "Event moved successfully" in result["message"]
    assert "Event moved" in captured["script"]
