# Calendar Assistant - Future Enhancements

## Current Issues to Fix

### Event Creation

- ✅ **Fixed**: End date not being set properly (now defaults to 1 hour duration)
- ✅ **Completed**: LLM now prompts for duration if not specified
- ✅ **Completed**: Better error handling for date/time parsing

## Planned Features (v2)

### Smart Event Creation

- **Duration Detection**: LLM should ask "Is one hour enough?" when duration isn't specified
- **Location Support**: Extract and set event location
- **Travel Time**: Calculate and add travel time to event duration
- **Smart Scheduling**: Suggest optimal times based on existing calendar

### Notification & Reminder System

- **Travel Time Alerts**: Set notifications based on travel time to location
- **Custom Reminder Preferences**: User-configurable reminder times (15min, 1hr, 1 day before)
- **Smart Notifications**: Different reminder types for different event types

### Enhanced Natural Language Processing

- **Duration Extraction**: "2-hour meeting", "quick 30min call"
- **Location Parsing**: "at the coffee shop", "downtown office"
- **Recurring Events**: "every Monday", "weekly team meeting"
- **Event Types**: "lunch", "meeting", "appointment" with different defaults

### Calendar Management

- **Multiple Calendar Support**: Create events in specific calendars
- **Event Templates**: Quick creation for common event types
- **Conflict Detection**: Warn about scheduling conflicts
- **Bulk Operations**: "Move all meetings this week to next week"

### User Experience

- **Confirmation Prompts**: "Create 1-hour meeting with Alex tomorrow at 2pm?"
- **Undo Operations**: "Undo last action"
- **Event Templates**: "Quick lunch", "Team meeting", "Doctor appointment"
- **Voice Integration**: Future Siri/voice assistant integration

### Technical Improvements

- **Error Recovery**: Better handling of AppleScript failures
- **Performance**: Cache calendar data for faster queries
- **Logging**: Track user actions for improvement
- **Testing**: Automated tests for all operations

### iOS/macOS Native App Features

- **Widget Support**: Quick calendar view
- **Siri Shortcuts**: Voice commands
- **Share Extension**: Create events from other apps
- **Background Sync**: Real-time calendar updates

## Implementation Priority

### Phase 1 (Immediate)

1. Fix duration detection in LLM
2. Add location support
3. Improve error handling

### Phase 2 (Short-term)

1. Smart notification system
2. Travel time integration
3. Event templates

### Phase 3 (Medium-term)

1. Native iOS/macOS app
2. Voice integration
3. Advanced NLP features

## Notes

- Keep the current Python implementation as a prototype
- Plan for eventual Swift/iOS migration
- Consider using EventKit framework for native app
- Maintain backward compatibility with current API
