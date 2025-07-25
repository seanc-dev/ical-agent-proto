# Main Loop Dispatcher Refactor Plan

## Overview

Refactor the main loop in `main.py` by extracting action handlers into a centralized dispatcher module.

## Goals

- Remove the large `if-elif` chain in `main.py`.
- Introduce `utils/command_dispatcher.py` with:
  - A mapping of action names to handler functions.
  - A unified `dispatch(action: str, details: dict)` function that executes the correct handler.
- Keep existing CLI behavior and tests passing.

## Sections

### 1. Command Dispatcher Module

- Create `utils/command_dispatcher.py`.
- Define handler functions for each action (`list_todays_events`, `list_all`, `list_events_only`, `list_reminders_only`, `create_event`, `delete_event`, `move_event`, `add_notification`, and a default unknown handler).
- Assemble a dict `HANDLERS: Dict[str, Callable]` mapping action names to handlers.
- Implement `dispatch(action: str, details: dict)` to look up and invoke the correct handler.

### 2. Handler Functions

- Each handler should:
  - Call the corresponding function from `calendar_agent_eventkit` or CLI helpers.
  - Handle errors and print appropriate messages.
- Example signature: `def handle_create_event(details: dict) -> None`.

### 3. Update `main.py`

- Import and call `dispatch` from the dispatcher module.
- Replace `if-elif` on `action` with `dispatch(action, details)`.

### 4. Testing

- **Unit Tests** (`tests/test_command_dispatcher.py`):
  - Test that `HANDLERS` contains all expected action keys.
  - Test that `dispatch` raises or handles unknown actions appropriately.
  - Test that each valid action runs without error (use mocks for calendar and CLI helpers).
- **Integration Tests**:
  - Ensure CLI end-to-end flow still passes.

## Timeline

- **Step 1:** Create plan file and stub module.
- **Step 2:** Scaffold unit test stubs (failing tests).
- **Step 3:** Implement dispatcher and handlers.
- **Step 4:** Refactor `main.py` and update tests.
- **Step 5:** Run and fix tests.
