#!/usr/bin/env python3
"""Debug script for the failing conversation context limits test."""

from unittest.mock import patch, MagicMock
import runpy


def debug_failing_test():
    """Debug the failing test specifically."""
    with patch("openai_client.client") as mock_client:
        # Mock responses - same as the failing test
        mock_response = MagicMock()
        mock_message = MagicMock()
        mock_function_call = MagicMock()
        mock_function_call.name = "list_all"
        mock_function_call.arguments = "{}"
        mock_message.function_call = mock_function_call
        mock_response.choices = [mock_message]
        mock_client.chat.completions.create.return_value = mock_response

        # Mock input for many turns (more than the default limit of 10)
        many_inputs = [f"turn {i}" for i in range(15)] + ["exit"]
        with patch("builtins.input", side_effect=many_inputs):
            with patch("builtins.print") as mock_print:
                # Run the main module
                runpy.run_module("main", run_name="__main__")

                # Check the calls
                calls = mock_client.chat.completions.create.call_args_list
                print(f"Number of calls: {len(calls)}")

                # Check the last call specifically
                if calls:
                    later_call = calls[-1]
                    messages = later_call[1]["messages"]
                    system_message = messages[0]["content"]
                    print(f"\nLast call system message:")
                    print(
                        f"Contains 'CONVERSATION CONTEXT': {'CONVERSATION CONTEXT' in system_message}"
                    )
                    print(f"Contains 'turn 14': {'turn 14' in system_message}")
                    print(f"Contains 'User:': {'User:' in system_message}")
                    print(f"Contains 'Assistant:': {'Assistant:' in system_message}")
                    print(f"System message length: {len(system_message)}")
                    print(f"System message: {system_message}")


if __name__ == "__main__":
    debug_failing_test()
