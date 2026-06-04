"""
Configuration for the AI Assistant.
Loads API keys from .env and defines model defaults and pricing.
"""

import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY:
    raise ValueError(
        "ANTHROPIC_API_KEY not found. "
        "Create a .env file with your key. See .env.example for reference."
    )

MODEL_NAME = "claude-haiku-4-5-20251001"
MAX_TOKENS = 1024
COST_PER_MILLION_INPUT = 0.80   # Haiku 4.5 input: $0.80/MTok
COST_PER_MILLION_OUTPUT = 4.00  # Haiku 4.5 output: $4.00/MTok
