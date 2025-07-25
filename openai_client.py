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
        details = {}
        # Extract duration in hours (e.g., '2-hour')
        m_hour = re.search(r"(\d+)\s*-?\s*hour", user_input, re.IGNORECASE)
        if m_hour:
            details["duration"] = int(m_hour.group(1)) * 60
        else:
            # Extract duration in minutes (e.g., '45min' or '45 minutes')
            m_min = re.search(r"(\d+)\s*(?:min(?:ute)?s?)", user_input, re.IGNORECASE)
            if m_min:
                details["duration"] = int(m_min.group(1))
        # Extract location by splitting on the last ' at ' to avoid capturing times
        lower_input = user_input.lower()
        if " at " in lower_input:
            # Split on the last ' at '
            loc = lower_input.rsplit(" at ", 1)[1].strip()
            details["location"] = loc
        lower = user_input.lower()
        # Extract explicit list range: 'list events from YYYY-MM-DD to YYYY-MM-DD'
        m_range = re.search(
            r"list events from\s+(\d{4}-\d{2}-\d{2})\s+to\s+(\d{4}-\d{2}-\d{2})",
            user_input,
            re.IGNORECASE,
        )
        if m_range:
            return {
                "action": "list_events_only",
                "details": {
                    "start_date": m_range.group(1),
                    "end_date": m_range.group(2),
                },
            }
        # Parse scheduling of a new event: 'schedule TITLE on DATE at TIME for DURATION minutes'
        m_sched = re.match(
            r"schedule\s+(.+?)\s+on\s+(tomorrow|\d{4}-\d{2}-\d{2})\s+at\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)\s+for\s+(\d+)\s*minutes",
            user_input,
            re.IGNORECASE,
        )
        if m_sched:
            title = m_sched.group(1).strip()
            date_raw = m_sched.group(2).strip().lower()
            # Resolve 'tomorrow'
            if date_raw == "tomorrow":
                date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            else:
                date = date_raw
            time_raw = m_sched.group(3).strip().lower()
            # Parse time (e.g., '1pm', '13:30')
            tm = re.match(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", time_raw)
            if tm:
                hour = int(tm.group(1))
                minute = int(tm.group(2) or 0)
                ampm = tm.group(3)
                if ampm:
                    if ampm == "pm" and hour < 12:
                        hour += 12
                    if ampm == "am" and hour == 12:
                        hour = 0
                time_str = f"{hour:02d}:{minute:02d}"
            else:
                time_str = time_raw
            duration = int(m_sched.group(4))
            return {
                "action": "create_event",
                "details": {
                    "title": title,
                    "date": date,
                    "time": time_str,
                    "duration": duration,
                },
            }
        # Parse deleting an event: 'delete TITLE on DATE'
        m_del = re.match(
            r"delete\s+(.+?)\s+on\s+(tomorrow|\d{4}-\d{2}-\d{2})",
            user_input,
            re.IGNORECASE,
        )
        if m_del:
            title = m_del.group(1).strip()
            date_raw = m_del.group(2).strip().lower()
            date = (
                (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                if date_raw == "tomorrow"
                else date_raw
            )
            return {"action": "delete_event", "details": {"title": title, "date": date}}
        # Parse moving an event: 'move TITLE on OLD_DATE to NEW_DATE at NEW_TIME'
        m_move = re.match(
            r"move\s+(.+?)\s+on\s+(tomorrow|\d{4}-\d{2}-\d{2})\s+to\s+(tomorrow|\d{4}-\d{2}-\d{2})\s+at\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)",
            user_input,
            re.IGNORECASE,
        )
        if m_move:
            title = m_move.group(1).strip()
            old_raw = m_move.group(2).strip().lower()
            new_raw = m_move.group(3).strip().lower()
            old_date = (
                (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                if old_raw == "tomorrow"
                else old_raw
            )
            new_date = (
                (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                if new_raw == "tomorrow"
                else new_raw
            )
            time_raw = m_move.group(4).strip().lower()
            tm = re.match(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", time_raw)
            if tm:
                hour = int(tm.group(1))
                minute = int(tm.group(2) or 0)
                ampm = tm.group(3)
                if ampm:
                    if ampm == "pm" and hour < 12:
                        hour += 12
                    if ampm == "am" and hour == 12:
                        hour = 0
                new_time = f"{hour:02d}:{minute:02d}"
            else:
                new_time = time_raw
            return {
                "action": "move_event",
                "details": {
                    "title": title,
                    "old_date": old_date,
                    "new_date": new_date,
                    "new_time": new_time,
                },
            }
        # Parse notifications: 'add notification to TITLE on DATE X minutes before'
        m_notify = re.match(
            r"add\s+notification\s+to\s+(.+?)\s+on\s+(tomorrow|\d{4}-\d{2}-\d{2})\s+(\d+)\s+minutes?\s+before",
            user_input,
            re.IGNORECASE,
        )
        if m_notify:
            title = m_notify.group(1).strip()
            date_raw = m_notify.group(2).strip().lower()
            date = (
                (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                if date_raw == "tomorrow"
                else date_raw
            )
            minutes_before = int(m_notify.group(3))
            return {
                "action": "add_notification",
                "details": {
                    "title": title,
                    "date": date,
                    "minutes_before": minutes_before,
                },
            }
        # Parse single-date list: 'events for/on YYYY-MM-DD'
        m_single = re.search(
            r"events? (?:for|on)\s+(\d{4}-\d{2}-\d{2})",
            user_input,
            re.IGNORECASE,
        )
        if m_single:
            return {
                "action": "list_events_only",
                "details": {
                    "start_date": m_single.group(1),
                    "end_date": m_single.group(1),
                },
            }
        # Determine action based on keywords
        if any(k in lower for k in ("delete", "cancel", "remove")):
            return {"action": "delete_event", "details": details}
        if any(k in lower for k in ("move", "reschedule", "shift")):
            return {"action": "move_event", "details": details}
        if any(k in lower for k in ("schedule", "create", "add", "book")):
            return {"action": "create_event", "details": details}
        if "reminder" in lower or "task" in lower:
            return {"action": "list_reminders_only", "details": details}
        if "event" in lower or "events" in lower:
            return {"action": "list_events_only", "details": details}
        if "today" in lower or "on" in lower:
            return {"action": "list_all", "details": details}
        # Default fallback
        return {"action": "error", "details": details}
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
