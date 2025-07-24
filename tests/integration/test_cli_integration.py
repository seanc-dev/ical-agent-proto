import pytest
from tests.test_cli_output import run_cli
import re
from datetime import datetime, timedelta

pytestmark = pytest.mark.integration


class TestNaturalLanguageListing:
    def test_list_today_variations(self):
        # Should list empty events for various 'today' commands
        for cmd in ["show my events", "what's on today?", "today's events"]:
            outputs = run_cli([cmd, "exit"])
            assert any("📅 Events:" in line for line in outputs)
            assert any("(none)" in line for line in outputs)

    def test_list_specific_date(self):
        # Should list (none) for explicit date
        date = datetime.now().strftime("%Y-%m-%d")
        outputs = run_cli([f"events for {date}", "exit"])
        assert any("📅 Events:" in line for line in outputs)
        assert any("(none)" in line for line in outputs)

    def test_list_tomorrow(self):
        # Should list (none) for tomorrow's events
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        outputs = run_cli([f"events for {tomorrow}", "exit"])
        assert any("📅 Events:" in line for line in outputs)
        assert any("(none)" in line for line in outputs)


class TestCRUDFlow:
    def test_create_move_notify_delete_sequence(self):
        # Full CRUD flow: create, move, notify, delete
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        commands = [
            f"schedule Meeting on {tomorrow} at 10:00 for 30 minutes",
            f"move Meeting on {tomorrow} to {tomorrow} at 11:00",
            f"add notification to Meeting on {tomorrow} 15 minutes before",
            f"delete Meeting on {tomorrow}",
            "exit",
        ]
        outputs = run_cli(commands)
        assert any("✅ Event created successfully" in line for line in outputs)
        assert any("✅ Event moved successfully" in line for line in outputs)
        assert any("✅ Notification added successfully" in line for line in outputs)
        assert any("✅ Event deleted successfully" in line for line in outputs)

    def test_schedule_then_list_sequence(self):
        # End-to-end schedule then list flow
        date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        commands = [
            f"schedule Meeting on {date} at 10:00 for 30 minutes",
            "show my events",
            "exit",
        ]
        outputs = run_cli(commands)
        # Confirm creation
        assert any("✅ Event created successfully" in line for line in outputs)
        # Confirm listing includes the event with correct timestamp
        assert any("📅 Events:" in line for line in outputs)
        pattern = rf"Meeting \| {date} 10:00:00"
        assert any(
            re.search(pattern, line) for line in outputs
        ), f"Did not find scheduled event in output: {outputs}"

    def test_schedule_and_explicit_date_list(self):
        # End-to-end schedule then explicit date list
        today = datetime.now().strftime("%Y-%m-%d")
        commands = [
            f"schedule Meeting on {today} at 11:00 for 45 minutes",
            f"events for {today}",
            "exit",
        ]
        outputs = run_cli(commands)
        # Confirm creation
        assert any("✅ Event created successfully" in line for line in outputs)
        # Confirm explicit date listing includes the event
        assert any("📅 Events:" in line for line in outputs)
        pattern_today = rf"Meeting \| {today} 11:00:00"
        assert any(
            re.search(pattern_today, line) for line in outputs
        ), f"Explicit date list missing event: {outputs}"

    def test_create_and_delete_listing(self):
        # Verify deletion removes event from listing
        date = datetime.now().strftime("%Y-%m-%d")
        commands = [
            f"schedule Meeting on {date} at 12:00 for 15 minutes",
            "show my events",
            f"delete Meeting on {date}",
            "show my events",
            "exit",
        ]
        outputs = run_cli(commands)
        # Find all listing sections
        sections = [i for i, line in enumerate(outputs) if "📅 Events:" in line]
        assert len(sections) >= 2, f"Expected two listing sections, got: {sections}"
        first_idx, second_idx = sections[0], sections[1]
        # First listing should contain the event
        first_block = outputs[first_idx:second_idx]
        assert any(
            re.search(rf"Meeting \| {date} 12:00:00", line) for line in first_block
        ), "Event missing in first listing"
        # After deletion, second listing shows (none)
        second_block = outputs[second_idx + 1 :]
        assert any(
            "(none)" in line for line in second_block
        ), f"Expected no events after deletion, got: {second_block}"
