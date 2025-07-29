#!/usr/bin/env python3
"""Demo script to showcase the TrendAnalyzer functionality."""

import os
import sys
from datetime import datetime, timedelta
from llm_testing.trend_analyzer import TrendAnalyzer, TrendPoint, TrendAnalysis
from llm_testing.insights_database import InsightsDatabase
from llm_testing.types import EvaluationResult


def create_sample_evaluation_results():
    """Create sample evaluation results for demonstration."""
    results = []
    base_time = datetime.now() - timedelta(days=30)

    # Create improving trend
    for i in range(10):
        base_score = 3.0 + (i * 0.15)  # Improving trend
        result = EvaluationResult(
            scenario_name=f"MorningRoutine{i % 3}",
            persona_name=f"Alex{i % 2}",
            prompt=f"Schedule morning routine for day {i}",
            assistant_response=f"Here's your morning routine for day {i}",
            scores={
                "clarity": base_score + 0.1,
                "helpfulness": base_score,
                "accuracy": base_score - 0.1,
                "relevance": base_score + 0.2,
                "completeness": base_score - 0.2,
            },
            intermediate_scores={},
            feedback=f"Good response for day {i}",
            timestamp=(base_time + timedelta(days=i)).isoformat(),
            code_version="0.1.0",
            model_version="gpt-4",
            metadata={"test": True, "trend": "improving"},
        )
        results.append(result)

    # Create declining trend
    for i in range(8):
        base_score = 4.5 - (i * 0.2)  # Declining trend
        result = EvaluationResult(
            scenario_name=f"EveningRoutine{i % 3}",
            persona_name=f"Sam{i % 2}",
            prompt=f"Schedule evening routine for day {i}",
            assistant_response=f"Here's your evening routine for day {i}",
            scores={
                "clarity": base_score + 0.1,
                "helpfulness": base_score,
                "accuracy": base_score - 0.1,
                "relevance": base_score + 0.2,
                "completeness": base_score - 0.2,
            },
            intermediate_scores={},
            feedback=f"Response for day {i}",
            timestamp=(base_time + timedelta(days=i + 10)).isoformat(),
            code_version="0.1.0",
            model_version="gpt-4",
            metadata={"test": True, "trend": "declining"},
        )
        results.append(result)

    # Create stable trend
    for i in range(6):
        base_score = 3.5  # Stable trend
        result = EvaluationResult(
            scenario_name=f"WorkoutRoutine{i % 3}",
            persona_name=f"Jordan{i % 2}",
            prompt=f"Schedule workout for day {i}",
            assistant_response=f"Here's your workout for day {i}",
            scores={
                "clarity": base_score + 0.1,
                "helpfulness": base_score,
                "accuracy": base_score - 0.1,
                "relevance": base_score + 0.2,
                "completeness": base_score - 0.2,
            },
            intermediate_scores={},
            feedback=f"Workout response for day {i}",
            timestamp=(base_time + timedelta(days=i + 20)).isoformat(),
            code_version="0.1.0",
            model_version="gpt-4",
            metadata={"test": True, "trend": "stable"},
        )
        results.append(result)

    return results


def main():
    """Run the TrendAnalyzer demo."""
    print("📊 TrendAnalyzer Demo")
    print("=" * 50)

    # Initialize components
    insights_db = InsightsDatabase("demo_insights.db")
    trend_analyzer = TrendAnalyzer(insights_db)

    # Create sample data
    print("\n📋 Creating sample evaluation results...")
    results = create_sample_evaluation_results()
    print(f"✅ Created {len(results)} sample evaluation results")

    # Analyze performance trends
    print("\n🔍 Analyzing performance trends...")
    trends = trend_analyzer.analyze_performance_trends(results)

    print(f"\n📈 Trend Analysis Results:")
    print("-" * 40)

    for trend_name, trend in trends.items():
        print(f"\n🎯 {trend_name.replace('_', ' ').title()}:")
        print(f"   Type: {trend.trend_type}")
        print(f"   Confidence: {trend.confidence:.2f}")
        print(f"   Slope: {trend.slope:.4f}")
        print(f"   R-squared: {trend.r_squared:.2f}")
        print(f"   Severity: {trend.severity}")
        print(f"   Data Points: {len(trend.data_points)}")

        if trend.insights:
            print(f"   Insights:")
            for insight in trend.insights:
                print(f"     • {insight}")

        if trend.recommendations:
            print(f"   Recommendations:")
            for rec in trend.recommendations:
                print(f"     • {rec}")

    # Generate performance summary
    print(f"\n📊 Performance Summary:")
    print("-" * 30)
    summary = trend_analyzer.get_performance_summary(results)

    print(f"Total Tests: {summary['total_tests']}")
    print(f"Average Score: {summary['average_score']:.2f}")
    print(f"Score Std Dev: {summary['score_std']:.2f}")
    print(f"Min Score: {summary['min_score']:.2f}")
    print(f"Max Score: {summary['max_score']:.2f}")

    print(f"\nScore Distribution:")
    for category, count in summary["score_distribution"].items():
        print(f"  {category.title()}: {count}")

    print(f"\nPersona Performance:")
    for persona, score in summary["persona_performance"].items():
        print(f"  {persona}: {score:.2f}")

    print(f"\nScenario Performance:")
    for scenario, score in summary["scenario_performance"].items():
        print(f"  {scenario}: {score:.2f}")

    print(f"\nCriteria Performance:")
    for criterion, score in summary["criteria_performance"].items():
        print(f"  {criterion.title()}: {score:.2f}")

    # Detect regressions
    print(f"\n🚨 Regression Detection:")
    print("-" * 30)

    # Split results into baseline and recent
    baseline_results = results[:10]  # First 10 as baseline
    recent_results = results[10:15]  # Next 5 as recent

    regressions = trend_analyzer.detect_regressions(recent_results, baseline_results)

    if regressions:
        print(f"Found {len(regressions)} potential regressions:")
        for regression in regressions:
            print(
                f"  • {regression['criterion']}: {regression['decline_percentage']:.1f}% decline"
            )
            print(
                f"    Baseline: {regression['baseline_score']:.2f} → Current: {regression['current_score']:.2f}"
            )
            print(f"    Severity: {regression['severity']}")
    else:
        print("No significant regressions detected.")

    # Generate trend insights
    print(f"\n💡 Generated Insights:")
    print("-" * 30)
    insights = trend_analyzer.generate_trend_insights(trends)

    for insight in insights:
        print(f"  • {insight.description}")
        print(f"    Confidence: {insight.confidence:.2f}")
        print(f"    Severity: {insight.severity}")
        print(f"    Type: {insight.insight_type}")

    # Store insights in database
    print(f"\n💾 Storing insights in database...")
    for insight in insights:
        insights_db.store_insight(insight)

    # Show database summary
    db_summary = insights_db.get_insights_summary()
    print(f"\n📊 Database Summary:")
    print(f"  Total Insights: {db_summary['total_insights']}")
    print(f"  Average Confidence: {db_summary['average_confidence']:.2f}")
    print(f"  Recent Insights: {db_summary['recent_insights']}")

    print(f"\n🎉 TrendAnalyzer demo completed!")
    print(f"Database location: {os.path.abspath('demo_insights.db')}")


if __name__ == "__main__":
    main()
