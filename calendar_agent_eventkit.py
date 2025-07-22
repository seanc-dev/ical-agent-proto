"""Handles Calendar integration using EventKit for the terminal calendar assistant."""

import time
from datetime import datetime

try:
    from Foundation import NSDate, NSRunLoop  # type: ignore
    from EventKit import EKEventStore, EKEntityTypeEvent, EKEntityTypeReminder  # type: ignore
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

    EKEntityTypeEvent = 0
    EKEntityTypeReminder = 1

    # No-op predicate for reminders
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
        # For simplicity, return empty list for now
        reminders = []
        return {"events": events, "reminders": reminders}

    def create_event(self, details):
        """Stub for event creation via EventKit."""
        if "duration" not in details:
            return {"success": False, "error": "Missing duration"}
        return {"success": False, "error": "Not implemented"}

    def delete_event(self, details):
        """Stub for event deletion via EventKit."""
        return {"success": False, "error": "Not implemented"}

    def move_event(self, details):
        """Stub for moving events via EventKit."""
        return {"success": False, "error": "Not implemented"}

    def add_notification(self, details):
        """Stub for adding notifications via EventKit."""
        return {"success": False, "error": "Not implemented"}


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
