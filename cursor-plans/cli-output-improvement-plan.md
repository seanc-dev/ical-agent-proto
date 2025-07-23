# CLI Output Improvement Plan

## 1. Objective

- Enhance the terminal interface for consistency, clarity, and robust error handling.

## 2. Behavior

### 2.1 Listing

- Always print error messages first if present (e.g., invalid date).
- Display events under “📅 Events:” with indented bullets.
- Display reminders under “⏰ Reminders:” with indented bullets.
- For empty lists, show “(none)”.

### 2.2 Create / Delete / Move / Notify

- After creating, ask for confirmation before executing: e.g., “Create event ‘X’ on date at time for duration? (Y/n)” when run interactively.
- On success, print: ✅ [message]
- On error, print: ❌ Error: [error]

### 2.3 Unknown Actions

- Print “[Not implemented yet]” in gray or with prefix ❓

## 3. Testing Strategy

- Use pytest with `capsys` to capture stdout:
  - Simulate user input for list commands and assert formatted output.
  - Test error case: invalid date → prints ❌ Error: … and no bullet lists.
  - Snapshot tests for full CLI session (e.g., list_all, list_events_only, list_reminders_only).

## 4. Implementation Steps

1. Scaffold failing tests in `tests/test_cli_output.py` covering all behaviors.
2. Update `main.py` to:
   - Detect `error` in results and handle accordingly before listing.
   - Always print “📅 Events:” and “⏰ Reminders:” with fallback “(none)”.
   - Implement confirmation prompts under a flag (e.g., `--confirm`).
3. Iterate until tests pass.
4. Remove plan file and merge.
