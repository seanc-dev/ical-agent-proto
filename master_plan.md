# Master Plan: Conversational Calendar Assistant

## Vision

Build a truly conversational calendar assistant that feels like talking to a real human assistant who takes as much load off your hands as you want, and adapts to your way of working. The experience should be seamless, contextual, and human-like.

## Development Strategy: Python-First Rapid Prototyping

**Build everything in Python first** to rapidly iterate on functionality before moving to Swift. This allows us to:

- Test complex features quickly
- Validate user experience patterns
- Iterate on conversational flows
- Perfect the LLM interactions
- Build a solid foundation before native implementation

## Completed Work ✅

- ✅ End-to-end CLI tests with full pipeline testing (CLI → LLM → EventKit)
- ✅ LLM-first edge case handling with timeout and clarification support
- ✅ Pure LLM-driven parsing (no rule-based fallbacks)
- ✅ Comprehensive edge case test suite
- ✅ Enhanced system prompts for misspellings, poor grammar, and ambiguous requests

## Prototype (v0.x): Conversational Calendar Assistant

### Core Functionality

- ✅ Natural language calendar management
- ✅ LLM-driven command interpretation
- ✅ EventKit integration
- ✅ Edge case handling with clarification

### Conversational Context & UX Improvements

#### Context Awareness

- **Conversation Memory**: Remember previous commands and context within session
- **User Preferences**: Learn and adapt to user's scheduling patterns and preferences
- **Contextual Suggestions**: "You usually have team standup on Mondays at 10am, should I schedule that?"
- **Follow-up Handling**: "Move it to 2pm" (knows what "it" refers to from previous command)

#### Human-Like Interaction

- **Proactive Suggestions**: "I notice you have a gap at 3pm, would you like me to schedule that project review we discussed?"
- **Adaptive Responses**: Match user's communication style (formal vs casual)
- **Emotional Intelligence**: Recognize stress levels and adjust assistance accordingly
- **Natural Language**: "I'm swamped today" → "Let me help you prioritize and reschedule some meetings"

#### Workflow Adaptation

- **Learning Patterns**: "You always schedule 1:1s on Fridays, should I suggest that?"
- **Work Style Matching**: Adapt to whether user prefers detailed planning or quick scheduling
- **Context Switching**: Handle interruptions and return to previous tasks seamlessly
- **Multi-step Conversations**: "Schedule the meeting, then remind me to prepare the agenda"

#### Intelligent Assistance

- **Conflict Resolution**: "You have a conflict with the 3pm meeting. Should I reschedule it or the new one?"
- **Smart Defaults**: "You usually have 30-minute meetings, is that good for this one?"
- **Proactive Management**: "I see you have 5 meetings back-to-back. Would you like me to add some buffer time?"
- **Contextual Help**: "I can help you with that. Would you like me to show you your availability first?"

### Edge Case Handling & Robustness

#### Input Normalization (LLM handles)

- ✅ Misspellings: "shedule" → "schedule"
- ✅ Poor grammar: Extract core intent
- ✅ Mixed case/whitespace: Normalize automatically
- ✅ Punctuation: Handle gracefully

#### Date/Time Robustness (LLM clarifies)

- ✅ Invalid dates: Detect and explain issues
- ✅ Ambiguous dates: "next Monday" when today is Monday
- ✅ Relative dates: "in 3 days", "this weekend"
- ✅ Time ambiguity: "noon" vs "12pm", "lunch time"

#### Event Management (LLM asks)

- ✅ Event not found: Provide helpful alternatives
- ✅ Multiple matches: List options for clarification
- ✅ Duplicate events: Detect and ask for confirmation
- ✅ Recurring events: Handle series vs single occurrence

#### Natural Language (LLM adapts)

- ✅ Vague requests: Ask for clarification
- ✅ Context dependencies: Maintain conversation context
- ✅ Complex requests: Break down multi-step operations
- ✅ Conditional logic: "if I'm free tomorrow, schedule meeting"

#### System Resilience

- ✅ API timeouts: Graceful handling with retry logic
- ✅ Rate limiting: Intelligent backoff strategies
- ✅ Network issues: Offline mode with sync when available
- ✅ Performance: Handle large calendars efficiently

### New Features to Add

#### Event Management

- **Event Copying**: "copy team meeting to next week"
- **Bulk Operations**: "delete all meetings this week" (with confirmation)
- **Event Templates**: "schedule a 1:1 meeting" (predefined templates)
- **Attendee Management**: "invite john@email.com to the meeting"

#### Advanced Scheduling

- **Availability Checking**: "if I'm free tomorrow at 2pm, schedule the meeting"
- **Conflict Resolution**: "find a time that works for both of us"
- **Recurring Patterns**: "schedule daily standup every weekday at 9am"
- **Travel Time**: "schedule meeting at the office, accounting for 30min travel time"

#### Search & Discovery

- **Fuzzy Search**: "find meetings about project X"
- **Attendee Filtering**: "show meetings with John"
- **Date Range Queries**: "what meetings do I have next week?"
- **Content Search**: "find meetings where we discussed the budget"

#### Smart Features

- **Undo Operations**: "undo my last action"
- **Action History**: "what did I just schedule?"
- **Confirmation Dialogs**: "are you sure you want to delete all meetings?"
- **Smart Suggestions**: "you usually have lunch at noon, should I block that time?"

### Email Integration (Moved from MVP)

#### Multi-platform Email Support

