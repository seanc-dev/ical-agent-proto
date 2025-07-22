# Core EventKit Integration Plan

## 1. Objective

- Implement event creation, deletion, moving, and notification via EventKit.

## 2. Behavior

### 2.1 create_event

- Requires `title`, `date`, `time`, `duration` (minutes).
- Optional `location`.
- Returns `success: True` with `message` on creation.
- Returns `success: False` and descriptive `error` on missing or invalid fields.

### 2.2 delete_event

- Requires `title`, `date`.
- Returns `success: True` with `message` on deletion.
- Returns `success: False` and descriptive `error` on missing or invalid fields.

### 2.3 move_event

- Requires `title`, `old_date`, `new_date`, `new_time`.
- Returns `success: True` with `message` on moving event.
- Returns `success: False` and descriptive `error` on missing or invalid fields.

### 2.4 add_notification

- Requires `title`, `date`, `minutes_before`.
- Returns `success: True` with `message` on scheduling notification.
- Returns `success: False` and descriptive `error` on missing or invalid fields.

## 3. Testing Strategy

- Scaffold failing tests in `tests/test_eventkit_core_integration.py`:
  - Missing required fields for each function.
  - Valid inputs should eventually result in `success: True`.

## 4. Implementation Steps

1. Create this plan file.
2. Scaffold failing test suite hierarchy:
   - `describe(create_event)` → `it(missing fields)` → `it(success case)`
   - Similar structure for `delete_event`, `move_event`, `add_notification`.
3. Implement minimal code in `calendar_agent_eventkit.py` to satisfy first failing test.
4. Iterate feature by feature until all tests pass.
5. Delete this plan file once feature is complete and merged.
