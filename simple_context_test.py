#!/usr/bin/env python3
"""Simple test to verify conversation context is passed to LLM."""

from unittest.mock import patch, MagicMock
import runpy


def test_context_passing():
    """Test that conversation context is passed to LLM."""
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

        # Mock input for just a few turns
        inputs = ["turn 0", "turn 1", "exit"]
        with patch("builtins.input", side_effect=inputs):
            with patch("builtins.print") as mock_print:
                # Run the main module
                runpy.run_module("main", run_name="__main__")

                # Check the calls
                calls = mock_client.chat.completions.create.call_args_list
                print(f"Number of calls: {len(calls)}")

                # Check each call
                for i, call in enumerate(calls):
                    messages = call[1]["messages"]
                    system_message = messages[0]["content"]
                    print(f"\nCall {i}:")
                    print(
                        f"Contains 'CONVERSATION CONTEXT': {'CONVERSATION CONTEXT' in system_message}"
                    )
                    print(f"Contains 'turn 0': {'turn 0' in system_message}")
                    print(f"Contains 'turn 1': {'turn 1' in system_message}")
                    print(f"System message length: {len(system_message)}")


if __name__ == "__main__":
    test_context_passing()
