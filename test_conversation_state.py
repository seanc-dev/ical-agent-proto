#!/usr/bin/env python3
"""Simple test to verify conversation state functionality."""

from core.conversation_manager import ConversationState


def test_conversation_state():
    """Test conversation state functionality."""
    state = ConversationState()

    # Add some turns
    state.append_turn("turn 0", "list_all", {})
    state.append_turn("turn 1", "list_all", {})
    state.append_turn("turn 2", "list_all", {})

    # Get context
    context = state.get_context_for_llm_prompt()
    print(f"Context: {context}")
    print(f"Contains 'turn 0': {'turn 0' in context}")
    print(f"Contains 'turn 1': {'turn 1' in context}")
    print(f"Contains 'turn 2': {'turn 2' in context}")
    print(f"Contains 'User:': {'User:' in context}")
    print(f"Contains 'Assistant:': {'Assistant:' in context}")


if __name__ == "__main__":
    test_conversation_state()
