# Codebase Overview

## 🏗️ Architecture Overview

The ical-chat-proto project is a **conversational calendar assistant** built with Python that integrates with Apple Calendar via EventKit. The system uses LLM-first parsing with GPT-4o for natural language understanding.

### **Core Philosophy**

- **LLM-First**: All command parsing is done by GPT-4o, no rule-based fallbacks
- **Conversational**: Maintains context across multiple turns
- **Proactive**: Learns user patterns and provides intelligent suggestions
- **Test-Driven**: Comprehensive testing with real LLM evaluation

## 📁 Project Structure

```
ical-chat-proto/
├── 📄 main.py                          # Main CLI entry point
├── 📄 openai_client.py                 # LLM integration & command parsing
├── 📄 calendar_agent_eventkit.py       # Apple Calendar integration
├── 📄 core/                            # Core memory & conversation systems
│   ├── conversation_manager.py         # Session memory & context
│   ├── memory_manager.py              # Long-term semantic memory
│   ├── embedding_manager.py           # Event embedding & search
│   ├── narrative_memory.py            # Story-based memory
│   ├── nudge_engine.py                # Proactive suggestions
│   └── types.py                       # Shared data types
├── 📄 utils/                           # Utility modules
│   ├── cli_output.py                  # CLI formatting helpers
│   ├── command_dispatcher.py          # Action routing
│   ├── command_utils.py               # Command parsing utilities
│   └── date_utils.py                  # Date/time utilities
├── 📄 llm_testing/                     # LLM-to-LLM testing framework
│   ├── evaluator.py                   # LLM-based evaluation
│   ├── personas.py                    # Test personas
│   ├── scenarios.py                   # Test scenarios
│   ├── dashboard.py                   # Metrics & alerts
│   ├── meta_tracker.py                # Insights & recommendations
│   └── tests/                         # Testing framework tests
├── 📄 tests/                           # Main test suite
│   ├── test_edge_cases.py             # Edge case testing
│   ├── test_core_integration.py       # Core memory tests
│   └── test_cli_output.py             # CLI formatting tests
├── 📄 cursor-plans/                    # Development planning docs
└── 📄 docs/                           # Documentation
```

## 🔄 Data Flow

### **1. User Input → LLM Parsing**

```
User: "schedule team meeting tomorrow at 2pm"
    ↓
openai_client.py: interpret_command()
    ↓
GPT-4o: Function calling
    ↓
Returns: {"action": "create_event", "details": {...}}
```

### **2. Action Dispatch → Calendar Integration**

```
Command: {"action": "create_event", "details": {...}}
    ↓
utils/command_dispatcher.py: dispatch()
    ↓
calendar_agent_eventkit.py: create_event()
    ↓
EventKit: Save to Apple Calendar
    ↓
Core Memory: Store embedding for future recall
```

### **3. Conversation Context**

```
Session: ConversationState (ephemeral)
    ↓
Multi-turn context: "move it to 3pm" → knows what "it" refers to
    ↓
Long-term: CoreMemory (persistent)
    ↓
Semantic search: "my usual Tuesday meeting" → finds past patterns
```

## 🧠 Core Systems

### **Conversation Manager** (`core/conversation_manager.py`)

- **Purpose**: Maintains session context across turns
- **Key Features**:
  - Context window management (last N turns)
  - Reference resolution ("it", "that meeting")
  - Conversation state persistence within session
- **Usage**: Automatically included in LLM prompts

### **Memory Manager** (`core/memory_manager.py`)

- **Purpose**: Long-term semantic memory for calendar events
- **Key Features**:
  - Event embedding and storage
  - Semantic search for similar past events
  - Pattern recognition and learning
  - Multiple memory types (events, intentions, preferences)
- **Usage**: Powers recall() and proactive suggestions

### **Embedding Manager** (`core/embedding_manager.py`)

- **Purpose**: Creates and stores embeddings for semantic search
- **Key Features**:
  - OpenAI embeddings for event text
  - Vector database storage (ChromaDB)
  - Similarity search for past events
- **Usage**: Backend for memory search functionality

## 🧪 Testing Framework

### **LLM Testing** (`llm_testing/`)

- **Purpose**: Evaluate assistant performance using LLM-based scoring
- **Key Components**:
  - **Personas**: 10 diverse user types (accessibility, challenges)
  - **Scenarios**: 15 test scenarios covering various use cases
  - **Evaluator**: GPT-4 scoring across 8 criteria
  - **Dashboard**: Real-time metrics and alerts
  - **Meta-Tracker**: Insights and recommendations

### **Test Categories**

- **Edge Cases**: Misspellings, poor grammar, invalid dates
- **Integration**: End-to-end CLI → LLM → EventKit testing
- **Core Memory**: Semantic search and pattern recognition
- **Conversation**: Multi-turn context and reference resolution

## 🛠️ Key Modules Deep Dive

### **Main Entry Point** (`main.py`)

```python
# Main loop: User input → LLM parsing → Action dispatch
while True:
    user_input = input("> ")
    interpreted = openai_client.interpret_command(user_input, context)
    dispatch(interpreted["action"], interpreted["details"])
    conversation_state.append_turn(user_input, interpreted["action"])
```

