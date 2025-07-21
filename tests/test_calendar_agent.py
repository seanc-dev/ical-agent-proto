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
