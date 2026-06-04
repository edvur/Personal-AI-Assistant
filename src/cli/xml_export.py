"""
XML Export Module: Save and load chat sessions as XML files.

File format:
<?xml version='1.0' encoding='utf-8'?>
<chat id="chat_20260604_143052">
  <created_at>2026-06-04T14:30:52</created_at>
  <system_prompt>...</system_prompt>
  <messages>
    <message role="user">...</message>
    <message role="assistant">...</message>
  </messages>
  <stats>
    <total_input_tokens>1234</total_input_tokens>
    <total_output_tokens>567</total_output_tokens>
    <total_cost_usd>0.003</total_cost_usd>
  </stats>
</chat>
"""

from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree, parse, indent

EXPORT_DIR = Path(__file__).parent.parent.parent / "data" / "xml_exports"


def ensure_export_dir():
    """Ensure the XML export directory exists."""
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def save_chat_xml(chat_data: dict) -> str:
    """
    Save a chat session to an XML file.

    Args:
        chat_data: Dictionary with keys id, created_at, system_prompt, messages, stats.

    Returns:
        The file path where the XML was saved.
    """
    ensure_export_dir()

    chat_id = chat_data.get("id", "chat_unknown")
    stats = chat_data.get("stats", {})

    root = Element("chat", id=chat_id)
    SubElement(root, "created_at").text = chat_data.get("created_at", "")
    SubElement(root, "system_prompt").text = chat_data.get("system_prompt", "")

    messages_el = SubElement(root, "messages")
    for msg in chat_data.get("messages", []):
        msg_el = SubElement(messages_el, "message", role=msg["role"])
        msg_el.text = msg["content"]

    stats_el = SubElement(root, "stats")
    SubElement(stats_el, "total_input_tokens").text = str(stats.get("total_input_tokens", 0))
    SubElement(stats_el, "total_output_tokens").text = str(stats.get("total_output_tokens", 0))
    SubElement(stats_el, "total_cost_usd").text = str(stats.get("total_cost_usd", 0.0))

    indent(root, space="  ")
    file_path = EXPORT_DIR / f"{chat_id}.xml"
    ElementTree(root).write(file_path, encoding="unicode", xml_declaration=True)

    return str(file_path)


def load_chat_xml(chat_id: str) -> dict:
    """
    Load a chat session from an XML file and return it as a dictionary.

    Args:
        chat_id: The ID of the chat to load (without .xml extension).

    Returns:
        A dictionary with the same structure as the JSON chat format.

    Raises:
        FileNotFoundError: If the specified XML file does not exist.
    """
    file_path = EXPORT_DIR / f"{chat_id}.xml"

    if not file_path.exists():
        raise FileNotFoundError(f"XML export '{chat_id}' not found in {EXPORT_DIR}.")

    root = parse(file_path).getroot()

    messages = [
        {"role": msg.get("role"), "content": msg.text or ""}
        for msg in root.findall("messages/message")
    ]

    stats_el = root.find("stats")
    stats = {
        "total_input_tokens": int(stats_el.findtext("total_input_tokens", "0")),
        "total_output_tokens": int(stats_el.findtext("total_output_tokens", "0")),
        "total_cost_usd": float(stats_el.findtext("total_cost_usd", "0.0")),
    }

    return {
        "id": root.get("id"),
        "created_at": root.findtext("created_at", ""),
        "system_prompt": root.findtext("system_prompt", ""),
        "messages": messages,
        "stats": stats,
    }


def list_xml_exports() -> list[dict]:
    """
    List all saved XML exports.

    Returns:
        A list of dicts with id, created_at, message_count, cost_usd,
        sorted by creation date descending.
    """
    ensure_export_dir()

    exports = []
    for file in EXPORT_DIR.glob("chat_*.xml"):
        try:
            root = parse(file).getroot()
            stats_el = root.find("stats")
            cost = float(stats_el.findtext("total_cost_usd", "0.0")) if stats_el is not None else 0.0
            exports.append({
                "id": root.get("id"),
                "created_at": root.findtext("created_at", ""),
                "message_count": len(root.findall("messages/message")),
                "cost_usd": cost,
            })
        except Exception as e:
            print(f"Error reading {file.name}: {e}")

    return sorted(exports, key=lambda x: x["created_at"], reverse=True)


def delete_xml_export(chat_id: str) -> bool:
    """
    Delete an XML export by chat ID.

    Args:
        chat_id: The ID of the export to delete (without .xml extension).

    Returns:
        True if deleted, False if not found.
    """
    file_path = EXPORT_DIR / f"{chat_id}.xml"

    if file_path.exists():
        file_path.unlink()
        return True

    print(f"XML export '{chat_id}' not found.")
    return False
