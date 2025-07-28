#!/usr/bin/env python3
"""Demo script to show the Meta-Tracker functionality in action."""

import uuid
from datetime import datetime
from llm_testing import TestingConfig
from llm_testing.meta_tracker import MetaTracker
from llm_testing.insights_database import Insight


def demo_meta_tracker():
    """Demonstrate the Meta-Tracker functionality."""
    print("🔍 Meta-Tracker Demo")
    print("=" * 50)

    # Initialize the meta-tracker
    config = TestingConfig()
    meta_tracker = MetaTracker(config)

    print("✅ Meta-Tracker initialized with InsightsDatabase")

    # Create some sample insights
    insights = [
        Insight(
            insight_id=str(uuid.uuid4()),
            insight_type="performance",
            description="Alex persona shows consistently high scores in basic scheduling scenarios",
            confidence=0.85,
            severity="medium",
            category="persona",
            code_version="0.1.0",
            timestamp=datetime.now().isoformat(),
            metadata={
                "persona": "Alex",
                "scenarios": ["Morning Routine Setup", "Travel Planning"],
                "average_score": 4.2,
                "test_count": 5,
            },
            linked_issues=[],
            linked_insights=[],
        ),
        Insight(
            insight_id=str(uuid.uuid4()),
            insight_type="accessibility",
            description="Morgan persona struggles with complex scheduling scenarios",
            confidence=0.92,
            severity="high",
            category="persona",
            code_version="0.1.0",
            timestamp=datetime.now().isoformat(),
            metadata={
                "persona": "Morgan",
                "scenarios": ["Family Coordination", "Study Schedule Optimization"],
                "average_score": 2.8,
                "test_count": 3,
                "accessibility_issues": ["screen_reader", "complex_ui"],
            },
            linked_issues=["issue-123"],
            linked_insights=[],
        ),
        Insight(
            insight_id=str(uuid.uuid4()),
            insight_type="regression",
            description="Performance regression detected in timezone handling scenarios",
            confidence=0.78,
            severity="high",
            category="scenario",
            code_version="0.1.0",
            timestamp=datetime.now().isoformat(),
            metadata={
                "scenario": "Travel Planning",
                "previous_score": 4.1,
                "current_score": 3.2,
                "regression_percentage": 22.0,
            },
            linked_issues=["issue-456"],
            linked_insights=[],
        ),
        Insight(
            insight_id=str(uuid.uuid4()),
            insight_type="improvement",
            description="Error handling significantly improved across all personas",
            confidence=0.88,
            severity="low",
            category="system",
            code_version="0.1.0",
            timestamp=datetime.now().isoformat(),
            metadata={
                "improvement_area": "error_handling",
                "previous_score": 2.5,
                "current_score": 4.1,
                "improvement_percentage": 64.0,
            },
            linked_issues=[],
            linked_insights=[],
        ),
    ]

    print(f"\n📊 Creating {len(insights)} sample insights...")

    # Track each insight
    for insight in insights:
        meta_tracker.track_insight(insight)

    print("\n✅ All insights tracked successfully!")

    # Demonstrate retrieval by type
    print("\n🔍 Retrieving insights by type:")
    performance_insights = meta_tracker.get_insights_by_type("performance")
    accessibility_insights = meta_tracker.get_insights_by_type("accessibility")
    regression_insights = meta_tracker.get_insights_by_type("regression")

    print(f"   Performance insights: {len(performance_insights)}")
    print(f"   Accessibility insights: {len(accessibility_insights)}")
    print(f"   Regression insights: {len(regression_insights)}")

    # Demonstrate retrieval by category
    print("\n📂 Retrieving insights by category:")
    persona_insights = meta_tracker.get_insights_by_type("persona")
    scenario_insights = meta_tracker.get_insights_by_type("scenario")
    system_insights = meta_tracker.get_insights_by_type("system")

    print(f"   Persona insights: {len(persona_insights)}")
    print(f"   Scenario insights: {len(scenario_insights)}")
    print(f"   System insights: {len(system_insights)}")

    # Demonstrate retrieval by version
    print("\n🏷️  Retrieving insights by version:")
    v1_insights = meta_tracker.get_insights_by_version("0.1.0")
    print(f"   Version 0.1.0 insights: {len(v1_insights)}")

    # Show insights summary
    print("\n📈 Insights Summary:")
    summary = meta_tracker.insights_db.get_insights_summary()
    print(f"   Total insights: {summary['total_insights']}")
    print(f"   By type: {summary['by_type']}")
    print(f"   By severity: {summary['by_severity']}")
    print(f"   Average confidence: {summary['average_confidence']:.2f}")
    print(f"   Recent insights (7 days): {summary['recent_insights']}")

    # Show high confidence insights
    print("\n🎯 High Confidence Insights (>= 0.8):")
    high_confidence = meta_tracker.insights_db.get_high_confidence_insights(0.8)
    for insight in high_confidence:
        print(
            f"   • {insight.description[:60]}... (confidence: {insight.confidence:.2f})"
        )

    # Demonstrate recommendations
    print("\n💡 Generating recommendations:")
    recommendations = meta_tracker.generate_recommendations()
    for rec in recommendations:
        print(f"   • {rec.title}: {rec.description}")
        print(
            f"     Priority: {rec.priority}, Impact: {rec.impact}, Effort: {rec.effort}"
        )

    # Show trends
    print("\n📊 Current Trends:")
    trends = meta_tracker.get_trends()
    for key, value in trends.items():
        print(f"   {key}: {value}")

    print("\n🎉 Meta-Tracker demo completed!")
    print(
        "The system is now tracking insights and generating actionable recommendations."
    )


if __name__ == "__main__":
    demo_meta_tracker()
