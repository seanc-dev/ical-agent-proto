# LLM-to-LLM Testing Framework

## Overview

The LLM-to-LLM Testing Framework is a comprehensive system for evaluating AI assistant performance using synthetic personas and real LLM-based scoring. It provides objective, data-driven insights into how well calendar assistants perform across diverse user types and scenarios.

## 🎯 Key Features

- **Real LLM Evaluation**: Uses GPT-4 to score assistant responses across multiple criteria
- **Diverse Personas**: 10 personas including accessibility and challenge types
- **Comprehensive Scenarios**: 15 scenarios covering various use cases
- **SQLite Database**: Persistent storage of results and insights
- **Real-time Dashboard**: Metrics and alert system
- **Bias Detection**: Comprehensive analysis of evaluation fairness
- **Trend Analysis**: Performance tracking over time

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install openai python-dotenv

# Set up environment
cp .env.example .env
# Add your OpenAI API key to .env
```

### Basic Usage

```python
from llm_testing import EvaluationLoop, TestingConfig
from llm_testing.evaluator import ScoringAgent

# Initialize framework
config = TestingConfig()
scoring_agent = ScoringAgent(config)
evaluator = EvaluationLoop(None, scoring_agent, config)

# Run evaluation
scenarios = get_all_scenarios()[:3]  # Test first 3 scenarios
results = evaluator.run_batch(scenarios)

# View results
for result in results.results:
    print(f"{result.persona_name} - {result.scenario_name}: {max(result.scores.values()):.2f}/5.0")
```

### Demo Script

```bash
python run_llm_testing_demo.py
```

## 📊 Architecture

### Core Components

1. **Personas Module** (`llm_testing/personas.py`)

   - 10 diverse user personas
   - Accessibility and challenge types
   - Configurable traits and behaviors

2. **Scenarios Module** (`llm_testing/scenarios.py`)

   - 15 comprehensive test scenarios
   - Ground truth anchors
   - Difficulty levels and categories

3. **Evaluator Module** (`llm_testing/evaluator.py`)

   - Real LLM-based scoring
   - Bias detection
   - Detailed feedback generation

4. **Database Module** (`llm_testing/database.py`)

   - SQLite storage
   - Results and insights tracking
   - Performance metrics

5. **Dashboard Module** (`llm_testing/dashboard.py`)
   - Real-time metrics
   - Alert system
   - Trend analysis

## 👥 Personas

### Standard Personas

- **Alex**: Busy executive, tech-savvy, efficiency-focused
- **Sam**: Creative professional, flexible schedule, work-life balance
- **Jordan**: Graduate student, budget-conscious, academic focus

### Accessibility Personas

- **Morgan**: Screen reader user, visual impairments
- **Riley**: Motor control challenges, voice commands

### Challenge Personas

- **Casey**: Tech-savvy power user
- **Taylor**: Minimalist user, prefers simplicity
- **Parker**: Remote worker, timezone challenges
- **Quinn**: Student, academic scheduling
- **Avery**: Small business owner, complex scheduling

## 🎯 Scenarios

### Categories

- **Basic Scheduling**: Simple event creation and management
- **Optimization**: Complex scheduling and efficiency
- **Accessibility**: Screen reader and voice command support
- **Timezone**: International and travel scenarios
- **Error Handling**: Invalid inputs and edge cases

### Examples

- **Morning Routine Setup**: Establish consistent morning schedule
- **Travel Planning**: Handle timezone changes and travel
- **Family Coordination**: Complex multi-person scheduling
- **Study Schedule Optimization**: Academic planning
- **Creative Flow Maintenance**: Creative professional scheduling

## 📈 Evaluation Criteria

### Scoring Rubric (1-5 scale)

- **Clarity** (20%): How clear and understandable is the response?
- **Helpfulness** (25%): Does the response address the user's needs?
- **Efficiency** (15%): Is the response concise and actionable?
- **Accuracy** (20%): Are the suggestions and information correct?
- **Persona Alignment** (10%): Does the response match the persona's style?
- **Goal Achievement** (10%): Does the response advance the user's goals?

### Additional Criteria

- **Accessibility** (10%): How well does it accommodate accessibility needs?
- **Error Handling** (10%): How gracefully does it handle invalid inputs?

## 🗄️ Database Schema

### Tables

- `evaluation_results`: Individual test results with scores and metadata
- `batch_results`: Batch performance and insights
- `performance_metrics`: Trends over time
- `insights`: Actionable recommendations

### Key Fields

- `scenario_name`, `persona_name`, `prompt`
- `assistant_response`, `scores`, `feedback`
- `timestamp`, `code_version`, `model_version`
- `metadata` (JSON): Evaluation method, bias detection, etc.

## 📊 Dashboard Metrics

### Key Metrics

- **Overall Score**: Weighted average across all criteria
- **Success Rate**: Percentage meeting threshold scores
- **Persona Performance**: Scores by persona type
- **Scenario Performance**: Performance by category
- **Trend Analysis**: Performance changes over time

### Alerts

- Performance below thresholds
- Regression detection
- Accessibility support issues
- Recommendation generation

## 🔧 Configuration

### TestingConfig Options

```python
config = TestingConfig(
    primary_model="gpt-4",
    fallback_model="gpt-3.5-turbo",
    alert_threshold=3.5,
    low_stakes_threshold=4.0,
    results_storage="llm_testing/results.db"
)
```

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `CALENDAR_NAME`: Calendar name for testing

## 🧪 Testing

### Run All Tests

```bash
python -m pytest llm_testing/tests/ -v
```

### Test Categories

- **Unit Tests**: Individual component testing
- **Integration Tests**: Full pipeline testing
- **Database Tests**: Storage and retrieval
- **Dashboard Tests**: Metrics and alerts

### Test Coverage

- 50+ passing tests
- All core components covered
- Real LLM integration tested
- Database functionality verified

## 📝 API Reference

### Main Classes

#### EvaluationLoop

```python
class EvaluationLoop:
    def __init__(self, assistant_client, scoring_agent, config)
    def run_scenario(self, scenario: Scenario) -> ScenarioResult
    def run_batch(self, scenarios: List[Scenario]) -> BatchResult
    def generate_report(self, results: BatchResult) -> EvaluationReport
