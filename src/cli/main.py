"""
Personal AI Assistant — CLI Version
Sprint 1: API-Call 
"""

from anthropic import Anthropic
from .config import ANTHROPIC_API_KEY, MODEL_NAME, MAX_TOKENS


def first_api_call():
    """
    First API Call to Claude. 
    Send request and get response.
    """
    # Create Client - connect to API
    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    # Send request to API
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=MAX_TOKENS,
        messages=[
            {
                "role": "user",
                "content": "Hello, Claude! What is REST?"
            }
        ]
    )

    # Print response
    print("=" * 50)
    print("Claude's response:")
    print("=" * 50)
    print(response.content[0].text)
    print("=" * 50)

    #Show Metadata   print("Response Metadata:")
    print(f"Model: {response.model}")
    print(f"Tokens Used: {response.usage.input_tokens + response.usage.output_tokens}")
    print(f"Output Tokens: {response.usage.output_tokens}")  
    print(f"Stop Reason: {response.stop_reason}")

if __name__ == "__main__":
    first_api_call()

