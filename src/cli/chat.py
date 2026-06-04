"""Chat with context-aware AI assistant using the Haiku model from Anthropic."""

from anthropic import Anthropic
from .config import (ANTHROPIC_API_KEY, MODEL_NAME, MAX_TOKENS, COST_PER_MILLION_INPUT, COST_PER_MILLION_OUTPUT)
from .storage import save_chat, load_chat, list_saved_chats, generate_chat_id
from .xml_export import save_chat_xml, list_xml_exports

class ChatSession:
    """
    Manage a stateful conversation with the LLM.

    Attributes:
        client:              Anthropic API client
        messages:            Full conversation history sent with every request
        system_prompt:       Invisible instruction that shapes the assistant's behaviour
        total_input_tokens:  Cumulative input tokens used across all turns
        total_output_tokens: Cumulative output tokens used across all turns
        chat_id:             Unique ID used when saving this session to disk
    """

    def __init__(self, system_prompt: str = "You are a helpful assistant."):
        """Initialise a new chat session with an empty message history."""
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.messages = []
        self.system_prompt = system_prompt
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.chat_id = generate_chat_id()  # Unique ID for this chat session

    def send(self, user_message: str)->str: 
        """
        Send a message to the assistant and get response. 
        All messages are stored in self.messages for context.
        Longer Conversations will use more tokens, so we track usage for cost estimation.
        """

        # Add user message to conversation
        self.messages.append({"role": "user", "content": user_message})

        # Send request to API with whole context
        response = self.client.messages.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
            system=self.system_prompt,
            messages= self.messages
        )

        # Add assistant response to conversation
        assistant_message = response.content[0].text
        
        #Add response to messages for context 
        self.messages.append({"role": "assistant", "content": assistant_message})

        # Update token usage
        self.total_input_tokens += response.usage.input_tokens
        self.total_output_tokens += response.usage.output_tokens

        return assistant_message
    
    def get_cost(self) -> dict:
        """
        Calculate estimated cost of the conversation based on token usage and model pricing.
        Returns a dictionary with total cost and breakdown.
        """
        input_cost = (self.total_input_tokens / 1_000_000) * COST_PER_MILLION_INPUT
        output_cost = (self.total_output_tokens / 1_000_000) * COST_PER_MILLION_OUTPUT
        total_cost = input_cost + output_cost

        return {
            "total_cost": round(total_cost, 6),
            "input_cost": round(input_cost, 6),
            "output_cost": round(output_cost, 6),
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens
        }
    
    def get_message_count(self) -> int:
        """
        Get the total number of messages in the conversation.
        Useful for understanding conversation length and context depth.
        """
        return len(self.messages)
    
    def save(self) -> str:
        """
        Save the current chat session to a JSON file using storage.py utilities.
        Returns the file path where the chat was saved.
        """
        from datetime import datetime
        cost = self.get_cost()
        chat_data = {
            "id": self.chat_id,
            "created_at": datetime.now().isoformat(),
            "system_prompt": self.system_prompt,
            "messages": self.messages,
            "stats": {
                "total_cost_usd": cost["total_cost"],
                "total_input_tokens": cost["total_input_tokens"],
                "total_output_tokens": cost["total_output_tokens"],
            }
        }
        return save_chat(chat_data)
    

def main():
    """
    Interactive CLI chat loop.
    Accepts user input and streams responses from Claude.
    Commands: quit, cost, context, new, save, list.
    """

    print("=" * 50)
    print("Personal AI Assistant - Chat Session")
    print("=" * 50)
    print("Commands: 'quit' to exit, 'cost' to see estimated costs, 'context' to see conversation history, 'new' to start a new conversation, 'save' to save as JSON, 'export' to save as XML, 'list' to see saved chats.")

    session = ChatSession(system_prompt="You are a helpful assistant that explains things in simple terms.")

    while True:
        #Read user input 
        try: 
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting chat. Goodbye!")
            break

        #Ignore empty input
        if not user_input:
            continue

        #Special commands
        if user_input.lower() == "quit":
            cost_info = session.get_cost()
            print(f"\nSitzungs-Statistik:")
            print(f"  - Total Messages: {session.get_message_count()}")
            print(f"  - Tokens: {cost_info['total_input_tokens']} in / {cost_info['total_output_tokens']} out")
            print(f"  - Estimated Cost: ${cost_info['total_cost']:.4f}")
            print("Goodbye!")
            break

        if user_input.lower() == "cost":
            cost_info = session.get_cost()
            print(f"\n📊 Bisherige Kosten:")
            print(f"   Input:  {cost_info['total_input_tokens']:>8} Tokens → ${cost_info['input_cost']:.6f}")
            print(f"   Output: {cost_info['total_output_tokens']:>8} Tokens → ${cost_info['output_cost']:.6f}")
            print(f"   Gesamt:                    → ${cost_info['total_cost']:.6f}")
            continue

        if user_input.lower() == "context":
            print(f"\n📚 Conversation History ({session.get_message_count()}):")
            for i, msg in enumerate(session.messages):
                role = "You" if msg["role"] == "user" else "Assistant"
                #Only show first 100 chars of each message for readability
                text = msg["content"][:100] 
                if len(msg["content"]) > 100: 
                    text += "..."
                print(f" [{i+1}] {role}: {text}")
            continue

        if user_input.lower() == "new":
            cost_info = session.get_cost()
            print(f"   (Alte Sitzung: ${cost_info['total_cost']:.4f})")
            session = ChatSession()
            print("🔄 Neues Gespräch gestartet.")
            continue

        if user_input.lower() == "save":
            file_path = session.save()
            print(f"Gespeichert: {file_path}")
            continue

        if user_input.lower() == "export":
            from datetime import datetime
            cost = session.get_cost()
            chat_data = {
                "id": session.chat_id,
                "created_at": datetime.now().isoformat(),
                "system_prompt": session.system_prompt,
                "messages": session.messages,
                "stats": {
                    "total_cost_usd": cost["total_cost"],
                    "total_input_tokens": cost["total_input_tokens"],
                    "total_output_tokens": cost["total_output_tokens"],
                }
            }
            file_path = save_chat_xml(chat_data)
            print(f"Exported as XML: {file_path}")
            continue

        if user_input.lower() == "list":
            chats = list_saved_chats()
            if not chats:
                print("Keine gespeicherten Chats gefunden.")
            else: 
                print("\n📂 Gespeicherte Chats:")
                for chat in chats:
                    print(f" - ID: {chat['id']} | Created At: {chat['created_at']} | Messages: {chat['message_count']} | Cost: ${chat['cost_usd']:.4f}")
            continue

        #Send message to assistant and print response
        print("Assistant is typing...", end="", flush=True)
        response = session.send(user_input)
        print("\rAssistant: " + response)

        #Print current cost after each response for transparency
        cost_info = session.get_cost()
        print(f"\n   [{cost_info['total_input_tokens']} in / {cost_info['total_output_tokens']} out"
            f" | ${cost_info['total_cost']:.4f} gesamt]") 
        
if __name__ == "__main__":
    main()
    
