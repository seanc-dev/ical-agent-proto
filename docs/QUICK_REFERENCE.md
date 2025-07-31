# Quick Reference Guide

## 🚀 Common Development Tasks

### **Adding a New Command**

1. **Add to LLM Functions** (`openai_client.py`):

```python
calendar_functions = [
    # ... existing functions ...
    {
        "name": "new_command",
        "description": "Description of what this command does",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {"type": "string", "description": "Parameter description"}
            },
            "required": ["param1"]
        }
    }
]
```

2. **Add Handler** (`utils/command_dispatcher.py`):

```python
def handle_new_command(details):
    """Handle the new command."""
    result = new_command_function(details)
    if result.get("success"):
        print(format_success_message(result.get("message")))
    else:
        print(format_error_message(result.get("error")))

# Add to HANDLERS
HANDLERS = {
    # ... existing handlers ...
    "new_command": handle_new_command,
}
```

3. **Add Tests**:

```python
def test_new_command():
    """Test the new command functionality."""
    # Test implementation
```

### **Adding a New Memory Type**

1. **Define Memory Class** (`core/memory_manager.py`):

```python
@dataclass
class NewMemoryType(Memory):
    """New memory type for specific data."""
    field1: str
    field2: int
    # ... additional fields
```

2. **Add to Memory Manager**:

```python
def add_new_memory_type(self, data: Dict) -> str:
    """Add new memory type to storage."""
    memory_id = f"new_type_{datetime.now().timestamp()}"
    memory = NewMemoryType(
        id=memory_id,
        type=MemoryType.NEW_TYPE,
        # ... populate fields
    )
    self.memories[memory_id] = memory
    self._save_memories()
    return memory_id
```

3. **Update Calendar Integration** (`calendar_agent_eventkit.py`):

```python
# Add to relevant calendar operations
if self.core_memory:
    self.core_memory.add_new_memory_type(event_data)
```

### **Adding a New Test Scenario**

1. **Add to Scenarios** (`llm_testing/scenarios.py`):

```python
def get_new_scenario() -> Scenario:
    return Scenario(
        name="New Test Scenario",
        description="Description of what this tests",
        prompt="User prompt to test",
        expected_behaviors=["Expected behavior 1", "Expected behavior 2"],
        category="category_name",
        difficulty="medium"
    )
```

2. **Add to Personas** (`llm_testing/personas.py`):

```python
def get_new_persona() -> Persona:
    return Persona(
        name="New Persona",
        description="Description of persona",
        traits=["trait1", "trait2"],
        accessibility_needs=["need1"],
        communication_style="formal"
    )
```

### **Adding CLI Output Formatting**

1. **Add Function** (`utils/cli_output.py`):

```python
def format_new_output(data: List[Dict[str, Any]]) -> str:
    """
    Format new output type for display.

    Args:
        data: List of data dictionaries

    Returns:
        Formatted string representation
    """
    if not data:
        return "📝 No data found"

    formatted_items = []
    for item in data:
        # Format each item
        formatted_items.append(f"📝 {item.get('title', 'Untitled')}")

    return "\n".join(formatted_items)
```

2. **Add Tests** (`tests/test_cli_output.py`):

```python
def test_format_new_output():
    """Test new output formatting."""
    data = [{"title": "Test Item"}]
    result = format_new_output(data)
    assert "📝 Test Item" in result
```

## 🔧 Common Commands

### **Development**

```bash
# Run the assistant
python main.py

# Run all tests
python -m pytest -v

# Run specific test file
python -m pytest tests/test_edge_cases.py -v

# Run LLM testing framework
python run_llm_testing_demo.py

# Check code style
python -m flake8 .

# Format code
python -m black .
```

### **Testing**

```bash
# Run edge case tests
python -m pytest tests/test_edge_cases.py -v

# Run core integration tests
python -m pytest tests/test_core_integration.py -v

# Run CLI output tests
python -m pytest tests/test_cli_output.py -v

# Run LLM testing framework
python -m pytest llm_testing/tests/ -v
```

### **Git Workflow**

```bash
# Create feature branch
git checkout -b feature/area/description

# Commit changes
git add .
git commit -m "feat: Add new feature"

# Push and create PR
git push -u origin feature/area/description
gh pr create --title "feat: Add new feature" --body "Description"
```

## 📋 Key Functions & Classes

### **Core Functions**

- `interpret_command(user_input, context)`: LLM command parsing
- `dispatch(action, details)`: Action routing
- `create_event(details)`: Calendar event creation
- `delete_event(details)`: Calendar event deletion
- `move_event(details)`: Calendar event rescheduling

### **Memory Functions**

- `CoreMemory.recall(query)`: Semantic search for past events
- `CoreMemory.add_past_event(data)`: Store event in memory
- `ConversationState.append_turn(input, action)`: Add to session context

### **Testing Functions**

- `ScoringAgent.evaluate_response(scenario, response)`: LLM-based evaluation
- `EvaluationLoop.run_batch(scenarios)`: Batch testing
- `MetaTracker.generate_insights(results)`: Generate insights

### **CLI Output Functions**

- `format_events(events)`: Format calendar events
- `format_reminders(reminders)`: Format reminders/tasks
- `format_error_message(error, suggestion)`: Format error messages
- `format_success_message(message)`: Format success messages

## 🐛 Common Issues & Solutions

### **Import Errors**

```bash
# Install dependencies
pip install openai python-dotenv

# Check imports
python -c "from llm_testing import EvaluationLoop"
```

### **OpenAI API Issues**

```bash
# Check API key
echo $OPENAI_API_KEY

# Test API connection
python -c "import openai; print('API available')"
```

### **EventKit Permission Issues**

```bash
# Check calendar access
python -c "from calendar_agent_eventkit import EventKitAgent; print('EventKit available')"
```

### **Test Failures**

```bash
# Run with verbose output
python -m pytest tests/test_specific.py -v -s

# Run single test
python -m pytest tests/test_specific.py::test_function -v
```

## 📊 Performance Monitoring

### **LLM Testing Metrics**

- **Average Score**: Overall performance across scenarios
- **Success Rate**: Percentage of tests passing threshold
- **Persona Performance**: Scores by user type
- **Scenario Performance**: Scores by test category

### **Memory Usage**

- **Database Size**: Check `core/memory.db` size
- **Embedding Count**: Number of stored embeddings
- **Query Performance**: Search response times

### **API Usage**

- **OpenAI Calls**: Monitor API usage and costs
- **Rate Limiting**: Handle API limits gracefully
- **Error Rates**: Track failed API calls

## 🎯 Best Practices

### **Code Style**

- Use type hints for all function parameters
- Add comprehensive docstrings
- Follow PEP 8 formatting
- Use descriptive variable names

### **Testing**

- Write tests before implementation (TDD)
- Test edge cases and error conditions
- Use the LLM testing framework for new features
- Maintain high test coverage

### **Documentation**

- Update docs as you develop
- Add examples to docstrings
- Keep README files current
- Document API changes

### **Error Handling**

- Provide helpful error messages
- Include suggestions for fixes
- Graceful degradation when APIs unavailable
- Comprehensive logging for debugging

This quick reference should help you navigate the codebase efficiently! 🚀
