import pytest
from tests.test_cli_output import run_cli
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
