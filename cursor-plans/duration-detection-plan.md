# Duration Detection Plan

## 1. Objective

Prompt the user for event duration when missing, default to one hour if accepted.

## 2. Behavior

### 2.1 Missing Duration

- Input lacking duration triggers an error response or follow-up.
- Default duration: one hour if user accepts.

## 3. Testing Strategy

- Scaffold a failing test in `test_assistant.py` for `create_event` without duration.
- Assert that `create_event(details_without_duration)` returns `error: "Missing duration"`.

## 4. Implementation Steps

1. Add failing test in `test_assistant.py`.
2. Update `calendar_agent_eventkit.py` stub to check for missing duration.
3. Run tests and iterate until tests pass.
4. Delete this plan file once merged.
