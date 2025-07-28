#!/usr/bin/env python3
"""Demo script to run the LLM testing framework and see real feedback."""

import os
import sys
from datetime import datetime
from llm_testing import EvaluationLoop, TestingConfig
from llm_testing.personas import get_all_personas
from llm_testing.scenarios import get_all_scenarios
from llm_testing.database import ResultsDatabase
from llm_testing.dashboard import Dashboard


def main():
    """Run the LLM testing framework demo."""
    print("🚀 LLM Testing Framework Demo")
    print("=" * 50)

    # Check if OpenAI is available
    try:
        from openai_client import client

        if client is None:
            print("⚠️  OpenAI client not available. Using placeholder evaluations.")
        else:
            print("✅ OpenAI client available. Running real LLM evaluations!")
    except ImportError:
        print("⚠️  OpenAI client not available. Using placeholder evaluations.")

    # Initialize the framework
    print("\n📋 Initializing LLM Testing Framework...")
    config = TestingConfig()

    # Create scoring agent
    from llm_testing.evaluator import ScoringAgent

    scoring_agent = ScoringAgent(config)

    # Create assistant client (we'll use None for now, the evaluator handles this)
    assistant_client = None

    evaluator = EvaluationLoop(assistant_client, scoring_agent, config)

    # Get personas and scenarios
    personas = get_all_personas()
    scenarios = get_all_scenarios()

    print(f"👥 Loaded {len(personas)} personas:")
    for persona in personas[:3]:  # Show first 3
        print(f"  - {persona.name}: {', '.join(persona.traits[:2])}")
    if len(personas) > 3:
        print(f"  ... and {len(personas) - 3} more")

    print(f"\n🎯 Loaded {len(scenarios)} scenarios:")
    for scenario in scenarios[:3]:  # Show first 3
        print(f"  - {scenario.name}: {scenario.category} ({scenario.difficulty})")
    if len(scenarios) > 3:
        print(f"  ... and {len(scenarios) - 3} more")

    # Run a small batch of tests
    print("\n🧪 Running evaluation batch...")
    test_scenarios = scenarios[:3]  # Test with first 3 scenarios

    start_time = datetime.now()
    batch_result = evaluator.run_batch(test_scenarios)
    end_time = datetime.now()

    duration = (end_time - start_time).total_seconds()
    print(f"⏱️  Evaluation completed in {duration:.2f} seconds")

    # Show results
    print("\n📊 Evaluation Results:")
    print("-" * 30)

    for result in batch_result.results:
        print(f"\n🎭 {result.persona_name} - {result.scenario_name}")
        print(f"   Overall Score: {max(result.scores.values()):.2f}/5.0")
        print(f"   Feedback: {result.feedback[:100]}...")

        # Show individual scores
        for criterion, score in result.scores.items():
            print(f"   {criterion.capitalize()}: {score:.1f}/5.0")

    # Show batch summary
    print(f"\n📈 Batch Summary:")
    print(f"   Total Tests: {len(batch_result.results)}")
    print(f"   Average Score: {batch_result.summary['average_score']:.2f}/5.0")
    print(f"   Success Rate: {batch_result.summary['success_rate']:.1%}")

    # Show insights
    print(f"\n💡 Insights:")
    for insight in batch_result.insights:
        print(f"   • {insight}")

    # Show recommendations
    print(f"\n🎯 Recommendations:")
    for rec in batch_result.summary.get("recommendations", []):
        print(f"   • {rec}")

    # Show alerts
    if batch_result.performance_alerts:
        print(f"\n🚨 Performance Alerts:")
        for alert in batch_result.performance_alerts:
            print(f"   ⚠️  {alert}")

    # Show database status
    print(f"\n💾 Database Status:")
    db = ResultsDatabase()
    recent_results = db.get_recent_results(limit=5)
    print(f"   Recent Results: {len(recent_results)} stored")

    # Show dashboard metrics
    print(f"\n📊 Dashboard Metrics:")
    dashboard = Dashboard(db, config.alert_threshold)
    metrics = dashboard.get_key_metrics()
    print(f"   Overall Performance: {metrics.get('overall_score', 'N/A')}")
    print(f"   Test Count: {metrics.get('total_tests', 'N/A')}")
    print(f"   Success Rate: {metrics.get('success_rate', 'N/A')}")

    print(f"\n🎉 Demo completed! Check the database for detailed results.")
    print(f"Database location: {os.path.abspath('llm_testing/results.db')}")


if __name__ == "__main__":
    main()
