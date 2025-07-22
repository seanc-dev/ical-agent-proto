# Date/Time Error Handling Plan

## 1. Objective

Enhance error handling in date/time parsing to provide clear feedback and prevent silent failures.

## 2. Behavior

### 2.1 Valid Dates

- Parse ISO date strings (`YYYY-MM-DD`) correctly.
- Handle `None` inputs by defaulting to today’s date.

### 2.2 Invalid Dates

- Detect invalid date formats (e.g., `"invalid"`, malformed strings).
- Return a result containing an `"error"` field with a descriptive message.
- Do not throw exceptions.

### 2.3 Boundary Conditions

- Reject out-of-range values (month > 12, day > 31).
- Handle leap years correctly (`"2024-02-29"` passes, `"2023-02-29"` errors).
- Ensure times beyond `23:59` are considered invalid.

## 3. API Changes

### list_events_and_reminders

- Modify return signature to include optional `"error"` key when parsing fails.

### CLI Behavior

- In `main.py`, detect `"error"` in result and display an error message instead of event/reminder lists.

## 4. Testing Strategy

1. Scaffold failing tests:
   - Assert that `list_events_and_reminders("invalid", "invalid")` returns a dict with `"error"`.
   - Assert that out-of-range dates produce an `"error"`.
2. Edge Cases:
   - Valid dates still return only `"events"` and `"reminders"`.
   - Leap year date passes; non-leap year date errors.

## 5. Implementation Steps

1. Scaffold failing tests in `test_assistant.py`.
2. Update `calendar_agent_eventkit.py` to include `"error"` in returned dict for parsing failures.
3. Update `main.py` to check for `"error"` and print error messages.
4. Run tests and iterate until they pass.
5. Delete this plan file once merged.
