"""Main terminal loop for the calendar assistant. Handles user input, interpretation, and calendar actions."""

import os
from dotenv import load_dotenv

# Load environment variables from .env FIRST
load_dotenv()

import openai_client
import re  # For parsing duration input via regex
from calendar_agent_eventkit import (
    list_events_and_reminders,
    create_event,
    delete_event,
    move_event,
    add_notification,
)
from utils.cli_output import format_events, format_reminders, print_events_and_reminders

# Main terminal loop
if __name__ == "__main__":
    print("Welcome to the Terminal Calendar Assistant! Type 'exit' to quit.")
    while True:
        user_input = input("\n> ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break
        # Interpret the command using GPT-4o
        interpreted = openai_client.interpret_command(user_input)
        print(f"\n[Interpreted]: {interpreted}")

        # Handle different action types
        action = interpreted.get("action") if interpreted else None
        details = interpreted.get("details") if interpreted else {}
        if not isinstance(details, dict):
            details = {}

        start_date = details.get("start_date")
        end_date = details.get("end_date")

        if action in [
            "list_todays_events",
            "list_all",
            "list_events_only",
            "list_reminders_only",
        ]:
            # Use CLI output helpers
            result = list_events_and_reminders(start_date, end_date)
            if result.get("error"):
                print(f"❌ Error: {result['error']}")
                continue
            events = result.get("events", [])
            reminders = result.get("reminders", [])
            if action in ["list_todays_events", "list_all"]:
                print_events_and_reminders(events, reminders)
            elif action == "list_events_only":
                print(format_events(events))
            elif action == "list_reminders_only":
                print(format_reminders(reminders))

        elif action == "create_event":
            # Prompt for duration if not provided
            if "duration" not in details or details.get("duration") is None:
                # Ask user for duration (default 60)
                resp = input(
                    "Duration not specified. Is one hour enough? (enter minutes e.g. 15 or press Enter for 60): "
                )
                resp_str = resp.strip()
                if resp_str:
                    # Try direct integer parsing
                    try:
                        details["duration"] = int(resp_str)
                    except ValueError:
                        # Fallback to extract first number via regex
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

        elif action == "delete_event":
            result = delete_event(details)
            if result.get("success"):
                print(f"✅ {result.get('message')}")
            else:
                print(f"❌ Error: {result.get('error')}")

        elif action == "move_event":
            result = move_event(details)
            if result.get("success"):
                print(f"✅ {result.get('message')}")
            else:
                print(f"❌ Error: {result.get('error')}")

        elif action == "add_notification":
            result = add_notification(details)
            if result.get("success"):
                print(f"✅ {result.get('message')}")
            else:
                print(f"❌ Error: {result.get('error')}")

        else:
            print("[Not implemented yet]")
