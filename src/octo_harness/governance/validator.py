"""
JSON schema validator and automatic payload repair utility.
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, Optional, Tuple


class JsonValidator:
    """Validates and automatically repairs malformed JSON outputs from LLMs."""

    @classmethod
    def clean_markdown_fences(cls, text: str) -> str:
        """Strip markdown code block fences (e.g. ```json ... ```)."""
        cleaned = text.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            cleaned = "\n".join(lines).strip()
        return cleaned

    @classmethod
    def try_parse_or_repair(cls, raw_text: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        """
        Attempts to parse JSON. If failed, applies heuristic fixes:
        - strips markdown fences
        - removes trailing commas
        - extracts substring between outermost { }
        Returns: (success, parsed_dict, error_or_cleaned_text)
        """
        cleaned = cls.clean_markdown_fences(raw_text)

        # 1. Direct parse
        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, dict):
                return True, parsed, ""
        except json.JSONDecodeError:
            pass

        # 2. Extract substring between outermost braces
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            snippet = cleaned[start : end + 1]
            # Strip trailing commas before closing braces
            fixed = re.sub(r",\s*([\}\]])", r"\1", snippet)
            try:
                parsed = json.loads(fixed)
                if isinstance(parsed, dict):
                    return True, parsed, ""
            except json.JSONDecodeError as err:
                return False, None, f"JSON repair failed: {err}"

        return False, None, "No valid JSON object found in text"
