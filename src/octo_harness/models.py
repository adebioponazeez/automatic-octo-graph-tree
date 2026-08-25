"""
Core domain models and Pydantic schemas for Octo Harness.
"""

from __future__ import annotations

import time
import uuid
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class ChatRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"
    TOOL = "tool"


class ModelCapability(str, Enum):
    CODE = "code"
    REASONING = "reasoning"
    FAST_CHAT = "fast_chat"
    MULTIMODAL = "multimodal"
    STRUCTURED_JSON = "structured_json"
    LONG_CONTEXT = "long_context"
    CREATIVE = "creative"
    MATH = "math"
    EXTRACTION = "extraction"


class ProviderType(str, Enum):
    GROK = "grok"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OPENROUTER = "openrouter"
    LOCAL = "local"
    MOCK = "mock"


class RoutingStrategy(str, Enum):
    GROK_PRIMARY = "grok_primary"
    QUALITY_FIRST = "quality_first"
    COST_OPTIMIZED = "cost_optimized"
    LATENCY_OPTIMIZED = "latency_optimized"
    ROUND_ROBIN = "round_robin"
    FALLBACK_CASCADE = "fallback_cascade"
    CUSTOM = "custom"


class ToolCallFunction(BaseModel):
    name: str
    arguments: str


class ToolCall(BaseModel):
    id: str = Field(default_factory=lambda: f"call_{uuid.uuid4().hex[:8]}")
    type: str = "function"
    function: ToolCallFunction


class ChatMessage(BaseModel):
    role: Union[ChatRole, str] = ChatRole.USER
    content: Optional[str] = ""
    name: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    tool_call_id: Optional[str] = None

    def to_provider_dict(self) -> Dict[str, Any]:
        """Convert to standard message dict for upstream LLM APIs."""
        data: Dict[str, Any] = {
            "role": self.role.value if isinstance(self.role, ChatRole) else str(self.role),
            "content": self.content or "",
        }
        if self.name:
            data["name"] = self.name
        if self.tool_calls:
            data["tool_calls"] = [tc.model_dump() for tc in self.tool_calls]
        if self.tool_call_id:
            data["tool_call_id"] = self.tool_call_id
        return data


class ModelSpec(BaseModel):
    model_id: str
    provider_type: ProviderType
    display_name: str
    capabilities: List[ModelCapability] = Field(default_factory=list)
    context_window: int = 128000
    input_cost_per_million: float = 2.00  # in USD per 1M tokens
    output_cost_per_million: float = 10.00  # in USD per 1M tokens
    max_tokens: int = 4096
    average_latency_ms: float = 450.0
    is_active: bool = True
    description: str = ""

    def calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate USD cost given token counts."""
        input_cost = (prompt_tokens / 1_000_000.0) * self.input_cost_per_million
        output_cost = (completion_tokens / 1_000_000.0) * self.output_cost_per_million
        return round(input_cost + output_cost, 6)


class UsageInfo(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0


class Choice(BaseModel):
    index: int = 0
    message: ChatMessage
    finish_reason: Optional[str] = "stop"


class CompletionRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = None
    strategy: RoutingStrategy = RoutingStrategy.GROK_PRIMARY
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: Optional[float] = 1.0
    max_tokens: Optional[int] = 2048
    stream: bool = False
    tools: Optional[List[Dict[str, Any]]] = None
    response_format: Optional[Dict[str, Any]] = None
    fallback_models: Optional[List[str]] = None
    allow_fallback: bool = True
    timeout_seconds: float = 30.0
    required_capabilities: Optional[List[ModelCapability]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RouteDecision(BaseModel):
    primary_model: str
    primary_provider: ProviderType
    fallback_chain: List[str] = Field(default_factory=list)
    strategy: RoutingStrategy
    detected_intent: ModelCapability = ModelCapability.FAST_CHAT
    confidence: float = 1.0
    estimated_cost_usd: float = 0.0
    reason: str = ""
    timestamp: float = Field(default_factory=time.time)


class CompletionResponse(BaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-{uuid.uuid4().hex[:12]}")
    object: str = "chat.completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    provider: ProviderType
    choices: List[Choice]
    usage: UsageInfo = Field(default_factory=UsageInfo)
    latency_ms: float = 0.0
    route_decision: Optional[RouteDecision] = None
    fallback_occurred: bool = False
    fallback_history: List[str] = Field(default_factory=list)

    @property
    def content(self) -> str:
        """Helper to get primary text content."""
        if self.choices and self.choices[0].message.content:
            return self.choices[0].message.content
        return ""


class ProviderHealth(BaseModel):
    provider_name: str
    provider_type: ProviderType
    status: str = "healthy"  # "healthy", "degraded", "down", "offline"
    latency_ms: float = 0.0
    last_checked: float = Field(default_factory=time.time)
    error_rate: float = 0.0
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    circuit_breaker_state: str = "CLOSED"  # "CLOSED", "OPEN", "HALF_OPEN"
    models_available: List[str] = Field(default_factory=list)


class CoworkTaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class CoworkTask(BaseModel):
    id: str = Field(default_factory=lambda: f"task-{uuid.uuid4().hex[:6]}")
    name: str
    description: str
    assigned_role: str  # "planner", "coder", "critic", "synthesizer", "auditor"
    dependencies: List[str] = Field(default_factory=list)
    status: CoworkTaskStatus = CoworkTaskStatus.PENDING
    result: Optional[str] = None
    model_used: Optional[str] = None
    provider_used: Optional[str] = None
    execution_time_s: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)
