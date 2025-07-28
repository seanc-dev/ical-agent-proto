#!/usr/bin/env python3
"""Debug script to test LLM evaluation directly."""

from llm_testing.evaluator import ScoringAgent
from llm_testing.config import TestingConfig
from llm_testing.personas import get_persona
from llm_testing.scenarios import get_all_scenarios
from llm_testing.scenarios import ExpectedBehavior


def test_llm_evaluation():
    """Test LLM evaluation directly."""
    print("🧪 Testing LLM Evaluation Directly")
    print("=" * 40)

    # Initialize
    config = TestingConfig()
    scorer = ScoringAgent(config)

    # Get a simple scenario
    persona = get_persona("Alex")
    scenarios = get_all_scenarios()
    scenario = scenarios[0]  # Use first available scenario

    print(f"Testing: {scenario.name} with {persona.name}")
    print(f"Prompt: {scenario.test_prompts[0].prompt}")

    # Mock assistant response
    assistant_response = "I'll help you set up your morning routine. Let me create a calendar event for your morning routine starting at 7:00 AM tomorrow."

    print(f"Assistant Response: {assistant_response}")

    # Test evaluation
    try:
        result = scorer.evaluate_response(
            scenario, assistant_response, scenario.expected_behaviors
        )

        print(f"\n✅ Evaluation Result:")
        print(f"   Scores: {result.scores}")
        print(f"   Feedback: {result.feedback[:200]}...")
        print(f"   Model: {result.model_version}")
        print(f"   Method: {result.metadata.get('evaluation_method', 'unknown')}")

    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_llm_evaluation()
