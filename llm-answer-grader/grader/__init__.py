"""llm-answer-grader — give every AI answer a report card.

Offline, deterministic, zero-dependency rubric scoring for LLM outputs.
"""

from .scorer import Card, DimensionResult, Finding, evaluate, evaluate_many, grade_for

__version__ = "0.1.0"
__all__ = ["Card", "DimensionResult", "Finding", "evaluate", "evaluate_many", "grade_for", "__version__"]
