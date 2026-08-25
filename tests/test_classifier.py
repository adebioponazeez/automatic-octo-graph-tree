"""
Tests for prompt intent classification.
"""

from octo_harness.models import ChatMessage, ChatRole, ModelCapability
from octo_harness.router.classifier import PromptClassifier


def test_classifier_code_intent():
    classifier = PromptClassifier()
    messages = [
        ChatMessage(
            role=ChatRole.USER,
            content="Can you refactor this python async function to fix the race condition? def process():",
        )
    ]
    intent, conf, reason = classifier.classify_prompt(messages)
    assert intent == ModelCapability.CODE
    assert conf > 0.8


def test_classifier_math_intent():
    classifier = PromptClassifier()
    messages = [
        ChatMessage(
            role=ChatRole.USER,
            content="Please calculate the derivative of the matrix equation f(x) = 3 * x^2 + 5 * x",
        )
    ]
    intent, conf, reason = classifier.classify_prompt(messages)
    assert intent == ModelCapability.MATH


def test_classifier_json_intent():
    classifier = PromptClassifier()
    messages = [
        ChatMessage(
            role=ChatRole.USER,
            content="Extract the user attributes and return them formatted as a strict JSON schema object",
        )
    ]
    intent, conf, reason = classifier.classify_prompt(messages)
    assert intent == ModelCapability.STRUCTURED_JSON


def test_classifier_reasoning_intent():
    classifier = PromptClassifier()
    messages = [
        ChatMessage(
            role=ChatRole.USER,
            content="Prove from first principles why this architecture has higher fault tolerance and analyze the tradeoffs",
        )
    ]
    intent, conf, reason = classifier.classify_prompt(messages)
    assert intent == ModelCapability.REASONING


def test_classifier_fast_chat_default():
    classifier = PromptClassifier()
    messages = [
        ChatMessage(role=ChatRole.USER, content="Hello! How are you doing today?")
    ]
    intent, conf, reason = classifier.classify_prompt(messages)
    assert intent == ModelCapability.FAST_CHAT
