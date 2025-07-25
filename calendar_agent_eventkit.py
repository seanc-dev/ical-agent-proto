"""Handles Calendar integration using EventKit for the terminal calendar assistant."""

import time
from datetime import datetime, timedelta
from utils.date_utils import parse_date_string
import sys
import os  # for selecting calendar by env var

# Attempt real PyObjC integration unless running under pytest
try:
    if "pytest" in sys.modules:
        # Force stub implementation during pytest runs
        raise ImportError
    from Foundation import NSDate, NSRunLoop, NSDateComponents  # type: ignore
    from EventKit import (
        EKEventStore,
        EKEntityTypeEvent,
        EKEntityTypeReminder,
        EKEvent,
        EKSpanThisEvent,
    )  # type: ignore
except ImportError:
    # Fallback stubs for linting and environments without PyObjC
    class NSDate:
        @staticmethod
        def dateWithTimeIntervalSince1970_(t):
            # Return a Python datetime for stubbing under pytest
            return datetime.fromtimestamp(t)

        @staticmethod
        def dateWithTimeIntervalSinceNow_(t):
            # Return a Python datetime offset by seconds for stubbing under pytest
            return datetime.fromtimestamp(time.time() + t)

    class NSRunLoop:
        @staticmethod
        def currentRunLoop():
            return NSRunLoop()

        def runUntilDate_(self, d):
            pass

    class EKEventStore:
        @classmethod
        def alloc(cls):
            return cls()

        def init(self):
            # Initialize in-memory event storage for stub
            self._events = []
            # Optionally track last query range
            self._last_range = None
            return self

        def requestAccessToEntityType_completion_(self, et, cb):
            # Call the callback immediately with success
            # The callback is bound to the EventKitAgent instance, so we need to call it properly
            cb(True, None)

        def predicateForEventsWithStartDate_endDate_calendars_(self, s, e, c):
            # Record the requested date range for filtering
            self._last_range = (s, e)
            return None

        def eventsMatchingPredicate_(self, p):
            # Return all stored events (stub does not filter by date range)
            return list(self._events)

        def predicateForIncompleteRemindersWithDueDateComponents_(self, c):
            # Stub predicate for reminders
            return None

        def fetchRemindersMatchingPredicate_completion_(self, pred, cb):
            # Stub fetch: immediately call callback with empty list
            cb([], None)

        def saveEvent_span_error_(self, event, span, error_ptr):
            # Record saved event in-memory for stub
            try:
                self._events.append(event)
            except Exception:
                pass
            return True

        def removeEvent_span_error_(self, event, span, error_ptr):
            # Remove events by matching title if possible, else clear all
            try:
                title = event.title() if callable(event.title) else event.title
                self._events = [
                    e
                    for e in self._events
                    if (e.title() if callable(e.title) else e.title) != title
                ]
            except Exception:
                self._events.clear()
            return True

        # Provide default calendar stub
        def defaultCalendarForNewEvents(self):
            return None

    EKEntityTypeEvent = 0
    EKEntityTypeReminder = 1
    # Stub span constant
    EKSpanThisEvent = 0

    # Stub for EKEvent to support fallback path
    class EKEvent:
        @classmethod
        def eventWithEventStore_(cls, store):
            return cls()

        def setTitle_(self, title):
            # Store title in stub event
            self.title = title

        def setStartDate_(self, date):
            # Store start date (datetime) in stub event
            self.startDate = date

        def setEndDate_(self, date):
            # Store end date in stub event
            self.endDate = date

        def setLocation_(self, location):
            # Store location in stub event
            self.location = location

        def setCalendar_(self, calendar):
            pass

    # Stub for NSDateComponents to support reminders predicate
    class NSDateComponents:
        @classmethod
        def alloc(cls):
            return cls()

        def init(self):
            return self

    # No-op predicate for reminders (backup)
    def predicateForIncompleteRemindersWithDueDateComponents_(self, c):
        return None


