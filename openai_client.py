"""Wraps GPT-4o (OpenAI) calls for interpreting user commands in the terminal calendar assistant."""

from dotenv import load_dotenv  # load .env file
import os
import openai
import json

# Load environment variables from .env
load_dotenv()
# Load API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Create OpenAI client (for SDK v1.x)
client = openai.OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

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
]


def interpret_command(user_input):
    """
    Use GPT-4o function calling to interpret the user's natural language command and return a dict with action and details.
    """
    # If no OpenAI client (e.g. missing API key), use simple rule-based fallback
    if not client:
        lower = user_input.lower()
        if any(k in lower for k in ("schedule", "create", "add", "book")):
            return {"action": "create_event"}
        if any(k in lower for k in ("delete", "cancel", "remove")):
            return {"action": "delete_event"}
        if any(k in lower for k in ("move", "reschedule", "shift")):
            return {"action": "move_event"}
        if "reminder" in lower:
            return {"action": "list_reminders_only"}
        if "event" in lower:
            return {"action": "list_events_only"}
        if "today" in lower or "on" in lower:
            return {"action": "list_all"}
        return {"action": "unknown", "details": user_input}
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a calendar assistant that must respond only with a function call to one of the available functions: "
                        "list_events_only, list_reminders_only, list_all, create_event, delete_event, move_event. "
                        "Do NOT return plain text. For scheduling intents (words: schedule, create, add, book), always call 'create_event' with title, date, and time. "
                        "For cancellations (delete, cancel, remove), call 'delete_event'. "
                        "For rescheduling (move, reschedule, shift), call 'move_event'. "
                        "For listing calendar events only, call 'list_events_only'. For listing reminders only, call 'list_reminders_only'. "
                        "For general listing intents (today, on, show me), call 'list_all'. "
                        "Do not choose 'unknown' unless no function matches."
                    ),
                },
                {"role": "user", "content": user_input},
            ],
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
            if any(k in lower for k in ("schedule", "create", "add", "book")):
                return {"action": "create_event", "details": {}}
            if any(k in lower for k in ("delete", "cancel", "remove")):
                return {"action": "delete_event", "details": {}}
            if any(k in lower for k in ("move", "reschedule", "shift")):
                return {"action": "move_event", "details": {}}
            if "reminder" in lower:
                return {"action": "list_reminders_only", "details": {}}
            if "event" in lower:
                return {"action": "list_events_only", "details": {}}
            if "today" in lower or "on" in lower:
                return {"action": "list_all", "details": {}}
            return {"action": "unknown", "details": user_input}
    except Exception as e:
        return {"action": "error", "details": str(e)}
