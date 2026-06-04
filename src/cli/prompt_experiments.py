"""
Prompt Engineering Experiments with Claude API.
Demonstrates how different system prompts affect the assistant's responses.
"""

from anthropic import Anthropic
from .config import ANTHROPIC_API_KEY, MODEL_NAME, MAX_TOKENS

client = Anthropic(api_key=ANTHROPIC_API_KEY)

def compare_prompts(techniken: dict, test_input: str): 
    """
    Compare different system prompts by sending the same user input.
    Prints the responses for each prompt.
    
    Args:
        techniken: A dictionary of prompt names and their corresponding system prompts.
        test_input: The user message to send for testing.
    """
    for name, prompt in techniken.items():
        print(f"\n{'=' * 50}")
        print(f"Technik: {name}")
        print(f"{'=' * 50}")

        final_prompt = prompt.replace("{input}", test_input)
        print(f"Prompt:\n{final_prompt[:200]}...")
        
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
            system=prompt,
            messages=[{"role": "user", "content": final_prompt}]
        )
        print(f"Prompt:\n{response.content[0].text}")
        print(f"\n{response.usage.input_tokens} in / {response.usage.output_tokens} out")


# ----- Experiment 1: Klassifizierung -----

def experiment_klassifizierung():
    """
    Zeigt wie Few-Shot die Qualität einer Klassifizierung verbessert.
    """
    techniken = {
        "Zero-Shot (keine Beispiele)": (
            "Klassifiziere diese Kundenanfrage in eine Kategorie "
            "(Beschwerde, Frage, Lob, Feature-Wunsch):\n\n"
            "{input}"
        ),
        "Few-Shot (mit Beispielen)": (
            "Klassifiziere Kundenanfragen. Hier sind Beispiele:\n\n"
            "Anfrage: 'Das Produkt ist nach 2 Tagen kaputtgegangen!'\n"
            "Kategorie: Beschwerde\n\n"
            "Anfrage: 'Wie kann ich mein Passwort zurücksetzen?'\n"
            "Kategorie: Frage\n\n"
            "Anfrage: 'Euer Support-Team war unglaublich hilfreich, danke!'\n"
            "Kategorie: Lob\n\n"
            "Anfrage: 'Es wäre toll, wenn man PDFs exportieren könnte.'\n"
            "Kategorie: Feature-Wunsch\n\n"
            "Klassifiziere jetzt diese Anfrage:\n"
            "Anfrage: '{input}'\n"
            "Kategorie:"
        ),
    }

    test = "Die App stürzt immer ab wenn ich ein Foto hochlade. Ich will mein Geld zurück!"
    compare_prompts(techniken, test)


# ----- Experiment 2: Chain-of-Thought -----

def experiment_chain_of_thought():
    """
    Chain-of-Thought: Das LLM "denkt laut" und kommt zu besseren Ergebnissen.
    Besonders wichtig bei Logik- und Rechenaufgaben.
    """
    techniken = {
        "Direkt (ohne Denkprozess)": (
            "Ein Unternehmen hat 120 Mitarbeiter. 40% arbeiten remote. "
            "Von den Remote-Mitarbeitern nutzen 75% ein VPN. "
            "Wie viele Mitarbeiter nutzen ein VPN?\n\n{input}"
        ),
        "Chain-of-Thought (mit Denkprozess)": (
            "Ein Unternehmen hat 120 Mitarbeiter. 40% arbeiten remote. "
            "Von den Remote-Mitarbeitern nutzen 75% ein VPN. "
            "Wie viele Mitarbeiter nutzen ein VPN?\n\n"
            "Denke Schritt für Schritt:\n{input}"
        ),
    }

    compare_prompts(techniken, "Zeige deine Berechnung.")


# ----- Experiment 3: Strukturierte Ausgabe -----

def experiment_strukturierte_ausgabe():
    """
    Zeigt wie man das LLM dazu bringt, in einem bestimmten Format
    zu antworten (JSON, Tabelle, etc.). Kritisch für Automatisierung.
    """
    techniken = {
        "Unstrukturiert": (
            "Analysiere diese Technologie und gib Vor- und Nachteile:\n\n{input}"
        ),
        "JSON-Format erzwingen": (
            "Analysiere diese Technologie. Antworte AUSSCHLIESSLICH "
            "in diesem JSON-Format, kein anderer Text:\n\n"
            '{{"technologie": "...", '
            '"kategorie": "...", '
            '"vorteile": ["..."], '
            '"nachteile": ["..."], '
            '"empfehlung": "..."}}\n\n'
            "Technologie: {input}"
        ),
    }

    compare_prompts(techniken, "Docker")


def main():
    """Run all three prompt engineering experiments in sequence."""
    print("\n" + "=" * 60)
    print("EXPERIMENT 1: Zero-Shot vs. Few-Shot Klassifizierung")
    print("=" * 60)
    experiment_klassifizierung()

    print("\n\n" + "=" * 60)
    print("EXPERIMENT 2: Chain-of-Thought Reasoning")
    print("=" * 60)
    experiment_chain_of_thought()

    print("\n\n" + "=" * 60)
    print("EXPERIMENT 3: Strukturierte Ausgabe (JSON)")
    print("=" * 60)
    experiment_strukturierte_ausgabe()


if __name__ == "__main__":
    main()

