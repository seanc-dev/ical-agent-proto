#!/usr/bin/env python3

from unittest.mock import patch, MagicMock
import openai_client


def test_debug():
    """Debug the mock setup."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_message = MagicMock()
    mock_function_call = MagicMock()

    # Configure the mock to return the correct values
    mock_function_call.configure_mock(name="list_all", arguments="{}")
    mock_message.configure_mock(function_call=mock_function_call)
    mock_response.configure_mock(choices=[mock_message])
    mock_client.chat.completions.create.return_value = mock_response

    with patch("openai_client.client", mock_client):
        result = openai_client.interpret_command("test", "")
        print("Result:", result)
        print("Expected action: list_all")
        print("Actual action:", result.get("action"))
        print("Action type:", type(result.get("action")))
        print("Mock function_call.name:", mock_function_call.name)
        print("Mock function_call.name type:", type(mock_function_call.name))


if __name__ == "__main__":
    test_debug()
