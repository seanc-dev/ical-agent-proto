# Date Utilities Extraction Plan

## 1. Objective

Extract all date parsing and resolution logic from `openai_client.py` and `calendar_agent_eventkit.py` into a dedicated `date_utils` module.

## 2. Behavior

### 2.1 ISO Date Parsing

- Correctly parse `YYYY-MM-DD` strings.

### 2.2 Relative Dates

- Recognize and convert `"tomorrow"` to the next calendar date.
- Compute the next occurrence of a weekday name (Monday–Sunday).

## 3. Testing Strategy

1. Write unit tests in `tests/test_date_utils.py` covering:
   - ISO date strings
   - "tomorrow"
   - Weekday names
   - Invalid inputs

## 4. Implementation Steps

1. Scaffold failing tests for `date_utils` in `tests/test_date_utils.py`.
2. Create `utils/date_utils.py` with stub functions: `parse_date_string` and `next_weekday`.
3. Implement logic to satisfy tests.
4. Refactor `openai_client.interpret_command` and `calendar_agent_eventkit` to use `date_utils`.
5. Remove this plan file once merged.
