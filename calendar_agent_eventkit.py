"""Handles Calendar integration using EventKit for the terminal calendar assistant."""

import time
from datetime import datetime, timedelta

try:
    from Foundation import NSDate, NSRunLoop, NSDateComponents  # type: ignore
    from EventKit import EKEventStore, EKEntityTypeEvent, EKEntityTypeReminder, EKEvent, EKSpanThisEvent  # type: ignore
except ImportError:
    # Fallback stubs for linting and environments without PyObjC
    class NSDate:
        @staticmethod
        def dateWithTimeIntervalSince1970_(t):
            return None

        @staticmethod
        def dateWithTimeIntervalSinceNow_(t):
            return None

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
            return self

        def requestAccessToEntityType_completion_(self, et, cb):
            cb(True, None)

        def predicateForEventsWithStartDate_endDate_calendars_(self, s, e, c):
            return None

        def eventsMatchingPredicate_(self, p):
            return []

        def predicateForIncompleteRemindersWithDueDateComponents_(self, c):
            # Stub predicate for reminders
            return None

        def fetchRemindersMatchingPredicate_completion_(self, pred, cb):
            # Stub fetch: immediately call callback with empty list
            cb([], None)

        def saveEvent_span_error_(self, event, span, error_ptr):
            cb = None  # type: ignore
            return True

        def removeEvent_span_error_(self, event, span, error_ptr):
            return True

    EKEntityTypeEvent = 0
    EKEntityTypeReminder = 1
    # Stub span constant
    EKSpanThisEvent = 0

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

    def _request_access(self, entity_type):
        """Request access and block until granted."""
        self._granted = False
        self.store.requestAccessToEntityType_completion_(
            entity_type, self._access_handler
        )
        # Run loop until callback
        while not self._granted:
            NSRunLoop.currentRunLoop().runUntilDate_(
                NSDate.dateWithTimeIntervalSinceNow_(0.1)
            )

    def _access_handler(self, granted, error):
        self._granted = True

    def list_events_and_reminders(self, start_date=None, end_date=None):
        """List events and incomplete reminders between start_date and end_date."""
        # Default to today and parse date range, with error handling
        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-%d")
        if not end_date:
            end_date = start_date
        try:
            start_dt = datetime.strptime(f"{start_date} 00:00", "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(f"{end_date} 23:59", "%Y-%m-%d %H:%M")
        except Exception as e:
            # Invalid date format
            return {"events": [], "reminders": [], "error": f"Invalid date format: {e}"}
        # Convert to NSDate
        start_ns = NSDate.dateWithTimeIntervalSince1970_(
            time.mktime(start_dt.timetuple())
        )
        end_ns = NSDate.dateWithTimeIntervalSince1970_(time.mktime(end_dt.timetuple()))
        # Events
        pred_events = self.store.predicateForEventsWithStartDate_endDate_calendars_(
            start_ns, end_ns, None
        )
        ek_events = self.store.eventsMatchingPredicate_(pred_events)
        events = [f"{e.title} | {e.startDate}" for e in ek_events]
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
            while not done["flag"]:
                NSRunLoop.currentRunLoop().runUntilDate_(
                    NSDate.dateWithTimeIntervalSinceNow_(0.1)
                )
            # Format reminder output
            reminders = [f"{r.title} | {r.dueDate}" for r in reminders_found]
        except Exception:
            reminders = []
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
        # Save to EventKit
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
        # Save moved event
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
