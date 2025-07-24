# Calendar Assistant - Future Enhancements

## Completed Work

- ✅ Date/time parsing error handling (invalid formats, leap years, out-of-range values).
- ✅ Missing duration detection (returns error when duration is omitted).
- ✅ Removed legacy AppleScript-based agent and migrated to EventKit integration.

## Next Priorities

### Phase 1: Core EventKit Integration

1. Implement `create_event`: Use EventKit to create events with title, date, time, duration, and location.
2. Implement `delete_event`: Remove events via EventKit.
3. Implement `move_event`: Reschedule events using EventKit.
4. Implement `add_notification`: Add notifications/reminders to events via EventKit.
5. Improve CLI feedback: Provide clear success and error messages.

### Phase 2: Smart Features & NLP Enhancements

- Natural language extraction of duration and location (e.g., "2-hour meeting at cafe").
- Travel time calculation and automatic travel-time alerts.
- Recurring events support (e.g., "every Monday").
- Smart scheduling suggestions with conflict detection.

### Phase 3: Enhanced UX & Platform Expansion

- Confirmation prompts and undo operations in CLI.
- Voice integration (Siri/voice assistant) for hands-free interaction.
- iOS/macOS native app: widgets, Siri shortcuts, share extensions, and background sync.

## Notes

- This Python CLI remains a prototype; plan for a Swift/iOS migration leveraging EventKit.
- Maintain backward compatibility with the current CLI API for seamless upgrades.

## Project Rules

- Commit any substantial changes incrementally with clear, descriptive messages.
- Use dedicated feature branches for each new feature or bugfix.
- Ensure all tests (unit, integration, CLI) pass before merging to main.
- Keep integration tests marked separately to avoid slowing down the default test suite.
