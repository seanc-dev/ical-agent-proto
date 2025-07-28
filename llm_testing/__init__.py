"""LLM-to-LLM Testing Framework for Calendar Assistant."""

from .config import TestingConfig
from .personas import Persona
from .scenarios import Scenario
from .prompts import TestPrompt, PromptTemplate
from .evaluator import ScoringAgent
from .evaluation_loop import EvaluationLoop
from .meta_tracker import MetaTracker

__version__ = "0.1.0"
__all__ = [
    "TestingConfig",
    "Persona",
    "Scenario",
    "TestPrompt",
    "PromptTemplate",
    "ScoringAgent",
    "EvaluationLoop",
    "MetaTracker",
]
