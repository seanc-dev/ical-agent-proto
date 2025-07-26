# Calendar Assistant - Future Enhancements

## Completed Work

- ✅ Date/time parsing error handling (invalid formats, leap years, out-of-range values).
- ✅ Missing duration detection (prompts for duration when omitted).
- ✅ EventKit integration for create_event, delete_event, move_event, add_notification, and recurring events.
- ✅ Natural language fallback parsing and LLM-driven interpretation for dates, times, durations, and locations.
- ✅ Comprehensive test suite: unit tests, CLI integration tests, NLP fallback tests, LLM invocation tests.
- ✅ End-to-end CLI tests with full pipeline testing (CLI → LLM → EventKit).

## Roadmap

### Prototype (v0.x): Robust CLI Calendar Assistant

**Core Functionality:**

- Interactive terminal loop with GPT-4o function calling for intent parsing.
- Core EventKit operations: full CRUD for events and reminders, including recurring events.
- Basic fallback parsing when API key is absent.
- User prompts for missing data (duration, location).
- Rich success/error messaging in CLI.

**Edge Case Handling & Robustness:**

- **Input Normalization**: Handle misspellings, poor grammar, mixed case, extra whitespace
- **Date/Time Robustness**: Invalid dates, past dates, leap years, timezone handling, ambiguous times
- **Event Management**: Duplicate detection, not found handling, multiple matches resolution
- **Natural Language**: Vague command clarification, context dependencies, multi-step requests
- **System Resilience**: Calendar access errors, network timeouts, concurrent access handling
- **User Experience**: Empty calendar handling, overflow protection, confirmation dialogs

**New Features to Add:**

- **Event Copying**: "copy team meeting to next week" → duplicate events with new dates
- **Bulk Operations**: "delete all meetings this week" → batch operations
- **Event Templates**: "schedule a 1:1 meeting" → predefined templates
- **Attendee Management**: "invite john@email.com to the meeting" → add attendees
- **Location Services**: "schedule meeting near downtown" → location-based scheduling
- **Search & Filter**: "find meetings about project X" → fuzzy search capabilities
- **Undo Operations**: "undo last action" → implement undo stack
- **Confirmation Dialogs**: "delete important meeting" → ask for confirmation

**Email Integration (Moved from MVP):**

- Multi-platform Email integration (Gmail, Apple Mail via IMAP/SMTP)
- Read, send, and categorize emails
- Email-to-calendar integration: "schedule meeting from email about project X"

**Checklist/Note Storage:**

- Persistent checklist storage: "remember I have 5 things to do"
- Context-aware conversations: "what was I supposed to do today?"
- Integration with calendar: "remind me about my checklist during meetings"
- Smart suggestions: "based on my checklist, when should I schedule X?"

### MVP (v1.0): AI-driven Mental Health Coaching App

- Calendar integration across platforms: unified 'Today' dashboard aggregating events, reminders, and emails.
- Wins tracking and celebration: allow users to log achievements and view milestones.
- Therapy Mode: AI-guided journaling prompts, check-ins, and personalized coaching messages.
- Resource Library: curated articles, helplines, and initial EAP program links.
- Advanced natural-language scheduling: model-based handling of dates/times/recurrences/locations/durations.
- Responsive web frontend (React) and foundational mobile UI for iOS/Android.
- Secure authentication and user profile management (OAuth for calendar and email).

### Launch (v2.x): Enterprise & Advanced Features

- Telehealth integration: scheduling and managing sessions with human therapists, video call link generation.
- Corporate Wellness Dashboard: admin analytics on usage, engagement, and wellness metrics.
- Native mobile apps (iOS in Swift, Android in Kotlin) with push notifications and offline support.
- Voice assistant support: Siri and Google Assistant command integration.
- Biometric and wearable data integration for stress and mood tracking.
- Internationalization and compliance: multi-language support, GDPR/HIPAA readiness.
- API for third-party integrations and developer ecosystem.

**Once MVP features are stabilized and tested, revisit expanding the core CLI into the full app platform with these advanced capabilities.**
