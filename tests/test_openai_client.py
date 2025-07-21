import types
import builtins

import openai_client


def test_interpret_command_no_api_key(monkeypatch):
    monkeypatch.setattr(openai_client, "client", None)
    result = openai_client.interpret_command("hi")
    assert result["action"] == "error"


class FakeMessage:
    def __init__(self, name, arguments):
        self.function_call = types.SimpleNamespace(name=name, arguments=arguments)

class FakeResponse:
    def __init__(self, message):
        self.choices = [types.SimpleNamespace(message=message)]

class FakeCompletions:
    def __init__(self, response):
        self._response = response

    def create(self, *args, **kwargs):
        return self._response

class FakeChat:
    def __init__(self, response):
        self.completions = FakeCompletions(response)

class FakeClient:
    def __init__(self, response):
        self.chat = FakeChat(response)


def test_interpret_command_success(monkeypatch):
    message = FakeMessage("list_all", "{}")
    response = FakeResponse(message)
    fake_client = FakeClient(response)
    monkeypatch.setattr(openai_client, "client", fake_client)
    result = openai_client.interpret_command("show events")
    assert result == {"action": "list_all", "details": {}}


def test_interpret_command_add_notification(monkeypatch):
    message = FakeMessage("add_notification", '{"title":"Meet","date":"2024-08-01"}')
    response = FakeResponse(message)
    fake_client = FakeClient(response)
    monkeypatch.setattr(openai_client, "client", fake_client)
    result = openai_client.interpret_command("remind me")
    assert result["action"] == "add_notification"
    assert result["details"]["title"] == "Meet"

def test_interpret_command_unknown(monkeypatch):
    message = types.SimpleNamespace(function_call=None)
    response = FakeResponse(message)
    fake_client = FakeClient(response)
    monkeypatch.setattr(openai_client, "client", fake_client)
    result = openai_client.interpret_command("hello")
    assert result == {"action": "unknown", "details": "hello"}


def test_interpret_command_exception(monkeypatch):
    class ErrorCompletions:
        def create(self, *args, **kwargs):
            raise RuntimeError("boom")
    fake_client = types.SimpleNamespace(chat=types.SimpleNamespace(completions=ErrorCompletions()))
    monkeypatch.setattr(openai_client, "client", fake_client)
    result = openai_client.interpret_command("hi")
    assert result["action"] == "error"
    assert "boom" in result["details"]
