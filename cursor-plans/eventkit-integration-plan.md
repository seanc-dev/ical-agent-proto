# EventKit Integration Testing Plan

## 1. Listing Events After Creation

- 1.1 Test that listing events returns only events within specified date range (default today)
- 1.2 Test that creating an event results in it being listed when listing events for that date

## 2. Event Creation Behavior

- 2.1 Test missing required fields errors (title, date, time, duration)
- 2.2 Test invalid date/time formats produce an error

## 3. Cleanup and Teardown

- 3.1 Delete created events after tests to avoid polluting the calendar

## 4. Edge Cases and Errors

- 4.1 Test listing invalid date ranges returns an error
- 4.2 Test that no events are returned when calendar is empty for a given range