```

#### ScoringAgent

```python
class ScoringAgent:
    def __init__(self, config: TestingConfig)
    def evaluate_response(self, scenario, assistant_response, expected_behaviors) -> EvaluationResult
    def _detect_bias(self, response: str, scores: Dict[str, float]) -> Dict[str, Any]
```

#### ResultsDatabase

```python
class ResultsDatabase:
    def __init__(self, db_path: str = "llm_testing/results.db")
    def store_evaluation_result(self, result: EvaluationResult)
    def get_recent_results(self, limit: int = 10) -> List[EvaluationResult]
    def get_performance_trends(self) -> Dict[str, Any]
```

#### Dashboard

```python
class Dashboard:
    def __init__(self, db: ResultsDatabase, alert_threshold: float)
    def get_key_metrics(self) -> Dict[str, Any]
    def get_scenario_performance(self) -> Dict[str, Any]
    def get_alert_summary(self) -> Dict[str, Any]
```

## 🎨 Usage Examples

### Basic Evaluation

```python
from llm_testing import EvaluationLoop, TestingConfig
from llm_testing.evaluator import ScoringAgent

# Setup
config = TestingConfig()
scorer = ScoringAgent(config)
evaluator = EvaluationLoop(None, scorer, config)

# Run single scenario
scenario = get_scenario("Morning Routine Setup")
result = evaluator.run_scenario(scenario)
print(f"Score: {max(result.results[0].scores.values()):.2f}/5.0")
```

### Batch Evaluation

```python
# Run multiple scenarios
scenarios = get_all_scenarios()[:5]
batch_result = evaluator.run_batch(scenarios)

# Analyze results
print(f"Average Score: {batch_result.summary['average_score']:.2f}")
print(f"Success Rate: {batch_result.summary['success_rate']:.1%}")
```

### Database Queries

```python
from llm_testing.database import ResultsDatabase

db = ResultsDatabase()
recent_results = db.get_recent_results(limit=10)
trends = db.get_performance_trends()

for result in recent_results:
    print(f"{result.persona_name}: {max(result.scores.values()):.2f}")
```

### Dashboard Analysis

```python
from llm_testing.dashboard import Dashboard

dashboard = Dashboard(db, config.alert_threshold)
metrics = dashboard.get_key_metrics()
alerts = dashboard.get_alert_summary()

print(f"Overall Performance: {metrics['overall_score']}")
print(f"Active Alerts: {len(alerts['alerts'])}")
```

## 🔮 Advanced Features

### Custom Personas

```python
from llm_testing.personas import Persona

custom_persona = Persona(
    name="CustomUser",
    traits=["custom trait"],
    goals=["custom goal"],
    behaviors=["custom behavior"],
    communication_style="direct",
    tech_savviness=4,
    # ... other fields
)
```

### Custom Scenarios

```python
from llm_testing.scenarios import Scenario, TestPrompt, ExpectedBehavior

custom_scenario = Scenario(
    name="Custom Scenario",
    category="custom",
    difficulty="medium",
    goals=["custom goal"],
    test_prompts=[TestPrompt("Custom prompt")],
    expected_behaviors=[ExpectedBehavior("Custom behavior")],
    persona=get_persona("Alex")
)
```

### Bias Detection

```python
# The framework automatically detects bias in evaluations
result = scorer.evaluate_response(scenario, response, behaviors)
bias_info = result.metadata.get("bias_detected", False)
confidence = result.metadata.get("confidence", 0.0)
```

## 🚨 Troubleshooting

### Common Issues

#### OpenAI API Errors

```bash
# Check API key
echo $OPENAI_API_KEY

# Test connection
python -c "from openai_client import client; print('Available:', client is not None)"
```

#### Database Issues

```bash
# Check database
ls -la llm_testing/results.db

# Reset database
rm llm_testing/results.db
python llm_testing/create_database.py
```

#### Import Errors

```bash
# Install dependencies
pip install openai python-dotenv

# Check imports
python -c "from llm_testing import EvaluationLoop"
```

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug info
python debug_llm_evaluation.py
```

## 📈 Performance Optimization

### Tips

- Use `fallback_model` for less critical evaluations
- Batch evaluations for efficiency
- Cache results to avoid duplicate API calls
- Monitor API usage and costs

### Configuration

```python
config = TestingConfig(
    primary_model="gpt-4",      # High-quality evaluation
    fallback_model="gpt-3.5-turbo",  # Cost-effective
    alert_threshold=3.5,         # Performance threshold
    low_stakes_threshold=4.0     # When to use fallback
)
```

## 🤝 Contributing

### Development Setup

```bash
# Clone repository
git clone <repository>
cd ical-chat-proto

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest llm_testing/tests/ -v
```

### Adding New Features

1. Create feature branch: `git checkout -b feature/llm-testing/new-feature`
2. Add tests in `llm_testing/tests/`
3. Update documentation
4. Submit pull request

### Code Style

- Follow PEP 8
- Add type hints
- Include docstrings
- Write comprehensive tests

## 📄 License

This project is part of the ical-chat-proto repository.

## 🆘 Support

For issues and questions:

1. Check the troubleshooting section
2. Review existing issues
3. Create a new issue with detailed information
4. Include error messages and environment details
