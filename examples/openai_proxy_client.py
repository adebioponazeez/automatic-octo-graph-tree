"""
Example demonstrating how to use the standard OpenAI Python client library
pointing directly to the Octo Harness Proxy Endpoint.
"""

import httpx


def test_openai_compatible_endpoint():
    print("[*] Sending request to Octo Harness OpenAI-compatible proxy (http://localhost:8000/v1)...")

    # Standard OpenAI chat completions payload
    payload = {
        "model": "grok-2-latest",
        "strategy": "grok_primary",
        "messages": [
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": "Write a quicksort algorithm in Python."},
        ],
        "temperature": 0.5,
    }

    try:
        response = httpx.post(
            "http://localhost:8000/v1/chat/completions",
            json=payload,
            timeout=30.0,
        )
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        print(response.json())
    except Exception as exc:
        print(f"Failed to connect to local server: {exc}")
        print("Make sure server is running via `octo-harness serve` or `make serve`")


if __name__ == "__main__":
    test_openai_compatible_endpoint()
