"""Wraps GPT-4o (OpenAI) calls for interpreting user commands in the terminal calendar assistant."""

from dotenv import load_dotenv  # type: ignore
import os

try:
    import openai  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    openai = None
import json
import re

# Normalized date parsing import
from datetime import datetime, timedelta  # Added for date parsing in fallback
from utils.date_utils import parse_date_string
from utils.command_utils import (
    parse_list_range,
    parse_schedule_event,
    parse_delete_event,
    parse_move_event,
    parse_add_notification,
    parse_single_date_list,
)

# Load environment variables from .env
load_dotenv()
# Load API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Create OpenAI client (for SDK v1.x)
client = openai.OpenAI(api_key=OPENAI_API_KEY) if openai and OPENAI_API_KEY else None

# Define available functions for function calling
calendar_functions = [
    {
        "name": "list_events_only",
        "description": "List only calendar events for today.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "list_reminders_only",
        "description": "List only reminders for today.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "list_all",
        "description": "List both events and reminders for today.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "list_todays_events",
        "description": "List all events and reminders for today (legacy fallback).",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "create_event",
        "description": "Create a new calendar event.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Event title"},
                "date": {"type": "string", "description": "Event date (YYYY-MM-DD)"},
                "time": {"type": "string", "description": "Event time (e.g., 14:00)"},
                "duration": {"type": "integer", "description": "Duration in minutes"},
                "location": {"type": "string", "description": "Event location"},
            },
            "required": ["title", "date", "time"],
        },
    },
    {
        "name": "delete_event",
        "description": "Delete an existing calendar event.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Event title to delete"},
                "date": {"type": "string", "description": "Event date (YYYY-MM-DD)"},
            },
            "required": ["title", "date"],
        },
    },
    {
        "name": "move_event",
        "description": "Move an existing calendar event to a new date/time.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Event title to move"},
                "old_date": {
                    "type": "string",
                    "description": "Current event date (YYYY-MM-DD)",
                },
                "new_date": {
                    "type": "string",
                    "description": "New event date (YYYY-MM-DD)",
                },
                "new_time": {
                    "type": "string",
                    "description": "New event time (e.g., 15:00)",
                },
            },
            "required": ["title", "old_date", "new_date", "new_time"],
        },
    },
    {
        "name": "add_notification",
        "description": "Add a notification reminder to an existing event.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Event title"},
                "date": {"type": "string", "description": "Event date (YYYY-MM-DD)"},
                "minutes_before": {
                    "type": "integer",
                    "description": "Minutes before event to trigger",
                },
            },
            "required": ["title", "date"],
        },
    },
]


def interpret_command(user_input):
    """
    Use GPT-4o function calling to interpret the user's natural language command and return a dict with action and details.
    """
    # Rule-based fallback only when no API key is provided; always prefer LLM when available
    # If no OpenAI client (e.g. missing API key), use rule-based fallback with extraction
    if not client:
        # Rule-based parsers in precedence order
        for parser, action in [
            (parse_list_range, "list_events_only"),
            (parse_schedule_event, "create_event"),
            (parse_delete_event, "delete_event"),
            (parse_move_event, "move_event"),
            (parse_add_notification, "add_notification"),
            (parse_single_date_list, "list_events_only"),
        ]:
            details = parser(user_input)
            if details:
                return {"action": action, "details": details}
        # Default unknown
        return {"action": "error", "details": {}}
    try:
        # Provide current date, time, and day context to the LLM
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M")
        current_day = now.strftime("%A")
        system_message = {
            "role": "system",
            "content": (
                f"You are a calendar assistant. Today is {current_day}, {current_date} at {current_time}. "
                "Respond only with a JSON function call to exactly one of the available functions: "
                "create_event, delete_event, move_event, list_reminders_only, list_events_only, list_all. "
                "Follow this precedence strictly: "
                "1) Cancellation verbs (delete, cancel, remove) → delete_event. "
                "2) Rescheduling verbs (move, reschedule, shift) → move_event. "
                "3) Scheduling verbs (schedule, create, add, book) → create_event. "
                "4) If the text contains 'reminder' or 'task' → list_reminders_only. "
                "5) If the text contains 'event' or 'appointment' → list_events_only. "
                "6) General listing queries ('what's on', 'show me', 'what do I have', 'today', 'on') → list_all. "
                "7) If the user mentions a weekday name (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday), compute the next occurrence of that day relative to today and call list_events_only with start_date and end_date set to that date. "
                # Location extraction
                "When creating an event, if the user specifies a location (phrases like 'at the cafe', 'in Conference Room B', or 'on Zoom'), include it as the 'location' field in the function arguments; otherwise omit 'location'. "
                # Duration extraction
                "When creating an event, if the user specifies a duration (phrases like 'for 45 minutes', 'for one hour', 'for 2 hours'), include it as the 'duration' field (integer minutes) in the function arguments; otherwise omit 'duration'. "
                "Do not return any other text. If no rule matches, return action 'unknown'."
            ),
        }
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[system_message, {"role": "user", "content": user_input}],
            functions=calendar_functions,  # type: ignore
            function_call="auto",
            temperature=0.0,
            max_tokens=256,
        )
        message = response.choices[0].message
        if message.function_call:
            func_name = message.function_call.name
            try:
                arguments = (
                    json.loads(message.function_call.arguments)
                    if message.function_call.arguments
                    else {}
                )
            except Exception:
                arguments = message.function_call.arguments or {}
            return {"action": func_name, "details": arguments}
        else:
            # Fallback mapping when function calling returns no selection
            lower = user_input.lower()
            if any(k in lower for k in ("delete", "cancel", "remove")):
                return {"action": "delete_event", "details": {}}
            if any(k in lower for k in ("move", "reschedule", "shift")):
                return {"action": "move_event", "details": {}}
            if any(k in lower for k in ("schedule", "create", "add", "book")):
                return {"action": "create_event", "details": {}}
            if "reminder" in lower or "task" in lower:
                return {"action": "list_reminders_only", "details": {}}
            if "event" in lower:
                return {"action": "list_events_only", "details": {}}
            if "today" in lower or "on" in lower:
                return {"action": "list_all", "details": {}}
            return {"action": "unknown", "details": user_input}
    except Exception as e:
        return {"action": "error", "details": str(e)}
