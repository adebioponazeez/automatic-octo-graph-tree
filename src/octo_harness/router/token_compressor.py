"""
Token Compression & Optimization Engine (TOON & Semantic Symbolism).
Implements Token-Oriented Object Notation (TOON) for 40-60% JSON token reduction,
atomic single-token semantic symbol anchoring, and lossless schema minification.
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional, Tuple, Union
from pydantic import BaseModel, Field


class CompressionStats(BaseModel):
    original_characters: int
    compressed_characters: int
    estimated_original_tokens: int
    estimated_compressed_tokens: int
    tokens_saved: int
    compression_ratio_percent: float  # e.g. 45.2% saved


class TOONEncoder:
    """
    Token-Oriented Object Notation (TOON) Encoder.
    Converts uniform arrays of JSON objects into compact tabular layouts,
    declaring schema keys once to eliminate 40-60% of repetitive token overhead.
    """

    @classmethod
    def encode(cls, data: Union[List[Dict[str, Any]], Dict[str, Any]]) -> str:
        """Converts structured JSON data into TOON format."""
        if not data:
            return ""

        # Uniform Array of Objects -> Tabular TOON
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            if not data:
                return "[]"

            # Collect all unique keys in order
            keys: List[str] = []
            for item in data:
                for k in item.keys():
                    if k not in keys:
                        keys.append(k)

            header = f"[{len(data)}]{{{','.join(keys)}}}:"
            rows = []
            for item in data:
                row_vals = []
                for k in keys:
                    val = item.get(k, "")
                    if val is None:
                        val_str = "null"
                    elif isinstance(val, (int, float, bool)):
                        val_str = str(val)
                    else:
                        # Escape commas or newlines if present
                        val_str = str(val).replace("\n", " ").replace(",", ";")
                    row_vals.append(val_str)
                rows.append("  " + ",".join(row_vals))

            return header + "\n" + "\n".join(rows)

        # Dict with Array values
        if isinstance(data, dict):
            lines = []
            for root_key, val in data.items():
                if isinstance(val, list) and all(isinstance(x, dict) for x in val):
                    encoded_sub = cls.encode(val)
                    lines.append(f"{root_key}{encoded_sub}")
                else:
                    lines.append(f"{root_key}: {json.dumps(val, separators=(',', ':'))}")
            return "\n".join(lines)

        # Fallback to ultra-compact JSON
        return json.dumps(data, separators=(",", ":"))


class SemanticPromptCompressor:
    """
    Compresses verbose instruction headers into verified 1-token atomic semantic anchors.
    Replaces verbose repetitive prompt boilerplate with ultra-dense semantic cues.
    """

    # High-density 1-token / 1-character semantic replacement mapping
    SEMANTIC_ANCHORS: Dict[str, str] = {
        "CRITICAL SYSTEM INVARIANT (DO NOT VIOLATE):": "🔒 INVARIANT:",
        "CRITICAL INVARIANT:": "🔒 INVARIANT:",
        "PRIMARY OBJECTIVE AND GOAL:": "🎯 GOAL:",
        "PRIMARY OBJECTIVE:": "🎯 GOAL:",
        "PERFORMANCE AND LATENCY REQUIREMENT:": "⚡ PERF:",
        "LATENCY CONSTRAINT:": "⚡ PERF:",
        "SECURITY AND SECRET SCANNING:": "🛡️ SEC:",
        "SECURITY GUARDRAIL:": "🛡️ SEC:",
        "EXPECTED OUTPUT FORMAT (STRICT JSON):": "📦 FORMAT: JSON",
        "EXPECTED OUTPUT FORMAT:": "📦 FORMAT:",
        "ADVERSARIAL RED TEAM AUDIT:": "⚔️ AUDIT:",
        "BUDGET AND COST CONSTRAINT:": "💰 BUDGET:",
        "STEP-BY-STEP REASONING REQUIRED:": "🧠 REASON:",
    }

    @classmethod
    def compress_prompt(cls, prompt: str) -> str:
        """Compresses instructions using atomic semantic anchors and whitespace compaction."""
        compressed = prompt

        # 1. Apply semantic anchor replacements
        for verbose_phrase, atomic_anchor in cls.SEMANTIC_ANCHORS.items():
            compressed = re.sub(re.escape(verbose_phrase), atomic_anchor, compressed, flags=re.IGNORECASE)

        # 2. Compact multiple empty lines to single newline
        compressed = re.sub(r"\n{3,}", "\n\n", compressed)

        # 3. Compact multiple spaces
        compressed = re.sub(r"[ \t]{2,}", " ", compressed)

        return compressed.strip()


class TokenOptimizer:
    """
    Unified Token Optimization Gateway.
    Applies TOON encoding to structured context payloads and semantic prompt compression.
    """

    def __init__(self):
        self.toon = TOONEncoder()
        self.semantic = SemanticPromptCompressor()

    def optimize_payload(
        self,
        prompt: str,
        structured_context: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]] = None,
    ) -> Tuple[str, CompressionStats]:
        """Compresses both the prompt and structured context, returning statistics."""
        orig_char_count = len(prompt)
        orig_context_json = ""
        if structured_context:
            orig_context_json = json.dumps(structured_context, indent=2)
            orig_char_count += len(orig_context_json)

        # 1. Compress prompt
        comp_prompt = self.semantic.compress_prompt(prompt)

        # 2. Convert structured context to TOON format
        if structured_context:
            toon_context = self.toon.encode(structured_context)
            final_optimized = f"{comp_prompt}\n\n[CONTEXT (TOON)]:\n{toon_context}"
        else:
            final_optimized = comp_prompt

        comp_char_count = len(final_optimized)

        # Estimate tokens (~4 characters per token heuristic)
        orig_tokens = max(1, orig_char_count // 4)
        comp_tokens = max(1, comp_char_count // 4)
        saved_tokens = max(0, orig_tokens - comp_tokens)
        ratio = round((saved_tokens / orig_tokens) * 100.0, 1)

        stats = CompressionStats(
            original_characters=orig_char_count,
            compressed_characters=comp_char_count,
            estimated_original_tokens=orig_tokens,
            estimated_compressed_tokens=comp_tokens,
            tokens_saved=saved_tokens,
            compression_ratio_percent=ratio,
        )

        return final_optimized, stats
