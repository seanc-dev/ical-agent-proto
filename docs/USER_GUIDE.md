# Calendar Assistant User Guide

## 🚀 Getting Started

### **Installation**

1. **Clone the repository**:

```bash
git clone https://github.com/seanc-dev/ical-agent-proto.git
cd ical-agent-proto
```

2. **Install dependencies**:

```bash
pip install openai python-dotenv
```

3. **Set up environment**:

```bash
cp .env.example .env
# Add your OpenAI API key to .env
echo "OPENAI_API_KEY=your_api_key_here" >> .env
```

4. **Run the assistant**:

```bash
python main.py
```

## 🎯 Basic Usage

### **Starting a Session**

```bash
python main.py
```

You'll see:

```
Welcome to the Terminal Calendar Assistant! Type 'exit' to quit.

>
```

### **Basic Commands**

#### **View Your Calendar**

```
> show my events
> what's on today?
> list my schedule
```

#### **Schedule Events**

```
> schedule team meeting tomorrow at 2pm
> create lunch meeting with John on Friday
> book 30-minute call with client next Tuesday
```

#### **Manage Events**

```
> delete team meeting
> move lunch to 1pm
> reschedule call to next week
```

#### **View Reminders**

```
> show my reminders
> list my tasks
> what do I need to do today?
```

## 🧠 Advanced Features

### **Natural Language Understanding**

The assistant understands natural language and handles:

#### **Misspellings**

```
> shedule meeting tomorrow    # → schedules meeting
> delet team meeting         # → deletes team meeting
> calender events           # → calendar events
```

#### **Poor Grammar**

```
> meeting tomorrow at 2pm I need    # → extracts "meeting tomorrow at 2pm"
> schedule meeting for tomorrow please  # → schedules meeting
> I want to have a meeting          # → schedules meeting
```

#### **Ambiguous References**

```
> schedule team meeting tomorrow
> move it to 3pm                    # → knows "it" refers to the team meeting
```

### **Conversation Context**

The assistant remembers your conversation:

```
> schedule team meeting tomorrow at 10am
✅ Event created successfully

> move it to 2pm
✅ Event moved successfully

> delete that meeting
✅ Event deleted successfully
```

### **Smart Suggestions**

The assistant learns your patterns:

```
> schedule my usual Tuesday check-in
✅ Found similar past event: "Weekly Check-in with Boss" (Tuesdays at 10am)
✅ Event created successfully
```

## 📅 Calendar Operations

### **Creating Events**

#### **Basic Event Creation**

```
> schedule team meeting tomorrow at 2pm
```

#### **With Duration**

```
> schedule 30-minute standup tomorrow at 9am
> create 2-hour project review on Friday
```

#### **With Location**

```
> schedule meeting in conference room A tomorrow
> create lunch at the office cafeteria
```

#### **With Attendees**

```
> schedule meeting with John and Sarah tomorrow
> create team sync with engineering team
```

#### **Recurring Events**

```
> schedule daily standup every weekday at 9am
> create weekly team meeting every Monday
> schedule monthly review on the first Friday
```

### **Managing Events**

#### **Moving Events**

```
> move team meeting to 3pm
> reschedule lunch to tomorrow
> shift call to next week
```

#### **Deleting Events**

```
> delete team meeting
> cancel lunch
> remove that meeting
```

#### **Finding Events**

```
> show my meetings today
> list events for tomorrow
> what's on my calendar this week?
```

### **Reminders and Tasks**

#### **Viewing Reminders**

```
> show my reminders
> list my tasks
> what do I need to do?
```

#### **Creating Reminders**

```
> remind me to call John tomorrow
> add task to review budget
> create reminder to follow up with client
```

## 🎯 Pro Tips

### **Time References**

The assistant understands various time formats:

#### **Relative Times**

```
> tomorrow
> next week
> in 3 days
> this weekend
```

#### **Specific Times**

```
> 2pm
> 14:00
> noon
> midnight
```

#### **Date Formats**

```
> January 15th
> 2024-01-15
> next Monday
> this Friday
```

### **Natural Language Patterns**

#### **Intent Recognition**

```
> I need to schedule a meeting
> Can you book a call?
> Please create an event
> Set up a meeting
```

#### **Context Awareness**

```
> schedule meeting with the team
> move it to next week
> delete that meeting
> reschedule to 3pm
```

### **Error Handling**

The assistant provides helpful feedback:

#### **Invalid Dates**

```
> schedule meeting on 2024-13-45
❌ Error: Invalid date format
💡 Suggestion: Use YYYY-MM-DD format
```

#### **Ambiguous Requests**

