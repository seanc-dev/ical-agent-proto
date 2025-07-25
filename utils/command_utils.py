import re
from datetime import datetime, timedelta
from utils.date_utils import parse_date_string


# Parses 'list events from START to END'
def parse_list_range(cmd: str):
    m = re.search(r"list events from\s+(\S+)\s+to\s+(\S+)", cmd, re.IGNORECASE)
    if m:
        return {
            "start_date": parse_date_string(m.group(1)),
            "end_date": parse_date_string(m.group(2)),
        }
    return None


# Parses 'schedule TITLE on DATE at TIME for DURATION minutes'
def parse_schedule_event(cmd: str):
    m = re.match(
        r"schedule\s+(.+?)\s+on\s+(\S+)\s+at\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)\s+for\s*(\d+)\s*minutes",
        cmd,
        re.IGNORECASE,
    )
    if m:
        title, date_raw, time_raw, duration = (
            m.group(1),
            m.group(2),
            m.group(3),
            m.group(4),
        )
        date = parse_date_string(date_raw)
        # Normalize time to HH:MM
        tm = re.match(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", time_raw, re.IGNORECASE)
        if tm:
            hour = int(tm.group(1))
            minute = int(tm.group(2) or 0)
            ampm = tm.group(3).lower() if tm.group(3) else None
            if ampm:
                if ampm == "pm" and hour < 12:
                    hour += 12
                if ampm == "am" and hour == 12:
                    hour = 0
            time_str = f"{hour:02d}:{minute:02d}"
        else:
            time_str = time_raw
        return {
            "title": title.strip(),
            "date": date,
            "time": time_str,
            "duration": int(duration),
        }
    return None


# Parses 'delete TITLE on DATE'
def parse_delete_event(cmd: str):
    m = re.match(r"delete\s+(.+?)\s+on\s+(\S+)", cmd, re.IGNORECASE)
    if m:
        title, date_raw = m.group(1).strip(), m.group(2)
        date = parse_date_string(date_raw)
        return {"title": title, "date": date}
    return None


# Parses 'move TITLE on OLD_DATE to NEW_DATE at NEW_TIME'
def parse_move_event(cmd: str):
    m = re.match(
        r"move\s+(.+?)\s+on\s+(\S+)\s+to\s+(\S+)\s+at\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)",
        cmd,
        re.IGNORECASE,
    )
    if m:
        title, old_raw, new_raw, time_raw = (
            m.group(1).strip(),
            m.group(2),
            m.group(3),
            m.group(4),
        )
        old_date = parse_date_string(old_raw)
        new_date = parse_date_string(new_raw)
        tm = re.match(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", time_raw, re.IGNORECASE)
        if tm:
            hour = int(tm.group(1))
            minute = int(tm.group(2) or 0)
            ampm = tm.group(3).lower() if tm.group(3) else None
            if ampm:
                if ampm == "pm" and hour < 12:
                    hour += 12
                if ampm == "am" and hour == 12:
                    hour = 0
            new_time = f"{hour:02d}:{minute:02d}"
        else:
            new_time = time_raw
        return {
            "title": title,
            "old_date": old_date,
            "new_date": new_date,
            "new_time": new_time,
        }
    return None


# Parses 'add notification to TITLE on DATE MIN minutes before'
def parse_add_notification(cmd: str):
    m = re.match(
        r"add\s+notification\s+to\s+(.+?)\s+on\s+(\S+)\s+(\d+)\s+minutes?\s+before",
        cmd,
        re.IGNORECASE,
    )
    if m:
        title, date_raw, minutes = m.group(1).strip(), m.group(2), int(m.group(3))
        date = parse_date_string(date_raw)
        return {"title": title, "date": date, "minutes_before": minutes}
    return None


# Parses 'events for/on YYYY-MM-DD' and allows weekday or 'tomorrow'
def parse_single_date_list(cmd: str):
    m = re.search(r"events?\s+(?:for|on)\s+(\S+)", cmd, re.IGNORECASE)
    if m:
        date = parse_date_string(m.group(1))
        return {"start_date": date, "end_date": date}
    return None
