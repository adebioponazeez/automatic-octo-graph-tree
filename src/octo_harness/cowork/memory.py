"""
Shared Blackboard Memory and Session Context for Multi-Agent Cowork Harness.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class MemoryEntry(BaseModel):
    key: str
    value: Any
    author_agent: str
    timestamp: float = Field(default_factory=time.time)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CoworkMemory:
    """
    Central blackboard memory for agents in a Cowork workflow to exchange intermediate
    artifacts, verification notes, and decision logs.
    """

    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or f"session-{int(time.time())}"
        self._entries: Dict[str, MemoryEntry] = {}
        self._execution_log: List[str] = []

    def set(self, key: str, value: Any, author_agent: str = "system", metadata: Optional[Dict[str, Any]] = None) -> None:
        """Store a key-value artifact in shared memory."""
        self._entries[key] = MemoryEntry(
            key=key,
            value=value,
            author_agent=author_agent,
            metadata=metadata or {},
        )
        self.log(f"Agent [{author_agent}] updated key '{key}'")

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve value by key from memory."""
        entry = self._entries.get(key)
        return entry.value if entry else default

    def get_entry(self, key: str) -> Optional[MemoryEntry]:
        """Retrieve full memory entry object."""
        return self._entries.get(key)

    def contains(self, key: str) -> bool:
        """Check if key exists in memory."""
        return key in self._entries

    def log(self, message: str) -> None:
        """Append an event to execution log."""
        timestamp_str = time.strftime("%H:%M:%S", time.localtime())
        self._execution_log.append(f"[{timestamp_str}] {message}")

    def get_logs(self) -> List[str]:
        """Return full execution log."""
        return list(self._execution_log)

    def snapshot(self) -> Dict[str, Any]:
        """Export snapshot of memory state."""
        return {
            "session_id": self.session_id,
            "entries_count": len(self._entries),
            "keys": list(self._entries.keys()),
            "logs": self._execution_log,
        }

    def clear(self) -> None:
        """Clear memory state."""
        self._entries.clear()
        self._execution_log.clear()