```
> schedule meeting next Monday
🤔 Which Monday? (Today is Monday)
📝 Context: There are multiple Mondays this month
```

#### **Missing Information**

```
> schedule meeting
🤔 What type of meeting would you like to schedule?
📝 Context: Need more details about the meeting
```

## 🔧 Configuration

### **Environment Variables**

Create a `.env` file with:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
CALENDAR_NAME=your_calendar_name
```

### **Calendar Selection**

If you have multiple calendars, specify which one to use:

```bash
export CALENDAR_NAME="Work Calendar"
python main.py
```

## 🧪 Testing

### **Run Tests**

```bash
# Run all tests
python -m pytest -v

# Run specific test categories
python -m pytest tests/test_edge_cases.py -v
python -m pytest tests/test_core_integration.py -v
```

### **LLM Testing Framework**

```bash
# Run the LLM testing demo
python run_llm_testing_demo.py

# Run specific test scenarios
python -c "from llm_testing import EvaluationLoop; print('Framework loaded')"
```

## 🐛 Troubleshooting

### **Common Issues**

#### **OpenAI API Errors**

```
❌ Error: OpenAI API not available
💡 Suggestion: Please check your API key configuration
```

**Solution**: Check your `.env` file and ensure `OPENAI_API_KEY` is set correctly.

#### **Calendar Permission Issues**

```
❌ Error: Calendar access denied
💡 Suggestion: Check calendar permissions in System Preferences
```

**Solution**: Go to System Preferences → Security & Privacy → Privacy → Calendar and ensure the application has access.

#### **Import Errors**

```
ModuleNotFoundError: No module named 'openai'
```

**Solution**: Install dependencies:

```bash
pip install openai python-dotenv
```

### **Debug Mode**

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### **Verbose Output**

Run with verbose output to see detailed information:

```bash
python main.py --verbose
```

## 📊 Performance Tips

### **Optimizing Response Time**

1. **Use specific commands**: "schedule meeting tomorrow at 2pm" vs "schedule meeting"
2. **Provide context**: "move team meeting to 3pm" vs "move it to 3pm"
3. **Use clear language**: Avoid ambiguous references

### **Memory Usage**

The assistant stores:

- **Session context**: Last 10 conversation turns
- **Event embeddings**: For semantic search
- **User preferences**: Learned patterns and preferences

### **API Usage**

Monitor your OpenAI API usage:

- Each command uses 1-2 API calls
- Complex requests may use more calls
- Set up usage alerts in your OpenAI dashboard

## 🎯 Best Practices

### **Effective Communication**

1. **Be specific**: "schedule 30-minute team meeting tomorrow at 2pm"
2. **Use natural language**: "move my lunch to 1pm"
3. **Provide context**: "reschedule the team meeting to next week"

### **Calendar Management**

1. **Regular cleanup**: Delete old events and reminders
2. **Use consistent naming**: "Team Standup" vs "standup" vs "team meeting"
3. **Add details**: Include location, attendees, and description

### **Privacy and Security**

1. **Local storage**: All data is stored locally
2. **API security**: Use environment variables for API keys
3. **Calendar permissions**: Only grant necessary calendar access

## 🚀 Advanced Features

### **Core Memory Integration**

The assistant learns from your calendar usage:

```
> schedule my usual Tuesday check-in
✅ Found similar past event: "Weekly Check-in with Boss" (Tuesdays at 10am)
✅ Event created successfully
```

### **Pattern Recognition**

The assistant recognizes patterns:

```
> schedule team meeting
🤔 You usually have team meetings on Mondays at 10am. Should I schedule it then?
```

### **Proactive Suggestions**

The assistant can suggest actions:

```
> I have a gap at 3pm today
💡 Would you like me to schedule that project review we discussed?
```

## 📞 Support

### **Getting Help**

1. **Check the documentation**: Review this guide and the codebase overview
2. **Run tests**: Ensure everything is working correctly
3. **Check logs**: Look for error messages and debug information
4. **Report issues**: Create an issue on GitHub with detailed information

### **Contributing**

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-feature`
3. **Make changes**: Follow the development guidelines
4. **Add tests**: Ensure new features are well-tested
5. **Submit a PR**: Create a pull request with detailed description

### **Development Setup**

See the [Codebase Overview](CODEBASE_OVERVIEW.md) and [Quick Reference](QUICK_REFERENCE.md) for development information.

---

**Happy scheduling! 🎉**

The calendar assistant is designed to make your life easier with intelligent, conversational calendar management. Feel free to experiment with natural language commands and discover new ways to interact with your calendar!
