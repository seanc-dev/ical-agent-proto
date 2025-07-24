# Calendar Assistant - Future Enhancements

## Completed Work

- ✅ Date/time parsing error handling (invalid formats, leap years, out-of-range values).
- ✅ Missing duration detection (prompts for duration when omitted).
- ✅ EventKit integration for create_event, delete_event, move_event, add_notification, and recurring events.
- ✅ Natural language fallback parsing and LLM-driven interpretation for dates, times, durations, and locations.
- ✅ Comprehensive test suite: unit tests, CLI integration tests, NLP fallback tests, LLM invocation tests.

## Roadmap

### Prototype (v0.x): CLI Calendar Assistant

- Interactive terminal loop with GPT-4o function calling for intent parsing.
- Core EventKit operations: full CRUD for events and reminders, including recurring events.
- Basic fallback parsing when API key is absent.
- User prompts for missing data (duration, location).
- Rich success/error messaging in CLI.

### MVP (v1.0): AI-driven Mental Health Coaching App

- Multi-platform Email integration (Gmail, Apple Mail via IMAP/SMTP): read, send, and categorize emails.
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
