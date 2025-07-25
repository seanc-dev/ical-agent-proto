"""Command dispatcher for main loop actions."""

HANDLERS = {}


def dispatch(action: str, details: dict):
    """Dispatch the given action to the appropriate handler."""
    if action not in HANDLERS:
        raise KeyError(f"Unknown action: {action}")
    return HANDLERS[action](details)
