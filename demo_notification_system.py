#!/usr/bin/env python3
"""Demo script for the LLM Testing Framework notification system."""

import json
from datetime import datetime
from llm_testing.notifications import (
    NotificationConfig,
    NotificationManager,
    create_notification_config_from_dict,
)
from llm_testing.dashboard import Dashboard, AlertSystem
from llm_testing.database import ResultsDatabase


def demo_notification_system():
    """Demonstrate the notification system capabilities."""
    print("🚀 LLM Testing Framework - Notification System Demo")
    print("=" * 60)

    # Create notification configuration
    config_dict = {
        "email_enabled": False,  # Set to True with real credentials
        "smtp_server": "smtp.gmail.com",
        "email_username": "your-email@gmail.com",
        "email_password": "your-app-password",
        "email_recipients": ["alerts@example.com"],
        "slack_enabled": False,  # Set to True with real webhook
        "slack_webhook_url": "https://hooks.slack.com/your-webhook",
        "slack_channel": "#alerts",
        "webhook_enabled": False,  # Set to True with real webhook
        "webhook_url": "https://api.example.com/webhook",
        "webhook_headers": {"Authorization": "Bearer your-token"},
    }

    config = create_notification_config_from_dict(config_dict)
    notification_manager = NotificationManager(config)

    print("📧 Notification Configuration:")
    print(f"   Email enabled: {config.email_enabled}")
    print(f"   Slack enabled: {config.slack_enabled}")
    print(f"   Webhook enabled: {config.webhook_enabled}")
    print()

    # Test notification providers
    print("🧪 Testing notification providers...")
    test_results = notification_manager.test_connections()

    for provider, success in test_results.items():
        status = "✅ Success" if success else "❌ Failed"
        print(f"   {provider.capitalize()}: {status}")
    print()

    # Create sample alerts
    sample_alerts = [
        {
            "severity": "critical",
            "type": "performance_regression",
            "message": "Performance regression detected in clarity scores",
            "first_seen": datetime.now().isoformat(),
            "key": "clarity_regression_001",
        },
        {
            "severity": "high",
            "type": "accessibility_issue",
            "message": "Accessibility issues detected in assistant responses",
            "first_seen": datetime.now().isoformat(),
            "key": "accessibility_001",
        },
        {
            "severity": "medium",
            "type": "trend_analysis",
            "message": "Declining trend in helpfulness scores over 7 days",
            "first_seen": datetime.now().isoformat(),
            "key": "helpfulness_trend_001",
        },
        {
            "severity": "low",
            "type": "test_completion",
            "message": "Test suite completed with 95% success rate",
            "first_seen": datetime.now().isoformat(),
            "key": "test_completion_001",
        },
    ]

    print("📢 Sending sample alerts...")
    for i, alert in enumerate(sample_alerts, 1):
        print(f"\n   Alert {i}: {alert['severity'].upper()} - {alert['type']}")
        results = notification_manager.send_notification(alert)

        for provider, success in results.items():
            status = "✅ Sent" if success else "❌ Failed"
            print(f"      {provider.capitalize()}: {status}")
    print()

    # Demo dashboard integration
    print("📊 Dashboard Integration Demo:")

    # Create a mock database
    db = ResultsDatabase(":memory:")

    # Create dashboard
    dashboard = Dashboard(db)

    # Create alert system with notification config
    alert_system = AlertSystem(dashboard, config_dict)

    print("   Dashboard created with notification integration")
    print("   Alert system configured with notification providers")
    print("   Ready to send real-time alerts during testing")
    print()

    # Show notification capabilities
    print("🎯 Notification System Features:")
    print("   ✅ Multi-provider support (Email, Slack, Webhook)")
    print("   ✅ Rich formatting (HTML emails, Slack attachments)")
    print("   ✅ Severity-based styling and emojis")
    print("   ✅ Error handling and graceful degradation")
    print("   ✅ Connection testing and health checks")
    print("   ✅ Dashboard integration for real-time alerts")
    print("   ✅ Configurable via dictionary or dataclass")
    print()

    # Configuration examples
    print("⚙️  Configuration Examples:")
    print()

    print("   Email Configuration:")
    print("   ```python")
    print("   config = NotificationConfig(")
    print("       email_enabled=True,")
    print("       smtp_server='smtp.gmail.com',")
    print("       email_username='your-email@gmail.com',")
    print("       email_password='your-app-password',")
    print("       email_recipients=['alerts@example.com']")
    print("   )")
    print("   ```")
    print()

    print("   Slack Configuration:")
    print("   ```python")
    print("   config = NotificationConfig(")
    print("       slack_enabled=True,")
    print("       slack_webhook_url='https://hooks.slack.com/your-webhook',")
    print("       slack_channel='#alerts'")
    print("   )")
    print("   ```")
    print()

    print("   Webhook Configuration:")
    print("   ```python")
    print("   config = NotificationConfig(")
    print("       webhook_enabled=True,")
    print("       webhook_url='https://api.example.com/webhook',")
    print("       webhook_headers={'Authorization': 'Bearer token'}")
    print("   )")
    print("   ```")
    print()

    print("🎉 Notification system demo completed!")
    print("   To enable real notifications, update the configuration")
    print("   with your actual credentials and webhook URLs.")


if __name__ == "__main__":
    demo_notification_system()
