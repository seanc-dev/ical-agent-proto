"""Wraps GPT-4o (OpenAI) calls for interpreting user commands in the terminal calendar assistant."""

import os
try:
    import openai
except Exception:  # pragma: no cover - optional dependency
    openai = None
import json

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
                "minutes_before": {"type": "integer", "description": "Minutes before event to trigger"},
            },
            "required": ["title", "date"],
        },
    },
]


def interpret_command(user_input):
    """
    Use GPT-4o function calling to interpret the user's natural language command and return a dict with action and details.
    """
    if not client:
        return {"action": "error", "details": "OPENAI_API_KEY not set in environment."}
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful calendar assistant. Choose the single most appropriate function to satisfy the user's request. Do not guess or combine actions. If the request is ambiguous, choose the most specific function that fully satisfies it.",
                },
                {"role": "user", "content": user_input},
            ],
            functions=calendar_functions,
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
            return {"action": "unknown", "details": user_input}
    except Exception as e:
        return {"action": "error", "details": str(e)}