- **Gmail Integration**: Read, send, categorize emails
- **Apple Mail**: Native macOS integration
- **IMAP/SMTP**: Generic email protocol support
- **Email-to-Calendar**: Convert email threads to calendar events

#### Smart Email Features

- **Email Parsing**: Extract meeting details from emails
- **Auto-scheduling**: "schedule a meeting based on this email thread"
- **Email Summaries**: "summarize my emails and suggest calendar actions"
- **Follow-up Tracking**: "remind me to follow up on this email next week"

### Checklist/Note Storage

#### Persistent Context

- **Checklist Storage**: "I have 5 things to do and want the assistant to remember them"
- **Context-Aware Conversations**: "add 'review budget' to my checklist"
- **Smart Suggestions**: "you mentioned wanting to review the budget, should I schedule time for that?"
- **Integration**: Connect checklists with calendar events

#### Note Management

- **Meeting Notes**: "take notes during the team meeting"
- **Action Items**: "extract action items from this meeting"
- **Follow-up Tracking**: "remind me to check on the project status next week"
- **Context Preservation**: "what did we discuss in last week's meeting?"

### Core Integration — Phase One

Core is the inference layer that turns a reactive assistant into a proactive, intelligent agent. It gives the MVP semantic memory, narrative awareness, and long-term recall by embedding and indexing life data — starting with calendar events, later expanding to reminders, email, and conversations.

#### ✅ Current Status

- **Working Apple Calendar integration** with full conversational control
- **EventKit + GPT-4o pipeline** live
- **Prototype driven by tests**
- **Cursor auto-mode** in place
- **Embedding tech** not yet implemented but central to the vision

#### 🔜 Phase One Goals

1. **Create First Embedding Index**

   - Extract titles + descriptions from past calendar events
   - Embed using OpenAI or similar
   - Store locally in JSON or a vector DB like ChromaDB

2. **Implement recall() Function**

   - Enable semantic search for similar past events
   - Use in commands like: "Schedule my usual Tuesday check-in with B"

3. **Contextual Nudging**

   - Add logic to suggest likely next actions
   - Example: "You usually check email around this time — want me to open it?"

4. **Structured Memory Types**
   - Define types of memory Core will hold:
     - **Past Events** (calendar, reminders, emails)
     - **Intentions** (e.g. "I want to get fitter")
     - **Commitments** (e.g. "follow up with Anna")
     - **Preferences** (e.g. "no meetings before 11am")
   - Draft a JSON schema or begin logging from tests and user inputs

### Advanced Conversational Features

#### Multi-modal Interaction

- **Voice Input**: "hey assistant, schedule a meeting"
- **Voice Output**: "I've scheduled your meeting for tomorrow at 2pm"
- **Image Recognition**: "schedule a meeting based on this screenshot of my calendar"
- **Document Parsing**: "create calendar events from this PDF agenda"

#### Intelligent Automation

- **Workflow Automation**: "when I get a meeting invite, automatically check my availability"
- **Smart Routing**: "forward calendar conflicts to my assistant"
- **Proactive Alerts**: "warn me if I have too many meetings in a day"
- **Auto-optimization**: "suggest a better schedule for my week"

#### Personalization

- **Learning Preferences**: Adapt to user's communication style and work patterns
- **Custom Commands**: "when I say 'busy day', show me my schedule and suggest breaks"
- **Contextual Shortcuts**: "my usual" for frequently used scheduling patterns
- **Work Style Adaptation**: Match user's planning vs spontaneous scheduling style

## MVP (v1.0): Production-Ready Calendar Assistant

### Core Requirements

- Native Swift implementation
- macOS app with system integration
- Offline capability with sync
- Enterprise security and compliance
- Performance optimization for large calendars

### Advanced Features

- Team collaboration and shared calendars
- Advanced analytics and insights
- Integration with enterprise tools
- Mobile companion app
- API for third-party integrations

## Success Metrics

### User Experience

- **Conversation Quality**: > 90% of interactions feel natural and helpful
- **Context Retention**: Remember user preferences and patterns accurately
- **Error Recovery**: Graceful handling of misunderstandings
- **Proactive Assistance**: Anticipate user needs and offer helpful suggestions

### Technical Performance

- **Response Time**: < 2 seconds for most interactions
- **Accuracy**: > 95% correct interpretation of user intent
- **Reliability**: 99.9% uptime with graceful degradation
- **Scalability**: Handle thousands of events efficiently

### Business Impact

- **Time Savings**: Reduce calendar management time by 50%
- **User Satisfaction**: > 4.5/5 rating for conversational experience
- **Adoption Rate**: > 80% of users use conversational features daily
- **Productivity**: Measurable improvement in scheduling efficiency

## Implementation Timeline

### Phase 1: Core Conversational Features (Current)

- ✅ LLM-first edge case handling
- 🔄 Conversational context and memory
- 🔄 Human-like interaction patterns
- 🔄 Workflow adaptation

### Phase 2: Advanced Features (Next)

- 🔄 Event copying and bulk operations
- 🔄 Smart scheduling and conflict resolution
- 🔄 Search and discovery features
- 🔄 Email integration

### Phase 3: Intelligence & Automation (Future)

- 🔄 Proactive assistance and suggestions
- 🔄 Workflow automation
- 🔄 Multi-modal interaction
- 🔄 Advanced personalization

### Phase 4: Production Readiness (Final)

- 🔄 Native Swift implementation
- 🔄 Enterprise features and security
- 🔄 Performance optimization
- 🔄 Mobile companion app

This roadmap ensures we build a truly conversational, human-like calendar assistant that adapts to each user's unique way of working.
