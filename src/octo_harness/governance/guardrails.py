"""
Guardrails and content safety inspection for inputs and outputs.
"""

from __future__ import annotations

import re
from typing import List, Optional, Tuple


class ContentGuardrails:
    """
    Detects security risks, prompt injection attempts, and scrubs sensitive API keys.
    """

    INJECTION_PATTERNS = [
        re.compile(r"ignore\s+(all\s+)?(previous|prior)\s+instructions", re.IGNORECASE),
        re.compile(r"disregard\s+(all\s+)?.*(safety|system|rules|instructions)", re.IGNORECASE),
        re.compile(r"you\s+are\s+now\s+(DAN|jailbroken|unrestricted)", re.IGNORECASE),
        re.compile(r"system\s*:\s*override", re.IGNORECASE),
        re.compile(r"<\|im_start\|>", re.IGNORECASE),
    ]

    SECRET_PATTERNS = [
        re.compile(r"sk-[a-zA-Z0-9_\-]{20,60}"),                    # OpenAI key
        re.compile(r"xai-[a-zA-Z0-9_\-]{20,60}"),                   # xAI Grok key
        re.compile(r"ant-[a-zA-Z0-9_\-]{20,60}"),                   # Anthropic key
        re.compile(r"AKIA[0-9A-Z]{16}"),                           # AWS Access Key
        re.compile(r"ghp_[a-zA-Z0-9]{36}"),                        # GitHub Personal Token
        re.compile(r"-----BEGIN (RSA|EC|PRIVATE) KEY-----"),        # Private keys
    ]

    @classmethod
    def check_prompt_injection(cls, text: str) -> Tuple[bool, Optional[str]]:
        """Scan for prompt injection signatures."""
        for pat in cls.INJECTION_PATTERNS:
            if pat.search(text):
                return True, f"Prompt injection pattern detected: '{pat.pattern}'"
        return False, None

    @classmethod
    def scrub_secrets(cls, text: str) -> str:
        """Mask detected API keys and secrets with [REDACTED_SECRET]."""
        sanitized = text
        for pat in cls.SECRET_PATTERNS:
            sanitized = pat.sub("[REDACTED_SECRET]", sanitized)
        return sanitized