### **LLM Integration** (`openai_client.py`)

```python
# Function calling with GPT-4o
calendar_functions = [
    {"name": "create_event", "description": "Schedule new events"},
    {"name": "delete_event", "description": "Remove events"},
    # ... more functions
]

def interpret_command(user_input, conversation_context=""):
    # Enhanced system prompt with edge case handling
    # Function calling for structured output
    # Error handling and clarification support
```

### **Calendar Integration** (`calendar_agent_eventkit.py`)

```python
class EventKitAgent:
    # Apple Calendar integration via PyObjC
    # Core memory integration for event embedding
    # Narrative memory for pattern recognition

    def create_event(self, details):
        # Save to EventKit
        # Add to Core memory
        # Update narrative patterns
```

### **Command Dispatcher** (`utils/command_dispatcher.py`)

```python
HANDLERS = {
    "create_event": handle_create_event,
    "delete_event": handle_delete_event,
    "move_event": handle_move_event,
    # ... more handlers
}

def dispatch(action: str, details: dict):
    # Route actions to appropriate handlers
    # Use CLI output helpers for consistent formatting
```

## 🎯 Key Features

### **Natural Language Processing**

- **Misspelling Tolerance**: "shedule" → "schedule"
- **Poor Grammar Handling**: "meeting tomorrow at 2pm I need" → extracts intent
- **Ambiguous Date Resolution**: "next Monday" → asks for clarification
- **Context Awareness**: "move it to 3pm" → knows what "it" refers to

### **Proactive Intelligence**

- **Pattern Recognition**: Learns user scheduling patterns
- **Smart Suggestions**: "You usually have team standup on Mondays"
- **Conflict Resolution**: Detects and suggests solutions for scheduling conflicts
- **Contextual Nudging**: Time-based suggestions based on past behavior

### **Memory & Recall**

- **Semantic Search**: "my usual Tuesday meeting" → finds past similar events
- **Preference Learning**: Remembers "no meetings before 11am"
- **Intention Tracking**: "I want to get fitter" → suggests gym time
- **Commitment Management**: "follow up with Anna" → creates reminders

## 🚀 Development Workflow

### **Adding New Features**

1. **Plan**: Add to `cursor-plans/` with detailed specification
2. **Test**: Create comprehensive test suite first
3. **Implement**: Follow TDD with LLM testing integration
4. **Document**: Update API docs and user guides
5. **Review**: Run full test suite and edge case testing

### **Testing Strategy**

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end pipeline testing
- **LLM Tests**: Real LLM evaluation of assistant responses
- **Edge Case Tests**: Comprehensive edge case coverage

### **Code Quality**

- **Type Hints**: Complete type annotations
- **Docstrings**: Comprehensive API documentation
- **Error Handling**: Graceful degradation and helpful messages
- **Performance**: Efficient database queries and memory usage

## 📊 Current Status

### **✅ Completed**

- **Core Calendar Integration**: Full EventKit integration
- **LLM-First Parsing**: GPT-4o function calling
- **Conversation Memory**: Multi-turn context management
- **Core Memory System**: Event embedding and semantic search
- **LLM Testing Framework**: Comprehensive evaluation system
- **Edge Case Handling**: Robust input normalization
- **CLI Output Helpers**: Centralized formatting system

### **🔄 In Progress**

- **Documentation**: API docs and user guides
- **Import Organization**: Standardize imports and add `__all__`
- **Performance Optimization**: Database and algorithm improvements

### **📋 Planned**

- **Notification System**: Email/Slack/webhook integration
- **Advanced Scenarios**: More complex test scenarios
- **CI/CD Integration**: Automated testing and deployment

## 🎯 Quick Start for Development

### **1. Understanding the Flow**

```bash
# Run the assistant
python main.py

# Test edge cases
python -m pytest tests/test_edge_cases.py -v

# Run LLM testing framework
python run_llm_testing_demo.py
```

### **2. Key Files to Know**

- **`main.py`**: Entry point and main loop
- **`openai_client.py`**: LLM integration and command parsing
- **`calendar_agent_eventkit.py`**: Calendar operations
- **`core/memory_manager.py`**: Memory and recall system
- **`llm_testing/evaluator.py`**: Testing framework

### **3. Common Patterns**

- **Adding Commands**: Update `calendar_functions` in `openai_client.py`
- **Adding Handlers**: Add to `HANDLERS` in `utils/command_dispatcher.py`
- **Adding Tests**: Create tests in appropriate `tests/` directory
- **Adding Memory**: Extend `core/memory_manager.py` with new memory types

### **4. Development Tips**

- **Test First**: Always write tests before implementation
- **LLM Testing**: Use the LLM testing framework for new features
- **Documentation**: Update docs as you develop
- **Edge Cases**: Consider misspellings, poor grammar, and invalid inputs

This codebase is designed for rapid iteration and continuous improvement, with comprehensive testing and documentation to support development velocity! 🚀
