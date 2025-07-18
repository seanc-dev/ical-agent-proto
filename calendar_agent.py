"""Handles Apple Calendar actions for the terminal calendar assistant."""

import subprocess
from datetime import datetime, timedelta


def _date_parts(date_str):
    """Return (year, month, day) tuple from YYYY-MM-DD string."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt.year, dt.month, dt.day


def _warm_up_calendar():
    """Warm up Calendar app to ensure consistent access."""
    warmup_script = """
    try
        tell application "Calendar"
            set calCount to count of calendars
            return "WARMUP_OK"
        end tell
    on error errMsg
        return "WARMUP_ERROR:" & errMsg
    end try
    """
    try:
        result = subprocess.run(
            ["osascript", "-e", warmup_script],
            capture_output=True,
            text=True,
            check=False,
        )
        return "WARMUP_OK" in result.stdout
    except Exception:
        return False


def list_events_and_reminders(start_date=None, end_date=None):
    """
    List events and reminders from Apple Calendar and Reminders for a given date or date range.
    Includes all-day events and only incomplete reminders.
    Dates should be strings in 'YYYY-MM-DD' format. If not provided, defaults to today.
    Returns a dict with 'events' and 'reminders' lists.
    """
    # Warm up Calendar app first
    _warm_up_calendar()

    if not start_date:
        start_date = datetime.now().strftime("%Y-%m-%d")
    if not end_date:
        end_date = start_date

    # Convert to AppleScript-friendly date strings like '18 July 2025 00:00:00'
    def _as_applescript_date(date_obj):
        return date_obj.strftime("%d %B %Y %H:%M:%S")

    start_dt = datetime.strptime(start_date + " 00:00", "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(end_date + " 23:59", "%Y-%m-%d %H:%M")

    start_as = _as_applescript_date(start_dt)
    end_as = _as_applescript_date(end_dt)

    print(f"[DEBUG] Querying events from {start_as} to {end_as}")

    script = f"""
    try
        set eventsOutput to ""
        set remindersOutput to ""
        set debugOutput to ""
        
        -- Use date strings directly in an AppleScript-friendly format
        set rangeStart to date "{start_as}"
        set rangeEnd to date "{end_as}"
        
        set debugOutput to debugOutput & "Date range: " & (rangeStart as string) & " to " & (rangeEnd as string) & "\n"
        
        tell application "Calendar"
            set totalEvents to 0
            repeat with cal in calendars
                set allCalEvents to (every event of cal)
                set calEventCount to count of allCalEvents
                set totalEvents to totalEvents + calEventCount
                set debugOutput to debugOutput & "Calendar: " & (name of cal) & " has " & calEventCount & " total events\n"
                
                set theEvents to (every event of cal whose start date >= rangeStart and start date <= rangeEnd)
                set filteredCount to count of theEvents
                set debugOutput to debugOutput & "  Found " & filteredCount & " events in date range\n"
                
                repeat with evt in theEvents
                    set eventsOutput to eventsOutput & (summary of evt) & " | " & (start date of evt as string) & "\n"
                end repeat
                
                set allDayEvents to (every event of cal whose all day event is true and start date >= rangeStart and start date <= rangeEnd)
                set allDayCount to count of allDayEvents
                set debugOutput to debugOutput & "  Found " & allDayCount & " all-day events\n"
                
                repeat with evt in allDayEvents
                    set eventsOutput to eventsOutput & (summary of evt) & " | All Day\n"
                end repeat
            end repeat
            set debugOutput to debugOutput & "Total events across all calendars: " & totalEvents & "\n"
        end tell
        
        tell application "Reminders"
            set totalReminders to 0
            repeat with lst in lists
                set allReminders to (every reminder of lst)
                set reminderCount to count of allReminders
                set totalReminders to totalReminders + reminderCount
                set debugOutput to debugOutput & "Reminder list: " & (name of lst) & " has " & reminderCount & " total reminders\n"
                
                set theReminders to (every reminder of lst whose due date >= rangeStart and due date <= rangeEnd and completed is false)
                set filteredReminderCount to count of theReminders
                set debugOutput to debugOutput & "  Found " & filteredReminderCount & " incomplete reminders in date range\n"
                
                repeat with rem in theReminders
                    set remindersOutput to remindersOutput & (name of rem) & " | " & (due date of rem as string) & "\n"
                end repeat
                
                set allDayReminders to (every reminder of lst whose all day is true and due date >= rangeStart and due date <= rangeEnd and completed is false)
                set allDayReminderCount to count of allDayReminders
                set debugOutput to debugOutput & "  Found " & allDayReminderCount & " all-day incomplete reminders\n"
                
                repeat with rem in allDayReminders
                    set remindersOutput to remindersOutput & (name of rem) & " | All Day\n"
                end repeat
            end repeat
            set debugOutput to debugOutput & "Total reminders across all lists: " & totalReminders & "\n"
        end tell
        
        return "DEBUG:" & debugOutput & "EVENTS:" & eventsOutput & "REMINDERS:" & remindersOutput
    on error errMsg
        return "ERROR:" & errMsg
    end try
    """

    try:
        result = subprocess.run(
            ["osascript", "-e", script], capture_output=True, text=True, check=False
        )
        output = result.stdout.strip()

        if result.stderr:
            print("[DEBUG] AppleScript stderr:", result.stderr.strip())

        if output.startswith("ERROR:"):
            error_msg = output.replace("ERROR:", "").strip()
            print("[DEBUG] AppleScript error:", error_msg)
            return {"events": [f"AppleScript error: {error_msg}"], "reminders": []}

        if "DEBUG:" in output:
            debug_part = output.split("DEBUG:")[1].split("EVENTS:")[0]
            print("[DEBUG] AppleScript debug output:")
            print(debug_part)

        if output and "EVENTS:" in output:
            parts = output.split("EVENTS:")
            if len(parts) > 1:
                events_reminders_part = parts[1]
                if "REMINDERS:" in events_reminders_part:
                    events_part, reminders_part = events_reminders_part.split(
                        "REMINDERS:", 1
                    )
                else:
                    events_part = events_reminders_part
                    reminders_part = ""

                events = [e for e in events_part.strip().split("\n") if e.strip()]
                reminders = [r for r in reminders_part.strip().split("\n") if r.strip()]
                return {"events": events, "reminders": reminders}

        return {"events": [], "reminders": []}
    except Exception as e:
        return {"events": [f"Error fetching events: {e}"], "reminders": []}


def create_event(details):
    """Create a new event in Apple Calendar."""
    title = details.get("title", "Untitled Event")
    date_str = details.get("date")
    time_str = details.get("time", "09:00")
    duration = details.get("duration", 60)  # Default 1 hour in minutes

    if not date_str:
        return {"success": False, "error": "Date is required"}

    try:
        # Parse date and time
        start_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        end_datetime = start_datetime + timedelta(minutes=duration)

        print(f"[DEBUG] Creating event: {title}")
        print(f"[DEBUG] Start: {start_datetime}")
        print(f"[DEBUG] End: {end_datetime}")
        print(f"[DEBUG] Duration: {duration} minutes")

        # Use a simpler approach with date arithmetic
        script = f"""
        try
            tell application "Calendar"
                set newEvent to make new event at end of events of calendar 1
                set summary of newEvent to "{title}"
                
                -- Set start date using date string
                set start date of newEvent to date "{start_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
                
                -- Set end date using date arithmetic (start + 1 hour)
                set end date of newEvent to (start date of newEvent) + {duration} * minutes
                
                return "SUCCESS: Event created"
            end tell
        on error errMsg
            return "ERROR:" & errMsg
        end try
        """

        print(f"[DEBUG] AppleScript:")
        print(script)

        result = subprocess.run(
            ["osascript", "-e", script], capture_output=True, text=True, check=False
        )

        print(f"[DEBUG] AppleScript result: {result.stdout.strip()}")
        if result.stderr:
            print(f"[DEBUG] AppleScript stderr: {result.stderr.strip()}")

        if "SUCCESS" in result.stdout:
            return {"success": True, "message": "Event created successfully"}
        else:
            error_msg = result.stdout.replace("ERROR:", "").strip()
            return {"success": False, "error": error_msg}

    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_event(details):
    """Delete an event from Apple Calendar."""
    title = details.get("title")
    date_str = details.get("date")

    if not title or not date_str:
        return {"success": False, "error": "Title and date are required"}

    try:
        event_date = datetime.strptime(date_str, "%Y-%m-%d")
        sy, sm, sd = _date_parts(date_str)

        script = f"""
        try
            tell application "Calendar"
                repeat with cal in calendars
                    set targetEvents to (every event of cal whose summary is "{title}" and start date ≥ date "{date_str} 00:00" and start date < date "{date_str} 23:59")
                    repeat with evt in targetEvents
                        delete evt
                    end repeat
                end repeat
                return "SUCCESS: Event deleted"
            end tell
        on error errMsg
            return "ERROR:" & errMsg
        end try
        """

        result = subprocess.run(
            ["osascript", "-e", script], capture_output=True, text=True, check=False
        )

        if "SUCCESS" in result.stdout:
            return {"success": True, "message": "Event deleted successfully"}
        else:
            error_msg = result.stdout.replace("ERROR:", "").strip()
            return {"success": False, "error": error_msg}

    except Exception as e:
        return {"success": False, "error": str(e)}


def move_event(details):
    """Move an event in Apple Calendar."""
    title = details.get("title")
    old_date = details.get("old_date")
    new_date = details.get("new_date")
    new_time = details.get("new_time", "09:00")

    if not all([title, old_date, new_date]):
        return {"success": False, "error": "Title, old_date, and new_date are required"}

    try:
        new_datetime = datetime.strptime(f"{new_date} {new_time}", "%Y-%m-%d %H:%M")

        script = f"""
        try
            tell application "Calendar"
                repeat with cal in calendars
                    set targetEvents to (every event of cal whose summary is "{title}" and start date ≥ date "{old_date} 00:00" and start date < date "{old_date} 23:59")
                    repeat with evt in targetEvents
                        set start date of evt to date "{new_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
                        set end date of evt to date "{new_datetime.strftime('%Y-%m-%d %H:%M:%S')}" + 1 * hours
                    end repeat
                end repeat
                return "SUCCESS: Event moved"
            end tell
        on error errMsg
            return "ERROR:" & errMsg
        end try
        """

        result = subprocess.run(
            ["osascript", "-e", script], capture_output=True, text=True, check=False
        )

        if "SUCCESS" in result.stdout:
            return {"success": True, "message": "Event moved successfully"}
        else:
            error_msg = result.stdout.replace("ERROR:", "").strip()
            return {"success": False, "error": error_msg}

    except Exception as e:
        return {"success": False, "error": str(e)}
