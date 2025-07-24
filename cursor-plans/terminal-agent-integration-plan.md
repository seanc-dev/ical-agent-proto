# Terminal Agent End-to-End Integration Testing Plan

## 1. Natural Language Listing

- 1.1 List today’s events via generic commands: “show me my events”, “what’s on today?”, “today’s events”
- 1.2 Validate empty calendar outputs “(none)” under 📅 or ⏰ headings
- 1.3 List specific date via “events for YYYY-MM-DD” yields correct date
- 1.4 List tomorrow’s events via phrase “tomorrow’s events” yields next day
- 1.5 Invalid date range command “list events from invalid to invalid” shows ❌ Error and no listing headings

## 2. Create-Read-Update-Delete Flow (One-off)

- 2.1 Schedule an event: “schedule Meeting on 2025-07-24 at 12:00 for 30 minutes” → ✅ confirmation
- 2.2 Verify listing includes newly created event
- 2.3 Move the event: “move Meeting on 2025-07-24 to 2025-07-25 at 13:30” → ✅ confirmation
- 2.4 Verify listing reflects updated date/time
- 2.5 Add notification: “add notification to Meeting on 2025-07-25 15 minutes before” → ✅ confirmation
- 2.6 Delete the event: “delete Meeting on 2025-07-25” → ✅ confirmation
- 2.7 Verify listing no longer shows the event

## 3. Recurring Events (COUNT-based)

- 3.1 Create daily recurring: “schedule Standup on 2025-07-26 at 09:00 for 15 minutes recurrence FREQ=DAILY;COUNT=3” → ✅ confirmation
- 3.2 List occurrences across full span and confirm 3 entries
- 3.3 Delete single occurrence: “delete Standup on 2025-07-27” → ✅ confirmation, two remaining
- 3.4 Delete entire series: “delete Standup on 2025-07-26 series” → ✅ confirmation, none remaining

## 4. Error and Edge Cases

- 4.1 Missing required fields in create: “schedule Lunch tomorrow at 12:00” → prompt duration, handle invalid input
- 4.2 Invalid move: “move X on 2025-01-01 to 2025-01-02 at 10:00” → ❌ explicit not-found error
- 4.3 Unknown action: “foobar” → “[Not implemented yet]” response

## 5. CI Automation

- 5.1 Create dedicated pytest test file `tests/test_cli_integration.py` using `run_cli` fixture
- 5.2 Tag these tests so CI can run fast via `pytest -m cli_integration`
- 5.3 Ensure full suite runs on merge to main

_Once this plan is in place, we can scaffold each test case and iterate to implement and verify._
