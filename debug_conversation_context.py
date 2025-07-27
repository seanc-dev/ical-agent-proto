#!/usr/bin/env python3
"""Debug script to understand conversation context issues."""

from unittest.mock import patch, MagicMock
import runpy
from core.conversation_manager import ConversationState


def debug_conversation_context():
    """Debug the conversation context issue."""
    with patch("openai_client.client") as mock_client:
        # Mock responses
        mock_response = MagicMock()
        mock_message = MagicMock()
        mock_function_call = MagicMock()
        mock_function_call.name = "list_all"
        mock_function_call.arguments = "{}"
        mock_message.function_call = mock_function_call
        mock_response.choices = [mock_message]
        mock_client.chat.completions.create.return_value = mock_response

        # Mock input for a few turns
        inputs = ["turn 0", "turn 1", "turn 2", "exit"]
        with patch("builtins.input", side_effect=inputs):
            with patch("builtins.print") as mock_print:
                # Run the main module
                runpy.run_module("main", run_name="__main__")

                # Check the calls
                calls = mock_client.chat.completions.create.call_args_list
                print(f"Number of calls: {len(calls)}")

                for i, call in enumerate(calls):
                    messages = call[1]["messages"]
                    system_message = messages[0]["content"]
                    print(f"\nCall {i}:")
                    print(
                        f"System message contains 'CONVERSATION CONTEXT': {'CONVERSATION CONTEXT' in system_message}"
                    )
                    print(
                        f"System message contains 'turn 0': {'turn 0' in system_message}"
                    )
                    print(
                        f"System message contains 'turn 1': {'turn 1' in system_message}"
                    )
                    print(
                        f"System message contains 'turn 2': {'turn 2' in system_message}"
                    )
                    print(f"System message length: {len(system_message)}")
                    print(f"First 200 chars: {system_message[:200]}...")


if __name__ == "__main__":
    debug_conversation_context()
