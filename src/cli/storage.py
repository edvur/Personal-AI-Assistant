"""
Speicher-Modul: Gespräche als JSON-Dateien speichern und laden.

Dateiformat:
{
    "id": "chat_20260604_143052",
    "created_at": "2026-06-04T14:30:52",
    "system_prompt": "Du bist...",
    "messages": [...],
    "stats": {
        "total_input_tokens": 1234,
        "total_output_tokens": 567,
        "total_cost_usd": 0.003
    }
}
"""

import json
import os
from datetime import datetime
from pathlib import Path


#folder for saved chats
CHAT_DIR = Path(__file__).parent.parent.parent / "data" / "saved_chats"

def ensure_chat_dir():
    """Ensure the chat directory exists."""
    if not CHAT_DIR.exists():
        CHAT_DIR.mkdir(parents=True, exist_ok=True)

def generate_chat_id() -> str:
    """
    Generate a unique chat ID based on timestamp.
    Format: chat_YYYYMMDD_HHMMSS
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    return f"chat_{timestamp}"

def save_chat(chat_data: dict) -> str:
    """
    Save a chat session to a JSON file.
    
    Args:
        chat_data: A dictionary containing chat information (id, system_prompt, messages, stats).
    
    Returns:
        The file path where the chat was saved.
    """
    ensure_chat_dir()
    
    chat_id = chat_data.get("id", generate_chat_id())
    file_path = CHAT_DIR / f"{chat_id}.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(chat_data, f, indent=4, ensure_ascii=False)
    
    return str(file_path)

def load_chat(chat_id: str) -> dict:
    """
    Load a chat session from a JSON file.

    Args:
        chat_id: The ID of the chat to load (without .json extension).

    Returns:
        A dictionary containing the chat data.

    Raises:
        FileNotFoundError: If the specified chat file does not exist.
    """
    file_path = CHAT_DIR / f"{chat_id}.json"

    if not file_path.exists():
        raise FileNotFoundError(f"Chat '{chat_id}' not found in {CHAT_DIR}.")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
    

def list_saved_chats() -> list[dict]:
    """
    List all saved chat sessions.
    
    Returns:
        A list of dictionaries, each containing 'id' and 'created_at' of a chat session.
    """
    ensure_chat_dir()
    
    chats = []
    for file in CHAT_DIR.glob("chat_*.json"):
        try: 
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                chats.append({
                    "id": data.get("id"),
                    "created_at": data.get("created_at"),
                    "message_count": len(data.get("messages", [])),
                    "cost_usd": data.get("stats", {}).get("total_cost_usd", 0)
                })
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading chat file {file}: {e}")
    
    return sorted(chats, key=lambda x: x["created_at"], reverse=True)

def delete_chat(chat_id: str) -> bool:
    """
    Delete a saved chat session by its ID.
    
    Args:
        chat_id: The ID of the chat to delete.
    
    Returns:
        True if the chat was successfully deleted, False otherwise.
    """
    file_path = CHAT_DIR / f"{chat_id}.json"
    
    if file_path.exists():
        file_path.unlink()
        return True
    else:
        print("Chat file not found.")
        return False
    