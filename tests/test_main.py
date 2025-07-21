import sys
import builtins
import runpy
import types

import openai_client


def test_main_exits_without_calling_openai(monkeypatch):
    inputs = ["exit"]
    def fake_input(prompt=""):
        return inputs.pop(0)
    monkeypatch.setitem(sys.modules, "dotenv", types.SimpleNamespace(load_dotenv=lambda: None))
    printed = []
    def fake_print(*args, **kwargs):
        printed.append(" ".join(str(a) for a in args))
    called = {"interpret": False}
    def fake_interpret(cmd):
        called["interpret"] = True
        return {}
    monkeypatch.setattr(builtins, "input", fake_input)
    monkeypatch.setattr(builtins, "print", fake_print)
    monkeypatch.setattr(openai_client, "interpret_command", fake_interpret)

    runpy.run_module("main", run_name="__main__")

    assert any("Welcome to the Terminal Calendar Assistant" in p for p in printed)
    assert any("Goodbye!" in p for p in printed)
    assert not called["interpret"]