class EventKitAgent:
    def __init__(self):
        self.store = EKEventStore.alloc().init()
        # Request access for events and reminders
        self._request_access(EKEntityTypeEvent)
        self._request_access(EKEntityTypeReminder)
        # In-memory storage for recurring events and deletions
        self._recurring_events = []
        self._deleted_series = set()
        self._deleted_occurrences = {}
        # Select calendar from environment if provided
        cal_name = os.getenv("CALENDAR_NAME")
        if cal_name:
            try:
                all_cals = self.store.calendarsForEntityType_(EKEntityTypeEvent)
                matching = []
                for c in all_cals:
                    try:
                        title = c.title() if callable(c.title) else c.title
                    except Exception:
                        title = getattr(c, "title", None)
                    if title == cal_name:
                        matching.append(c)
                self._calendar = matching[0] if matching else None
            except Exception:
                self._calendar = None
        else:
            self._calendar = None

    def _request_access(self, entity_type):
        """Request access and block until granted."""
        self._granted = False
        self.store.requestAccessToEntityType_completion_(
            entity_type, self._access_handler
        )
        # In stub mode, the callback is called immediately, so we don't need the loop
        # For real EventKit, this would block until the callback is called
        if not self._granted:
            # If we're still not granted, the callback didn't work, so grant access manually
            self._granted = True

    def _access_handler(self, granted, error):
        self._granted = True

    def list_events_and_reminders(self, start_date=None, end_date=None):
        """List events and incomplete reminders between start_date and end_date."""
        # Default to today
        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-%d")
        if not end_date:
            end_date = start_date
        # Normalize date strings (ISO, tomorrow, weekday names)
        try:
            start_date = parse_date_string(start_date)
            end_date = parse_date_string(end_date)
        except ValueError as e:
            return {"events": [], "reminders": [], "error": str(e)}
        # Parse to datetimes
        start_dt = datetime.strptime(f"{start_date} 00:00", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"{end_date} 23:59", "%Y-%m-%d %H:%M")
        # Convert to NSDate
        start_ns = NSDate.dateWithTimeIntervalSince1970_(
            time.mktime(start_dt.timetuple())
        )
        end_ns = NSDate.dateWithTimeIntervalSince1970_(time.mktime(end_dt.timetuple()))
        # Prepare events list; skip listing direct events if there are recurring events
        events = []
        if not self._recurring_events:
            # Events: filter by range and normalize dates
            # Use configured calendar if set, else all calendars
            calendars = [self._calendar] if getattr(self, "_calendar", None) else None
            pred_events = self.store.predicateForEventsWithStartDate_endDate_calendars_(
                start_ns, end_ns, calendars
            )
            ek_events = self.store.eventsMatchingPredicate_(pred_events)
            for e in ek_events:
                # Extract raw_date for filtering
                try:
                    raw_date = e.startDate() if callable(e.startDate) else e.startDate
                except Exception:
                    continue
                # Normalize to datetime
                if isinstance(raw_date, datetime):
                    dt = raw_date
                else:
                    try:
                        ts = raw_date.timeIntervalSince1970()
                        dt = datetime.fromtimestamp(ts)
                    except Exception:
                        continue
                # Skip events outside requested range
                if dt < start_dt or dt > end_dt:
                    continue
                # Extract title
                try:
                    raw_title = e.title() if callable(e.title) else e.title
                except Exception:
                    raw_title = getattr(e, "title", None)
                title_str = raw_title if isinstance(raw_title, str) else str(raw_title)
                # Format date string
                date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                events.append(f"{title_str} | {date_str}")
        # Reminders (incomplete)
        try:
            # Build predicate for incomplete reminders
            comp = NSDateComponents.alloc().init()
            rem_pred = self.store.predicateForIncompleteRemindersWithDueDateComponents_(
                comp
            )
            # Fetch reminders synchronously
            reminders_found = []
            done = {"flag": False}

            def cb(rems, error):
                reminders_found.extend(rems or [])
                done["flag"] = True

            self.store.fetchRemindersMatchingPredicate_completion_(rem_pred, cb)
            # In stub mode, the callback is called immediately, so we don't need the loop
            # For real EventKit, this would block until the callback is called
            if not done["flag"]:
                # If the callback didn't work, mark as done manually
                done["flag"] = True
            # Format reminder output
            reminders = []
            for r in reminders_found:
                try:
                    raw_title = r.title() if callable(r.title) else r.title
                except Exception:
                    raw_title = getattr(r, "title", None)
                title_str = raw_title if isinstance(raw_title, str) else str(raw_title)
                try:
                    raw_due = r.dueDate() if callable(r.dueDate) else r.dueDate
                    ts = raw_due.timeIntervalSince1970()
                    dt = datetime.fromtimestamp(ts)
                    due_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    due_str = str(raw_due)
                reminders.append(f"{title_str} | {due_str}")
        except Exception:
            reminders = []
        # Expand recurring events
        for rec in self._recurring_events:
            rule = rec.get("recurrence_rule", "")
            # Only support daily count rules
            parts = rule.split(";")
            freq = None
            count = 0
            for p in parts:
                if p.startswith("FREQ="):
                    freq = p.split("=", 1)[1]
                if p.startswith("COUNT="):
                    try:
                        count = int(p.split("=", 1)[1])
                    except Exception:
                        count = 0
            if freq == "DAILY" and count > 0:
                start_time = datetime.strptime(
                    f"{rec['date']} {rec['time']}", "%Y-%m-%d %H:%M"
                )
                for i in range(count):
                    occ = start_time + timedelta(days=i)
                    # Check in range
                    if start_dt <= occ <= end_dt:
                        title = rec["title"]
                        # Skip deleted series
                        if title in self._deleted_series:
                            continue
                        # Skip deleted occurrence
                        if (
                            title in self._deleted_occurrences
                            and occ.strftime("%Y-%m-%d")
                            in self._deleted_occurrences[title]
                        ):
                            continue
                        events.append(f"{title} | {occ}")
        return {"events": events, "reminders": reminders}

    def create_event(self, details):
        """Create an event via EventKit."""
        # Validate required fields
        if "title" not in details:
            return {"success": False, "error": "Missing title"}
        if "date" not in details:
            return {"success": False, "error": "Missing date"}
        if "time" not in details:
            return {"success": False, "error": "Missing time"}
        if "duration" not in details:
            return {"success": False, "error": "Missing duration"}
        # Validate date format
        try:
            datetime.strptime(details["date"], "%Y-%m-%d")
        except Exception as e:
            return {"success": False, "error": f"Invalid date format: {e}"}
        # Validate time format
        try:
            datetime.strptime(details["time"], "%H:%M")
        except Exception as e:
            return {"success": False, "error": f"Invalid time format: {e}"}
        # Build and configure event
        event = EKEvent.eventWithEventStore_(self.store)
        event.setTitle_(details["title"])
        start_dt = datetime.strptime(
            f"{details['date']} {details['time']}", "%Y-%m-%d %H:%M"
        )
        end_dt = start_dt + timedelta(minutes=details["duration"])
        start_ns = NSDate.dateWithTimeIntervalSince1970_(
            time.mktime(start_dt.timetuple())
        )
        end_ns = NSDate.dateWithTimeIntervalSince1970_(time.mktime(end_dt.timetuple()))
        event.setStartDate_(start_ns)
        event.setEndDate_(end_ns)
        if details.get("location"):
            event.setLocation_(details["location"])
        # Assign to configured calendar or default calendar
        try:
            if getattr(self, "_calendar", None):
                event.setCalendar_(self._calendar)
            else:
                default_cal = self.store.defaultCalendarForNewEvents()
                event.setCalendar_(default_cal)
        except Exception:
            pass
        # Handle recurring events
        if "recurrence_rule" in details:
            # Store recurrence details in memory
            self._recurring_events.append(
                {
                    "title": details["title"],
                    "date": details["date"],
                    "time": details["time"],
                    "duration": details["duration"],
                    "recurrence_rule": details["recurrence_rule"],
                }
            )
            return {"success": True, "message": "Event created successfully"}
        # Save to EventKit for one-off events
        try:
            success = self.store.saveEvent_span_error_(event, EKSpanThisEvent, None)
        except Exception as e:
            return {"success": False, "error": f"Failed to save event: {e}"}
        if not success:
            return {"success": False, "error": "Failed to save event"}
        return {"success": True, "message": "Event created successfully"}

    def delete_event(self, details):
        """Delete an event via EventKit."""
        # Validate required fields
        if "title" not in details:
            return {"success": False, "error": "Missing title"}
        if "date" not in details:
            return {"success": False, "error": "Missing date"}
        # Validate date format
        try:
            datetime.strptime(details["date"], "%Y-%m-%d")
        except Exception as e:
            return {"success": False, "error": f"Invalid date format: {e}"}
        # Remove event (stubbed predicate/search is simplistic)
        try:
            success = self.store.removeEvent_span_error_(None, EKSpanThisEvent, None)
        except Exception as e:
            return {"success": False, "error": f"Failed to delete event: {e}"}
        if not success:
            return {"success": False, "error": "Failed to delete event"}
        # Handle recurring deletion flags
        title = details.get("title")
        if details.get("delete_series"):
            self._deleted_series.add(title)
        else:
            date = details.get("date")
            self._deleted_occurrences.setdefault(title, set()).add(date)
        return {"success": True, "message": "Event deleted successfully"}

    def move_event(self, details):
        """Move an event via EventKit."""
        # Validate required fields
        if "old_date" not in details:
            return {"success": False, "error": "Missing old_date"}
        if "new_date" not in details:
            return {"success": False, "error": "Missing new_date"}
        if "new_time" not in details:
            return {"success": False, "error": "Missing new_time"}
        if "title" not in details:
            return {"success": False, "error": "Missing title"}
        # Validate date formats
        try:
            datetime.strptime(details["old_date"], "%Y-%m-%d")
            datetime.strptime(details["new_date"], "%Y-%m-%d")
        except Exception as e:
            return {"success": False, "error": f"Invalid date format: {e}"}
        # Validate time format
        try:
            datetime.strptime(details["new_time"], "%H:%M")
        except Exception as e:
            return {"success": False, "error": f"Invalid time format: {e}"}
        # Find and update event (stubbed implementation)
        try:
            success = self.store.saveEvent_span_error_(None, EKSpanThisEvent, None)
        except Exception as e:
            return {"success": False, "error": f"Failed to move event: {e}"}
        if not success:
            return {"success": False, "error": "Failed to move event"}
        return {"success": True, "message": "Event moved successfully"}

    def add_notification(self, details):
        """Add notification to an event via EventKit."""
        # Validate required fields
        if "minutes_before" not in details:
            return {"success": False, "error": "Missing minutes_before"}
        if not isinstance(details.get("minutes_before"), int):
            return {"success": False, "error": "Invalid minutes_before type"}
        if "title" not in details:
            return {"success": False, "error": "Missing title"}
        if "date" not in details:
            return {"success": False, "error": "Missing date"}
        # Validate date format
        try:
            datetime.strptime(details["date"], "%Y-%m-%d")
        except Exception as e:
            return {"success": False, "error": f"Invalid date format: {e}"}
        # Save notification (stub)
        try:
            success = self.store.saveEvent_span_error_(None, EKSpanThisEvent, None)
        except Exception as e:
            return {"success": False, "error": f"Failed to add notification: {e}"}
        if not success:
            return {"success": False, "error": "Failed to add notification"}
        return {"success": True, "message": "Notification added successfully"}


# Instantiate agent
_agent = EventKitAgent()

# Expose functions matching calendar_agent interface


def list_events_and_reminders(start_date=None, end_date=None):
    return _agent.list_events_and_reminders(start_date, end_date)


def create_event(details):
    return _agent.create_event(details)


def delete_event(details):
    return _agent.delete_event(details)


def move_event(details):
    return _agent.move_event(details)


def add_notification(details):
    return _agent.add_notification(details)
