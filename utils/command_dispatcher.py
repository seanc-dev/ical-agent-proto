"""Command dispatcher for main loop actions."""

import re
from calendar_agent_eventkit import (
    list_events_and_reminders,
    create_event,
    delete_event,
    move_event,
    add_notification,
)
from utils.cli_output import format_events, format_reminders, print_events_and_reminders


def handle_list_todays_events(details):
    result = list_events_and_reminders(
        details.get("start_date"), details.get("end_date")
    )
    if result.get("error"):
        print(f"❌ Error: {result['error']}")
        return
    print_events_and_reminders(result.get("events", []), result.get("reminders", []))


def handle_list_all(details):
    # Alias for list_todays_events
    handle_list_todays_events(details)


def handle_list_events_only(details):
    result = list_events_and_reminders(
        details.get("start_date"), details.get("end_date")
    )
    if result.get("error"):
        print(f"❌ Error: {result['error']}")
        return
    print(format_events(result.get("events", [])))


def handle_list_reminders_only(details):
    result = list_events_and_reminders(
        details.get("start_date"), details.get("end_date")
    )
    if result.get("error"):
        print(f"❌ Error: {result['error']}")
        return
    print(format_reminders(result.get("reminders", [])))


def handle_create_event(details):
    # Prompt for duration if not provided
    if "duration" not in details or details.get("duration") is None:
        resp = input(
            "Duration not specified. Is one hour enough? (enter minutes e.g. 15 or press Enter for 60): "
        )
        resp_str = resp.strip()
        if resp_str:
            try:
                details["duration"] = int(resp_str)
            except ValueError:
                m = re.search(r"(\d+)", resp_str)
                if m:
                    details["duration"] = int(m.group(1))
                else:
                    print("Invalid duration; defaulting to 60 minutes.")
                    details["duration"] = 60
        else:
            details["duration"] = 60
    result = create_event(details)
    if result.get("success"):
        print(f"✅ {result.get('message')}")
    else:
        print(f"❌ Error: {result.get('error')}")


def handle_delete_event(details):
    result = delete_event(details)
    if result.get("success"):
        print(f"✅ {result.get('message')}")
    else:
        print(f"❌ Error: {result.get('error')}")


def handle_move_event(details):
    result = move_event(details)
    if result.get("success"):
        print(f"✅ {result.get('message')}")
    else:
        print(f"❌ Error: {result.get('error')}")


def handle_add_notification(details):
    result = add_notification(details)
    if result.get("success"):
        print(f"✅ {result.get('message')}")
    else:
        print(f"❌ Error: {result.get('error')}")


# Map actions to handlers
HANDLERS = {
    "list_todays_events": handle_list_todays_events,
    "list_all": handle_list_all,
    "list_events_only": handle_list_events_only,
    "list_reminders_only": handle_list_reminders_only,
    "create_event": handle_create_event,
    "delete_event": handle_delete_event,
    "move_event": handle_move_event,
    "add_notification": handle_add_notification,
}


def dispatch(action: str, details: dict):
    """Dispatch the given action to the appropriate handler."""
    if action not in HANDLERS:
        raise KeyError(f"Unknown action: {action}")
    return HANDLERS[action](details)
