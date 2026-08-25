"""
Prompt and intent classification engine for capability-based model routing.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple
from octo_harness.models import ChatMessage, ModelCapability


class PromptClassifier:
    """
    Analyzes prompt text, message history, and requested parameters to detect
    primary capability requirements and complexity.
    """

    STRONG_CODE_KEYWORDS = {
        "def ", "class ", "fn ", "pub fn", "function(", "import ", "const ",
        "typescript", "javascript", "python", "rust", "c++", "golang", "sql query",
        "refactor", "stack trace", "traceback", "syntaxerror", "async def",
        "dockerfile", "pytest", "unit test", "regex pattern", "algorithm"
    }

    REASONING_KEYWORDS = {
        "why", "how come", "prove", "analyze", "evaluate", "compare", "critique",
        "deduce", "infer", "step by step", "rationale", "root cause", "tradeoff",
        "implications", "hypothesis", "architecture", "first principles"
    }

    MATH_KEYWORDS = {
        "calculate", "equation", "formula", "integral", "derivative", "probability",
        "statistics", "matrix", "algebra", "theorem", "variance", "standard deviation",
        "solve for x", "arithmetic"
    }

    JSON_KEYWORDS = {
        "json schema", "json object", "structured json", "json format",
        "json payload", "as a json", "in json", "key-value object"
    }

    CREATIVE_KEYWORDS = {
        "write a story", "write a poem", "write a script", "essay", "dialogue",
        "creative writing", "brainstorm", "metaphor", "fictional"
    }

    EXTRACTION_KEYWORDS = {
        "extract the", "summarize", "bullet points", "key takeaways", "tldr",
        "action items"
    }

    def classify_prompt(self, messages: List[ChatMessage]) -> Tuple[ModelCapability, float, str]:
        """
        Classifies prompt messages into a primary capability requirement with confidence score.
        Returns: (ModelCapability, confidence, reason)
        """
        if not messages:
            return ModelCapability.FAST_CHAT, 1.0, "Empty prompt defaulted to fast_chat"

        # Combine text from all messages, weighting recent user messages higher
        full_text = ""
        last_user_content = ""
        for msg in messages:
            content = msg.content or ""
            full_text += " " + content
            if msg.role in ("user", "USER"):
                last_user_content = content

        text_to_analyze = (last_user_content + " " + full_text).lower()

        # Check for structured JSON output first
        if any(k in text_to_analyze for k in self.JSON_KEYWORDS) or ("strict json" in text_to_analyze) or ("formatted as json" in text_to_analyze):
            return ModelCapability.STRUCTURED_JSON, 0.90, "JSON or schema structuring requested"

        # Check for code blocks or strong code patterns
        if "```" in text_to_analyze or any(k in text_to_analyze for k in self.STRONG_CODE_KEYWORDS):
            return ModelCapability.CODE, 0.92, "Code blocks or programming keywords detected"

        # Check for math/logic formulas
        math_matches = sum(1 for k in self.MATH_KEYWORDS if k in text_to_analyze)
        if math_matches >= 2 or re.search(r"\d+\s*[\+\-\*\/\^]\s*\d+", text_to_analyze):
            return ModelCapability.MATH, 0.88, "Mathematical formulation or calculation detected"

        # Check for deep reasoning / analysis
        reasoning_matches = sum(1 for k in self.REASONING_KEYWORDS if k in text_to_analyze)
        if reasoning_matches >= 2:
            return ModelCapability.REASONING, 0.85, "In-depth analytical or multi-step reasoning requested"

        # Check for extraction / summarization
        if any(k in text_to_analyze for k in self.EXTRACTION_KEYWORDS):
            return ModelCapability.EXTRACTION, 0.80, "Text extraction or summarization detected"

        # Check for creative writing
        if any(k in text_to_analyze for k in self.CREATIVE_KEYWORDS):
            return ModelCapability.CREATIVE, 0.80, "Creative writing or ideation requested"

        # Check length for long-context
        if len(text_to_analyze) > 20000:
            return ModelCapability.LONG_CONTEXT, 0.90, "High token volume context detected"

        # Default fast conversational chat
        return ModelCapability.FAST_CHAT, 0.75, "General conversational query"
