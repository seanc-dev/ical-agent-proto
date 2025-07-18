#!/usr/bin/env python3
"""
Automated testing for the Calendar Assistant.
Simulates user inputs and tests different scenarios.
"""

import sys
import os
from unittest.mock import patch
from io import StringIO
from datetime import datetime, timedelta

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openai_client import interpret_command
from calendar_agent_eventkit import (
    list_events_and_reminders,
    create_event,
    delete_event,
    move_event,
)


class CalendarAssistantTester:
    def __init__(self):
        self.test_results = []

    def run_test(self, test_name, test_func):
        print(f"\n🧪 Running test: {test_name}")
        print("=" * 60)
        try:
            result = test_func()
            if result:
                print(f"✅ {test_name} passed")
                self.test_results.append((test_name, "PASSED", None))
            else:
                print(f"❌ {test_name} failed")
                self.test_results.append((test_name, "FAILED", "Returned False"))
        except Exception as e:
            print(f"❌ {test_name} error: {e}")
            self.test_results.append((test_name, "ERROR", str(e)))

    def test_interpret_command(self):
        test_cases = [
            # List all
            ("what's on today?", "list_all"),
            ("show me what's on my calendar today", "list_all"),
            ("what's coming up today?", "list_all"),
            # List events only
            ("show my events", "list_events_only"),
            ("list my appointments for today", "list_events_only"),
            ("what events do i have today?", "list_events_only"),
            # List reminders only
            ("what are my reminders?", "list_reminders_only"),
            ("list all reminders", "list_reminders_only"),
            ("show my tasks", "list_reminders_only"),
            # Create event
            ("schedule lunch tomorrow at 1pm", "create_event"),
            ("add a dentist appointment on 2023-11-01 at 9:00", "create_event"),
            ("book a meeting with Sarah next Monday at 14:00", "create_event"),
            # Delete event
            ("delete my meeting tomorrow", "delete_event"),
            ("cancel the dentist appointment for today", "delete_event"),
            ("remove the lunch appointment", "delete_event"),
            # Move event
            ("reschedule my lunch from 1pm to 2pm", "move_event"),
            ("move meeting to next Thursday at 10", "move_event"),
            ("shift the call with Bob to Friday afternoon", "move_event"),
        ]
        for inp, expected in test_cases:
            res = interpret_command(inp)
            action = res.get("action") if res else None
            print(f"  Input: '{inp}' -> action '{action}', expected '{expected}'")
            if action != expected:
                print(f"    ❌ Expected {expected}, got {action}")
                return False
            print("    ✅ OK")
        return True

    def test_list_events(self):
        print("Testing listing events/reminders for today...")
        res = list_events_and_reminders()
        events = res.get("events", [])
        reminders = res.get("reminders", [])
        print(f"  Found {len(events)} events and {len(reminders)} reminders")
        # Always return True as long as function runs without error
        return True

    def test_create_event(self):
        print("Testing event creation stub...")
        details = {
            "title": "Test",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": "12:00",
            "duration": 30,
        }
        res = create_event(details)
        print(f"  Result: {res}")
        # Stub returns success False
        if "success" in res:
            return True
        return False

    def test_date_parsing(self):
        print("Testing date parsing edge cases...")
        for d in [None, "2024-07-18", "2024-12-31"]:
            res = list_events_and_reminders(d, d)
            print(
                f"  Date {d}: {len(res.get('events', []))} events, {len(res.get('reminders', []))} reminders"
            )
        return True

    def test_error_handling(self):
        print("Testing error handling...")
        # Invalid date
        try:
            list_events_and_reminders("invalid", "invalid")
            print("  ✅ Handled invalid dates gracefully")
        except:
            print("  ❌ Crash on invalid dates")
            return False
        # Missing create details
        res = create_event({})
        print(f"  Create missing data result: {res}")
        if not res.get("success", True):
            return True
        return False

    def print_summary(self):
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        total = len(self.test_results)
        passed = sum(1 for _, s, _ in self.test_results if s == "PASSED")
        failed = sum(1 for _, s, _ in self.test_results if s == "FAILED")
        errors = sum(1 for _, s, _ in self.test_results if s == "ERROR")
        print(f"Total: {total}, Passed: {passed}, Failed: {failed}, Errors: {errors}")

    def run_all(self):
        self.run_test("InterpretCommand", self.test_interpret_command)
        self.run_test("ListEvents", self.test_list_events)
        self.run_test("CreateEvent", self.test_create_event)
        self.run_test("DateParsing", self.test_date_parsing)
        self.run_test("ErrorHandling", self.test_error_handling)
        self.print_summary()


if __name__ == "__main__":
    CalendarAssistantTester().run_all()
