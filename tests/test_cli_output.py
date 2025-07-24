import pytest
import runpy
import builtins
import sys
import re


def run_cli(inputs):
    """
    Helper to run `main.py` with a sequence of inputs and capture printed output.
    """
    printed = []

    def fake_input(prompt=""):
        return inputs.pop(0)

    def fake_print(*args, **kwargs):
        printed.append(" ".join(str(a) for a in args))

    monkeypatch = pytest.MonkeyPatch()
    import openai_client

    # Stub interpret_command with simple rule-based mapping for tests
    def fallback_map(cmd):
        # Map commands to actions with explicit details for tests
        if cmd == "list events from invalid to invalid":
            return {
                "action": "list_events_only",
                "details": {"start_date": "invalid", "end_date": "invalid"},
            }
        if cmd == "show my events":
            return {"action": "list_events_only", "details": {}}
        if cmd == "show my reminders":
            return {"action": "list_reminders_only", "details": {}}
        if cmd.lower() in ("what's on today?", "what’s on today?"):
            return {"action": "list_all", "details": {}}
        if cmd.startswith("schedule Meeting on 2025-07-23 at 10:00 for 30 minutes"):
            return {
                "action": "create_event",
                "details": {
                    "title": "Meeting",
                    "date": "2025-07-23",
                    "time": "10:00",
                    "duration": 30,
                },
            }
        if cmd.startswith("schedule Lunch tomorrow at 12:00"):
            return {
                "action": "create_event",
                "details": {"title": "Lunch", "date": "tomorrow", "time": "12:00"},
            }
        # Generic schedule Meeting commands
        m_sched = re.match(
            r"schedule Meeting on (\d{4}-\d{2}-\d{2}) at (\d{1,2}:\d{2}) for (\d+) minutes",
            cmd,
        )
        if m_sched:
            return {
                "action": "create_event",
                "details": {
                    "title": "Meeting",
                    "date": m_sched.group(1),
                    "time": m_sched.group(2),
                    "duration": int(m_sched.group(3)),
                },
            }
        if cmd.startswith("delete Meeting on 2025-07-23"):
            return {
                "action": "delete_event",
                "details": {"title": "Meeting", "date": "2025-07-23"},
            }
        # Generic delete Meeting command
        m_del = re.match(r"delete Meeting on (\d{4}-\d{2}-\d{2})", cmd)
        if m_del:
            return {
                "action": "delete_event",
                "details": {"title": "Meeting", "date": m_del.group(1)},
            }
        if cmd.startswith("move Meeting on 2025-07-23 to 2025-07-24 at 11:00"):
            return {
                "action": "move_event",
                "details": {
                    "title": "Meeting",
                    "old_date": "2025-07-23",
                    "new_date": "2025-07-24",
                    "new_time": "11:00",
                },
            }
        # Generic move Meeting command
        m_move = re.match(
            r"move Meeting on (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2}) at (\d{1,2}:\d{2})",
            cmd,
        )
        if m_move:
            return {
                "action": "move_event",
                "details": {
                    "title": "Meeting",
                    "old_date": m_move.group(1),
                    "new_date": m_move.group(2),
                    "new_time": m_move.group(3),
                },
            }
        if cmd.startswith(
            "add notification to Meeting on 2025-07-24 15 minutes before"
        ):
            return {
                "action": "add_notification",
                "details": {
                    "title": "Meeting",
                    "date": "2025-07-24",
                    "minutes_before": 15,
                },
            }
        # Generic add notification for Meeting
        m_notify = re.match(
            r"add notification to Meeting on (\d{4}-\d{2}-\d{2}) (\d+) minutes before",
            cmd,
        )
        if m_notify:
            return {
                "action": "add_notification",
                "details": {
                    "title": "Meeting",
                    "date": m_notify.group(1),
                    "minutes_before": int(m_notify.group(2)),
                },
            }
        # Support "today's events" listing
        if cmd.lower() == "today's events":
            return {"action": "list_events_only", "details": {}}
        # Support "tomorrow's events" listing
        if cmd.lower() == "tomorrow's events":
            return {"action": "list_events_only", "details": {}}
        # Generic support for "events for ..."
        if cmd.lower().startswith("events for "):
            return {"action": "list_events_only", "details": {}}
        # Default unknown
        return {"action": "unknown", "details": {}}

    monkeypatch.setitem(
        sys.modules,
        "dotenv",
        __import__("types").SimpleNamespace(load_dotenv=lambda: None),
    )
    monkeypatch.setattr(builtins, "input", fake_input)
    monkeypatch.setattr(builtins, "print", fake_print)
    monkeypatch.setattr(openai_client, "interpret_command", fallback_map)
    runpy.run_module("main", run_name="__main__")
    monkeypatch.undo()
    return printed


class TestCLIListingOutput:
    def test_list_events_only_empty(self):
        outputs = run_cli(["show my events", "exit"])
        assert any("📅 Events:" in line for line in outputs)
        # Should show '(none)'
        assert any("(none)" in line for line in outputs)

    def test_list_reminders_only_empty(self):
        outputs = run_cli(["show my reminders", "exit"])
        assert any("⏰ Reminders:" in line for line in outputs)
        assert any("(none)" in line for line in outputs)

    def test_list_all_empty(self):
        outputs = run_cli(["what’s on today?", "exit"])
        assert any("📅 Events:" in line for line in outputs)
        assert any("⏰ Reminders:" in line for line in outputs)


class TestCLIErrorOutput:
    def test_invalid_date_error(self):
        outputs = run_cli(["list events from invalid to invalid", "exit"])
        assert any("❌ Error:" in line for line in outputs)
        # Should not list events or reminders
        assert not any("📅 Events:" in line for line in outputs)
        assert not any("⏰ Reminders:" in line for line in outputs)


class TestCLICreateConfirm:
    def test_create_confirm_prompt(self):
        # This test will be implemented once confirm flag is in place
        pytest.skip("Confirm prompt not yet implemented")


# TODO: More tests for create/delete/move/notify output formatting


class TestCLIOtherActionsOutput:
    def test_create_event_success(self):
        outputs = run_cli(
            ["schedule Meeting on 2025-07-23 at 10:00 for 30 minutes", "exit"]
        )
        assert any("✅ Event created successfully" in line for line in outputs)

    def test_create_event_missing_duration(self):
        pytest.skip("Interactive duration prompt behavior not yet covered by CLI tests")

    def test_delete_event_success(self):
        outputs = run_cli(["delete Meeting on 2025-07-23", "exit"])
        assert any("✅ Event deleted successfully" in line for line in outputs)

    def test_move_event_success(self):
        outputs = run_cli(["move Meeting on 2025-07-23 to 2025-07-24 at 11:00", "exit"])
        assert any("✅ Event moved successfully" in line for line in outputs)

    def test_add_notification_success(self):
        outputs = run_cli(
            ["add notification to Meeting on 2025-07-24 15 minutes before", "exit"]
        )
        assert any("✅ Notification added successfully" in line for line in outputs)

    def test_unknown_action(self):
        outputs = run_cli(["foobar", "exit"])
        assert any("[Not implemented yet]" in line for line in outputs)
