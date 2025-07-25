"""CLI output formatting helpers for calendar assistant."""

from typing import List


def format_events(events: List[str]) -> str:
    """Format a list of event strings into a CLI-friendly block."""
    output = "\n📅 Events:"
    if events:
        for event in events:
            output += f"\n  - {event}"
    else:
        output += "\n  (none)"
    return output


def format_reminders(reminders: List[str]) -> str:
    """Format a list of reminder strings into a CLI-friendly block."""
    output = "\n⏰ Reminders:"
    if reminders:
        for reminder in reminders:
            output += f"\n  - {reminder}"
    else:
        output += "\n  (none)"
    return output


def print_events_and_reminders(events: List[str], reminders: List[str]) -> None:
    """Print formatted events and reminders blocks to the CLI."""
    print(format_events(events))
    print(format_reminders(reminders))
