# Sprint 1 — Dein erster AI-Call (Woche 1–2)

> **Ziel:** Am Ende dieser 2 Wochen hast du ein CLI-Tool, das echte Gespräche
> mit einem LLM führt, den Verlauf speichert und dir zeigt, was jeder Call kostet.

---

## Tag 1: Umgebung aufsetzen (2h)

### 1.1 uv installieren

uv ist ein moderner Python-Paketmanager, der pip, venv und pyenv ersetzt —
in einem einzigen Tool, 10–100x schneller. Öffne dein Terminal
(in VS Code: `Ctrl+Ö` oder `Ctrl+Backtick`):

```bash
# uv installieren
# Windows (PowerShell):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Mac/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Prüfen ob es funktioniert:
uv --version
```

**Warum uv statt pip/venv?**
pip + venv + pyenv sind drei separate Tools, die man einzeln verwalten muss.
uv macht alles in einem: Python-Version verwalten, virtuelle Umgebung
automatisch erstellen, Packages blitzschnell installieren. Es ist der
neue Standard in der Python-Welt und spart dir von Anfang an Ärger.

### 1.2 Projekt mit uv initialisieren

```bash
# In dein geklontes Repo wechseln
cd Personal-AI-Assistant

# Projekt initialisieren — uv erstellt pyproject.toml und .venv automatisch
uv init --python 3.12

# Python wird automatisch heruntergeladen falls nötig!
# Du brauchst Python NICHT vorher manuell installieren.
```

**Was passiert bei `uv init`?**
uv erstellt eine `pyproject.toml` (die moderne Alternative zu `requirements.txt`),
lädt automatisch die richtige Python-Version herunter, und erstellt eine
virtuelle Umgebung im `.venv`-Ordner. Du musst die venv nie manuell
aktivieren — `uv run` erledigt das automatisch.

### 1.3 VS Code konfigurieren

Installiere diese VS Code Extensions (links in der Seitenleiste → Extensions):

- **Python** (Microsoft) — Syntax Highlighting, Debugging, Linting
- **Pylance** (Microsoft) — Autocomplete, Type Checking
- **GitLens** — Git-Verlauf direkt im Code sehen
- **Thunder Client** — API-Testing (brauchst du ab Sprint 2)

Dann in VS Code: `Ctrl+Shift+P` → "Python: Select Interpreter" → wähle
die venv (`./.venv/bin/python` oder `./.venv/Scripts/python.exe`).
uv legt die venv immer als `.venv` im Projektroot an.

### 1.4 Erste Dateien und Ordnerstruktur anlegen

```bash
# Ordnerstruktur erstellen
mkdir -p src/cli
mkdir -p journal
mkdir -p docs
mkdir -p tests

# Erste Dateien anlegen
touch src/__init__.py
touch src/cli/__init__.py
touch src/cli/main.py
touch src/cli/config.py
touch .env
touch .env.example
```

**Hinweis:** `pyproject.toml` und `uv.lock` hat `uv init` bereits erstellt.
Du brauchst keine `requirements.txt`.

### 1.5 .gitignore einrichten

Erstelle eine `.gitignore` Datei im Projektroot:

```gitignore
# Python
.venv/
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/

# Umgebungsvariablen (NIEMALS committen!)
.env

# IDE
.vscode/settings.json
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Daten
data/
*.db
```

**Warum ist .gitignore so wichtig?**
Ohne `.gitignore` könntest du versehentlich deinen API-Key (``.env``)
auf GitHub pushen. Das ist ein echtes Sicherheitsrisiko — Bots scannen
GitHub nach API-Keys und missbrauchen sie innerhalb von Minuten.

### 1.6 Erster Commit

```bash
git add .
git commit -m "chore: Projektstruktur und .gitignore aufsetzen"
git push origin main
```

**Commit-Nachrichten Konvention:**
- `feat:` — Neue Funktion
- `fix:` — Bugfix
- `docs:` — Dokumentation
- `chore:` — Setup, Konfiguration, Dependencies
- `refactor:` — Code umstrukturieren ohne neue Funktion

### 1.7 Learning Journal starten

Erstelle `journal/tag-01.md`:

```markdown
# Tag 1 — [Datum]

## Was ich getan habe
- Projektstruktur aufgesetzt
- venv erstellt
- VS Code konfiguriert

## Was ich gelernt habe
- Was eine virtuelle Umgebung ist und warum man sie braucht
- Wie .gitignore funktioniert

## Was schwierig war
- [Hier ehrlich sein]

## Morgen
- Anthropic API Key holen
- Ersten API-Call machen
```

---

## Tag 2: Erster API-Call (2h)

### 2.1 Anthropic API Key beschaffen

1. Gehe zu https://console.anthropic.com/
2. Erstelle einen Account (falls noch nicht vorhanden)
3. Gehe zu "API Keys" → "Create Key"
4. Kopiere den Key — er wird nur einmal angezeigt!

### 2.2 API Key sicher speichern

Trage deinen Key in `.env` ein:

```env
ANTHROPIC_API_KEY=sk-ant-api03-dein-key-hier
```

Und in `.env.example` (diese Datei wird committet, als Vorlage für andere):

```env
ANTHROPIC_API_KEY=sk-ant-api03-HIER-DEINEN-KEY-EINTRAGEN
```

### 2.3 Dependencies installieren

```bash
uv add anthropic python-dotenv
```

**Was passiert hier?**
`uv add` installiert die Packages UND trägt sie automatisch in `pyproject.toml` ein.
Du brauchst keine `requirements.txt` mehr — `pyproject.toml` ist der moderne Standard.
uv erstellt außerdem eine `uv.lock` Datei, die exakte Versionen festhält
(committen! So kann jeder dein Projekt mit identischen Versionen nutzen).

- `anthropic` — Die offizielle Python-Library von Anthropic für die Claude API
- `python-dotenv` — Liest `.env` Dateien und macht die Werte als
  Umgebungsvariablen verfügbar, damit du Keys nicht im Code stehen hast

### 2.4 Konfigurationsdatei erstellen

Erstelle `src/cli/config.py`:

```python
"""
Konfiguration für den AI Assistant.
Lädt API-Keys aus .env und definiert Standardwerte.
"""

import os
from dotenv import load_dotenv

# .env Datei laden — sucht automatisch im Projektverzeichnis
load_dotenv()

# API Key aus Umgebungsvariable lesen
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Prüfen ob der Key existiert
if not ANTHROPIC_API_KEY:
    raise ValueError(
        "ANTHROPIC_API_KEY nicht gefunden! "
        "Erstelle eine .env Datei mit deinem Key. "
        "Siehe .env.example als Vorlage."
    )

# Modell-Konfiguration
MODEL_NAME = "claude-haiku-4-5-20251001"  # Günstigstes Modell zum Lernen
MAX_TOKENS = 1024                          # Max. Antwortlänge

# Kosten pro Million Tokens (in USD) — für Kostenberechnung
COST_PER_MILLION_INPUT = 1.00    # Haiku Input: $1.00/MTok
COST_PER_MILLION_OUTPUT = 5.00   # Haiku Output: $5.00/MTok
```

**Warum Haiku statt Sonnet oder Opus?**
Haiku ist 3–5x günstiger und für Lernzwecke völlig ausreichend.
Du wechselst später auf Sonnet, wenn du die Qualitätsunterschiede
verstehen willst. Beim Entwickeln und Testen ist Haiku die richtige Wahl.

### 2.5 Ersten API-Call machen

Erstelle `src/cli/main.py`:

```python
"""
Personal AI Assistant — CLI Version
Sprint 1: Einfacher Chat mit Claude API
"""

from anthropic import Anthropic
from config import ANTHROPIC_API_KEY, MODEL_NAME, MAX_TOKENS


def erster_api_call():
    """
    Dein allererster API-Call an Claude.
    Schickt eine einfache Frage und gibt die Antwort aus.
    """
    # Client erstellen — verbindet sich mit der Anthropic API
    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    # Nachricht senden
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=MAX_TOKENS,
        messages=[
            {
                "role": "user",
                "content": "Was ist eine REST-API? Erkläre es mir in 3 Sätzen."
            }
        ]
    )

    # Antwort ausgeben
    print("=" * 50)
    print("ANTWORT VON CLAUDE:")
    print("=" * 50)
    print(response.content[0].text)
    print("=" * 50)

    # Metadaten anzeigen — DAS ist wichtig zum Verstehen!
    print(f"\nModell:          {response.model}")
    print(f"Input Tokens:    {response.usage.input_tokens}")
    print(f"Output Tokens:   {response.usage.output_tokens}")
    print(f"Stop Reason:     {response.stop_reason}")


if __name__ == "__main__":
    erster_api_call()
```

Ausführen:

```bash
cd src/cli
uv run python assistant
```

**Warum `uv run` statt direkt `python`?**
`uv run` aktiviert automatisch die richtige venv und stellt sicher,
dass alle Dependencies verfügbar sind. Du musst nie manuell
`source .venv/bin/activate` tippen.

**Was passiert hier genau?**

1. `Anthropic(api_key=...)` — Erstellt einen Client, der HTTPS-Requests
   an `api.anthropic.com` schickt. Der API-Key authentifiziert dich.

2. `client.messages.create(...)` — Sendet einen POST-Request an
   `/v1/messages` mit deiner Nachricht als JSON-Body.

3. `response.content[0].text` — Die API antwortet mit einem JSON-Objekt.
   `content` ist eine Liste von Blöcken (Text, Tool-Calls etc.).
   `content[0].text` ist der erste Textblock.

4. `response.usage` — Zeigt dir, wie viele Tokens verbraucht wurden.
   **Das ist dein Kostenzähler.** Jeder Token kostet Geld.

**Was sind Tokens?**
Tokens sind die Einheiten, in denen LLMs Text verarbeiten.
Ein Token ist ungefähr 4 Zeichen oder ¾ eines deutschen Wortes.
"Hallo, wie geht es dir?" ≈ 8 Tokens.
Das ist wichtig, weil du pro Token bezahlst.

### 2.6 Experimentiere! (restliche Zeit)

Ändere die Nachricht in `main.py` und beobachte:

- Wie sich die Token-Anzahl bei längeren Fragen verändert
- Wie sich `stop_reason` verhält (`end_turn` vs. `max_tokens`)
- Was passiert, wenn du `max_tokens` auf 50 setzt

```bash
git add .
git commit -m "feat: erster API-Call an Claude funktioniert"
git push
```

---

## Tag 3: System Prompts & Rollen (2h)

### 3.1 Was ist ein System Prompt?

Der System Prompt ist eine unsichtbare Anweisung, die dem LLM sagt,
WER es ist und WIE es sich verhalten soll. Der User sieht ihn nie,
aber er bestimmt den gesamten Charakter der Antworten.

### 3.2 System Prompts implementieren

Erweitere `main.py`:

```python
def chat_mit_system_prompt():
    """
    Zeigt den Effekt von System Prompts.
    Gleiche Frage, verschiedene Persönlichkeiten.
    """
    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    system_prompts = {
        "Experte": (
            "Du bist ein erfahrener Software-Architekt mit 20 Jahren Erfahrung. "
            "Du antwortest präzise und technisch korrekt. "
            "Du verwendest Fachbegriffe und erklärst sie kurz."
        ),
        "Anfänger-Freundlich": (
            "Du bist ein geduldiger Programmier-Lehrer. "
            "Du erklärst alles so, als wäre der Schüler 12 Jahre alt. "
            "Du verwendest Analogien aus dem Alltag. "
            "Du verwendest keine Fachbegriffe ohne sie zu erklären."
        ),
        "Pirat": (
            "Du bist ein Pirat, der Programmierer geworden ist. "
            "Du antwortest mit Piraten-Slang, aber technisch korrekt. "
            "Du nennst Bugs 'Ratten im Laderaum' und Deployments 'in See stechen'."
        ),
    }

    frage = "Was ist der Unterschied zwischen einer API und einer Datenbank?"

    for name, system_prompt in system_prompts.items():
        print(f"\n{'='*50}")
        print(f"PERSONA: {name}")
        print(f"{'='*50}")

        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
            system=system_prompt,        # <-- DAS ist neu
            messages=[
                {"role": "user", "content": frage}
            ]
        )

        print(response.content[0].text)
        print(f"\n[Tokens: {response.usage.input_tokens} in / "
              f"{response.usage.output_tokens} out]")


if __name__ == "__main__":
    chat_mit_system_prompt()
```

**Was du hier lernst:**
- Der gleiche Input erzeugt komplett andere Outputs je nach System Prompt
- Mehr System Prompt Text = mehr Input Tokens = höhere Kosten
- Der System Prompt ist dein wichtigstes Steuerungswerkzeug

### 3.3 Beobachte und dokumentiere

Erstelle `docs/prompt-patterns.md` und notiere:

```markdown
# Prompt Patterns — Meine Beobachtungen

## System Prompt Länge vs. Qualität
- Kurzer System Prompt (1 Satz): ...
- Mittlerer System Prompt (3-5 Sätze): ...
- Langer System Prompt (10+ Sätze): ...

## Was funktioniert gut?
- ...

## Was funktioniert nicht?
- ...
```

---

## Tag 4: Kontext & Gesprächsverlauf (2h)

### 4.1 Das Problem: LLMs haben kein Gedächtnis

Jeder API-Call ist stateless — das LLM weiß nichts von vorherigen
Nachrichten. Wenn du sagst "und was noch?", weiß es nicht, worauf
du dich beziehst. Die Lösung: Du schickst den gesamten bisherigen
Verlauf mit jedem Call mit.

### 4.2 Gesprächsverlauf implementieren

Erstelle `src/cli/chat.py`:

```python
"""
Chat-Modul mit Gesprächsverlauf.
Das LLM "erinnert" sich, weil wir den Verlauf mitschicken.
"""

from anthropic import Anthropic
from config import (
    ANTHROPIC_API_KEY, MODEL_NAME, MAX_TOKENS,
    COST_PER_MILLION_INPUT, COST_PER_MILLION_OUTPUT
)


class ChatSession:
    """
    Verwaltet ein Gespräch mit dem LLM.

    Attribute:
        client:          Anthropic API Client
        messages:        Liste aller Nachrichten im Gespräch
        system_prompt:   Unsichtbare Anweisung an das LLM
        total_input:     Summe aller Input Tokens
        total_output:    Summe aller Output Tokens
    """

    def __init__(self, system_prompt: str = "Du bist ein hilfreicher Assistent."):
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.messages = []                 # Hier sammeln sich die Nachrichten
        self.system_prompt = system_prompt
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def send(self, user_message: str) -> str:
        """
        Sendet eine Nachricht und gibt die Antwort zurück.

        WICHTIG: Wir schicken ALLE bisherigen Nachrichten mit.
        So "erinnert" sich das LLM an den Verlauf.
        Das bedeutet auch: Längere Gespräche = mehr Tokens = höhere Kosten.
        """
        # User-Nachricht zum Verlauf hinzufügen
        self.messages.append({
            "role": "user",
            "content": user_message
        })

        # API-Call mit dem GESAMTEN Verlauf
        response = self.client.messages.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
            system=self.system_prompt,
            messages=self.messages    # <-- Alle Nachrichten, nicht nur die letzte!
        )

        # Antwort extrahieren
        assistant_message = response.content[0].text

        # Antwort zum Verlauf hinzufügen
        self.messages.append({
            "role": "assistant",
            "content": assistant_message
        })

        # Token-Verbrauch tracken
        self.total_input_tokens += response.usage.input_tokens
        self.total_output_tokens += response.usage.output_tokens

        return assistant_message

    def get_cost(self) -> dict:
        """
        Berechnet die bisherigen Kosten des Gesprächs.
        Gibt ein Dictionary mit den Kosten in USD zurück.
        """
        input_cost = (self.total_input_tokens / 1_000_000) * COST_PER_MILLION_INPUT
        output_cost = (self.total_output_tokens / 1_000_000) * COST_PER_MILLION_OUTPUT
        return {
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
            "input_cost_usd": round(input_cost, 6),
            "output_cost_usd": round(output_cost, 6),
            "total_cost_usd": round(input_cost + output_cost, 6),
        }

    def get_message_count(self) -> int:
        """Anzahl der Nachrichten im Gespräch."""
        return len(self.messages)


def main():
    """
    Interaktive Chat-Schleife.
    Tippe 'quit' zum Beenden, 'kosten' für Kostenübersicht,
    'verlauf' um alle Nachrichten zu sehen.
    """
    print("=" * 50)
    print("Personal AI Assistant — CLI Chat")
    print("Befehle: 'quit', 'kosten', 'verlauf', 'neu'")
    print("=" * 50)

    session = ChatSession(
        system_prompt=(
            "Du bist ein hilfreicher AI-Assistent, der beim Programmieren lernen hilft. "
            "Du antwortest auf Deutsch. "
            "Du erklärst Konzepte klar und gibst konkrete Code-Beispiele. "
            "Wenn du Code zeigst, erkläre immer was jede Zeile tut."
        )
    )

    while True:
        # User-Input lesen
        try:
            user_input = input("\n🧑 Du: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nAuf Wiedersehen!")
            break

        # Leere Eingabe ignorieren
        if not user_input:
            continue

        # Sonderbefehle
        if user_input.lower() == "quit":
            kosten = session.get_cost()
            print(f"\n📊 Sitzungs-Statistik:")
            print(f"   Nachrichten: {session.get_message_count()}")
            print(f"   Tokens:     {kosten['input_tokens']} in / {kosten['output_tokens']} out")
            print(f"   Kosten:     ${kosten['total_cost_usd']:.4f}")
            print("\nAuf Wiedersehen!")
            break

        if user_input.lower() == "kosten":
            kosten = session.get_cost()
            print(f"\n📊 Bisherige Kosten:")
            print(f"   Input:  {kosten['input_tokens']:>8} Tokens → ${kosten['input_cost_usd']:.6f}")
            print(f"   Output: {kosten['output_tokens']:>8} Tokens → ${kosten['output_cost_usd']:.6f}")
            print(f"   Gesamt:                    → ${kosten['total_cost_usd']:.6f}")
            continue

        if user_input.lower() == "verlauf":
            print(f"\n📜 Gesprächsverlauf ({session.get_message_count()} Nachrichten):")
            for i, msg in enumerate(session.messages):
                rolle = "🧑 Du" if msg["role"] == "user" else "🤖 KI"
                # Nur die ersten 100 Zeichen jeder Nachricht anzeigen
                text = msg["content"][:100]
                if len(msg["content"]) > 100:
                    text += "..."
                print(f"   [{i+1}] {rolle}: {text}")
            continue

        if user_input.lower() == "neu":
            kosten = session.get_cost()
            print(f"   (Alte Sitzung: ${kosten['total_cost_usd']:.4f})")
            session = ChatSession()
            print("🔄 Neues Gespräch gestartet.")
            continue

        # Nachricht senden
        print("\n🤖 Claude: ", end="", flush=True)
        antwort = session.send(user_input)
        print(antwort)

        # Token-Info nach jeder Antwort anzeigen
        kosten = session.get_cost()
        print(f"\n   [{kosten['input_tokens']} in / {kosten['output_tokens']} out"
              f" | ${kosten['total_cost_usd']:.4f} gesamt]")


if __name__ == "__main__":
    main()
```

### 4.2.1 Fehlerbehebung beim Ausführen von chat.py

Beim Testen sind folgende Fehler aufgetaucht — und so löst du sie:

**Fehler 1: `ImportError: attempted relative import with no known parent package`**

```
uv run src/cli/chat.py
ImportError: attempted relative import with no known parent package
```

Ursache: `uv run datei.py` führt die Datei als eigenständiges Skript aus.
Relative Imports (`from .config import ...`) funktionieren nur innerhalb eines Packages.

Fix: Füge einen `[build-system]` und `[project.scripts]`-Eintrag in `pyproject.toml` hinzu:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/cli"]

[project.scripts]
assistant = "cli.main:first_api_call"
chat = "cli.chat:main"
```

Dann einmalig synchronisieren und danach mit dem Script-Namen starten:

```bash
uv sync
uv run chat
```

---

**Fehler 2: `ImportError: cannot import name 'COST_PER_MILLION_INPUT'`**

Ursache: `config.py` enthält die Kostenkonstanten nicht.

Fix: Füge am Ende von `src/cli/config.py` hinzu:

```python
COST_PER_MILLION_INPUT = 0.80   # Haiku 4.5 Input: $0.80/MTok
COST_PER_MILLION_OUTPUT = 4.00  # Haiku 4.5 Output: $4.00/MTok
```

---

**Fehler 3: `AttributeError: 'ChatSession' object has no attribute 'total_input_tokens'`**

Ursache: In `__init__` wurden die Attribute als `total_input` / `total_output` angelegt,
aber in `send()` und `get_cost()` als `total_input_tokens` / `total_output_tokens` verwendet.

Fix: In `__init__` umbenennen:

```python
self.total_input_tokens = 0   # nicht total_input
self.total_output_tokens = 0  # nicht total_output
```

---

**Fehler 4: `TypeError: cannot unpack non-sequence dict`**

Ursache: `for i, msg in session.messages:` — Dictionaries kann man nicht so entpacken.

Fix:

```python
for i, msg in enumerate(session.messages):
```

### 4.3 Teste und beobachte den Kontext

Führe das Programm aus und teste diese Sequenz:

```
Du: Was ist Python?
Du: Und worin unterscheidet es sich von JavaScript?
Du: Welches von beiden eignet sich besser für AI?
Du: Fasse unsere Diskussion in 3 Punkten zusammen.
Du: kosten
```

**Was du beobachten solltest:**
- Die Antwort auf "Und worin..." bezieht sich auf Python, obwohl
  du es nicht nochmal erwähnt hast → der Verlauf funktioniert
- Die Input-Tokens steigen mit jeder Nachricht, weil der gesamte
  Verlauf immer mitgeschickt wird
- "Fasse zusammen" funktioniert nur, weil das LLM die vorherigen
  Nachrichten sieht
- Tippe `kosten` um zu sehen, was das Gespräch gekostet hat

### 4.4 Kontext-Experiment dokumentieren

Erstelle `docs/kontext-experiment.md`:

```markdown
# Kontext-Experiment

## Beobachtung: Token-Wachstum pro Nachricht
| Nachricht Nr. | Input Tokens | Output Tokens | Warum? |
|---|---|---|---|
| 1 | ~30 | ~200 | Nur System Prompt + 1 Nachricht |
| 2 | ~260 | ~300 | System + Msg 1 + Antwort 1 + Msg 2 |
| 3 | ~590 | ~250 | Alles von oben + Msg 3 |
| ... | wächst! | variiert | Jede Nachricht macht den Kontext größer |

## Erkenntnis
Der Kontext wächst mit jedem Turn. Bei langen Gesprächen wird das
teuer und irgendwann erreicht man das Context Window Limit.
→ In Sprint 3 (RAG) lernen wir, wie man damit umgeht.
```

---

## Tag 5: Prompt-Techniken (2h)

### 5.1 Zero-Shot vs. Few-Shot

Erstelle `src/cli/prompt_experiments.py`:

```python
"""
Prompt Engineering Experimente.
Zeigt den Unterschied zwischen verschiedenen Prompting-Techniken.
"""

from anthropic import Anthropic
from .config import ANTHROPIC_API_KEY, MODEL_NAME, MAX_TOKENS


client = Anthropic(api_key=ANTHROPIC_API_KEY)


def vergleiche_prompts(techniken: dict, test_input: str):
    """
    Sendet den gleichen Test-Input mit verschiedenen Prompt-Techniken
    und zeigt die Ergebnisse nebeneinander.
    """
    for name, prompt in techniken.items():
        print(f"\n{'='*50}")
        print(f"TECHNIK: {name}")
        print(f"{'='*50}")

        # Das {input} im Prompt durch den Test-Input ersetzen
        final_prompt = prompt.replace("{input}", test_input)
        print(f"PROMPT:\n{final_prompt[:200]}...")

        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": final_prompt}]
        )

        print(f"\nANTWORT:\n{response.content[0].text}")
        print(f"\n[{response.usage.input_tokens} in / "
              f"{response.usage.output_tokens} out]")


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
    vergleiche_prompts(techniken, test)


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

    vergleiche_prompts(techniken, "Zeige deine Berechnung.")


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

    vergleiche_prompts(techniken, "Docker")


def main():
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
```

Füge in `pyproject.toml` unter `[project.scripts]` einen weiteren Eintrag hinzu:

```toml
[project.scripts]
assistant = "cli.main:first_api_call"
chat      = "cli.chat:main"
prompts   = "cli.prompt_experiments:main"
```

Dann einmalig synchronisieren und ausführen:

```bash
uv sync
uv run prompts
```

### 5.1.1 Fehlerbehebung

**Fehler: `ImportError: attempted relative import with no known parent package`**

Gleiche Ursache wie bei `chat.py` — direkt als Skript ausgeführt statt als Package.
Lösung: `pyproject.toml` um den `prompts`-Eintrag ergänzen (siehe oben) und mit `uv run prompts` starten.

### 5.2 Was du beobachten und dokumentieren sollst

Notiere in `docs/prompt-patterns.md`:

| Technik | Wann einsetzen? | Beispiel |
|---|---|---|
| Zero-Shot | Einfache Aufgaben, die das LLM "von sich aus" kann | Übersetzung, Zusammenfassung |
| Few-Shot | Wenn du ein bestimmtes Ausgabeformat oder Stil willst | Klassifizierung, Kategorisierung |
| Chain-of-Thought | Logik, Mathematik, mehrstufige Entscheidungen | Berechnungen, Analyse |
| Strukturierte Ausgabe | Wenn ein Programm die Antwort weiterverarbeiten soll | JSON-API-Responses |

---

## Tag 6–7: Chat-Verlauf speichern & laden (4h)

### 6.1 JSON-Speicherung implementieren

Erstelle `src/cli/storage.py`:

```python
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


# Ordner für gespeicherte Chats
CHAT_DIR = Path(__file__).parent.parent.parent / "data" / "chats"


def ensure_chat_dir():
    """Erstellt den Chat-Ordner, falls er nicht existiert."""
    CHAT_DIR.mkdir(parents=True, exist_ok=True)


def generate_chat_id() -> str:
    """
    Erzeugt eine eindeutige Chat-ID basierend auf dem Zeitstempel.
    Format: chat_YYYYMMDD_HHMMSS
    """
    return f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def save_chat(chat_id: str, system_prompt: str, messages: list,
              stats: dict) -> str:
    """
    Speichert ein Gespräch als JSON-Datei.

    Args:
        chat_id:       Eindeutige ID des Chats
        system_prompt:  Der verwendete System Prompt
        messages:       Liste der Nachrichten [{role, content}, ...]
        stats:          Token-Verbrauch und Kosten

    Returns:
        Pfad zur gespeicherten Datei
    """
    ensure_chat_dir()

    chat_data = {
        "id": chat_id,
        "created_at": datetime.now().isoformat(),
        "system_prompt": system_prompt,
        "messages": messages,
        "stats": stats,
    }

    filepath = CHAT_DIR / f"{chat_id}.json"

    # indent=2 macht die Datei lesbar (nicht alles in einer Zeile)
    # ensure_ascii=False damit deutsche Umlaute korrekt gespeichert werden
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(chat_data, f, indent=2, ensure_ascii=False)

    return str(filepath)


def load_chat(chat_id: str) -> dict:
    """
    Lädt ein Gespräch aus einer JSON-Datei.

    Args:
        chat_id: Die ID des zu ladenden Chats

    Returns:
        Dictionary mit den Chat-Daten

    Raises:
        FileNotFoundError: Wenn der Chat nicht existiert
    """
    filepath = CHAT_DIR / f"{chat_id}.json"

    if not filepath.exists():
        raise FileNotFoundError(f"Chat '{chat_id}' nicht gefunden in {CHAT_DIR}")

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def list_chats() -> list[dict]:
    """
    Listet alle gespeicherten Chats auf.

    Returns:
        Liste von Dictionaries mit {id, created_at, message_count, cost}
        Sortiert nach Erstellungsdatum (neueste zuerst).
    """
    ensure_chat_dir()
    chats = []

    for filepath in CHAT_DIR.glob("chat_*.json"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                chats.append({
                    "id": data["id"],
                    "created_at": data["created_at"],
                    "message_count": len(data["messages"]),
                    "cost_usd": data.get("stats", {}).get("total_cost_usd", 0),
                })
        except (json.JSONDecodeError, KeyError) as e:
            print(f"⚠️  Fehler beim Lesen von {filepath.name}: {e}")

    # Sortieren: neueste zuerst
    chats.sort(key=lambda x: x["created_at"], reverse=True)
    return chats


def delete_chat(chat_id: str) -> bool:
    """
    Löscht einen gespeicherten Chat.

    Returns:
        True wenn erfolgreich gelöscht, False wenn nicht gefunden.
    """
    filepath = CHAT_DIR / f"{chat_id}.json"
    if filepath.exists():
        filepath.unlink()
        return True
    return False
```

### 6.2 Storage in ChatSession einbauen

Ergänze in `chat.py` die Import- und Speicher-Funktionen:

```python
# Am Anfang von chat.py hinzufügen:
from storage import save_chat, load_chat, list_chats, generate_chat_id

# In der ChatSession-Klasse __init__:
self.chat_id = generate_chat_id()

# Neue Methode in ChatSession:
def save(self) -> str:
    """Speichert das aktuelle Gespräch als JSON."""
    filepath = save_chat(
        chat_id=self.chat_id,
        system_prompt=self.system_prompt,
        messages=self.messages,
        stats=self.get_cost()
    )
    return filepath

# In der main()-Funktion neue Befehle hinzufügen:
if user_input.lower() == "save":
    path = session.save()
    print(f"💾 Gespeichert: {path}")
    continue

if user_input.lower() == "liste":
    chats = list_chats()
    if not chats:
        print("📂 Keine gespeicherten Chats.")
    else:
        print(f"\n📂 Gespeicherte Chats ({len(chats)}):")
        for c in chats:
            print(f"   {c['id']} | {c['message_count']} Nachrichten"
                  f" | ${c['cost_usd']:.4f}")
    continue
```

### 6.3 JSON vs. XML verstehen

Erstelle `docs/json-vs-xml.md`:

```markdown
# JSON vs. XML — Vergleich

## Dein Chat als JSON (so speichern wir es)
```json
{
  "id": "chat_20260604_1430",
  "messages": [
    {"role": "user", "content": "Was ist Python?"},
    {"role": "assistant", "content": "Python ist..."}
  ]
}
```

## Gleicher Chat als XML
```xml
<?xml version="1.0" encoding="UTF-8"?>
<chat id="chat_20260604_1430">
  <messages>
    <message role="user">Was ist Python?</message>
    <message role="assistant">Python ist...</message>
  </messages>
</chat>
```

## Vergleich
| Kriterium | JSON | XML |
|---|---|---|
| Lesbarkeit | Gut | Gut, aber mehr Text |
| Dateigröße | Kleiner | Größer (wegen Tags) |
| Parsing in Python | json.load() | xml.etree oder lxml |
| Verwendung heute | APIs, Web, Config | Legacy, SOAP, Office-Formate |
| Datentypen | String, Number, Bool, null | Alles ist String |

## Fazit
JSON ist der Standard für APIs und moderne Anwendungen.
XML wird noch in Enterprise-Umgebungen und Dateiformaten (docx, svg) verwendet.
Für unser Projekt: JSON.
```

---

## Tag 8–9: Alles zusammenführen & Git (4h)

### 8.1 Code aufräumen und testen

```bash
# Alle Tests durchführen (manuell erstmal)
uv run assistant   # Erster API-Call
uv run chat        # Interaktiver Chat
uv run prompts     # Prompt-Techniken

# Prüfe ob alle Dateien sauber sind:
# - Keine API-Keys im Code?
# - Docstrings an jeder Funktion?
# - Kommentare wo nötig?
```

### 8.2 Git Branching üben

```bash
# Neuen Branch für ein Feature erstellen
git checkout -b feature/xml-export

# Hier XML-Export implementieren (Übungsaufgabe!)
# → Erstelle src/cli/xml_export.py
# → Exportiere einen Chat als XML

git add .
git commit -m "feat: XML Export für Chat-Verläufe"

# Zurück zu main wechseln und mergen
git checkout main
git merge feature/xml-export

# Branch löschen (aufgeräumt)
git branch -d feature/xml-export

git push origin main
```

### 8.3 Sprint-1-Übungsaufgaben (selbständig lösen!)

Bevor du zu Sprint 2 weitergehst, löse diese Aufgaben selbst.
Sie festigen alles, was du gelernt hast:

**Aufgabe A — Token-Kosten-Rechner (leicht)**
Erweitere `config.py` um eine Funktion `berechne_kosten(input_tokens, output_tokens, modell)`,
die die Kosten für verschiedene Modelle berechnet (Haiku, Sonnet, Opus).
Zeige beim Chat-Befehl `kosten` den Vergleich: "Dieses Gespräch hätte
mit Sonnet $X und mit Opus $Y gekostet."

**Aufgabe B — Chat-Suche (mittel)**
Erweitere `storage.py` um eine Funktion `search_chats(keyword)`,
die alle gespeicherten Chats nach einem Stichwort durchsucht
und die Treffer mit Kontext anzeigt.

**Aufgabe C — Prompt-Bibliothek (mittel)**
Erstelle `src/cli/prompts.py` mit einer Sammlung von System Prompts,
die der User im Chat-Tool auswählen kann. Speichere sie als
Dictionary oder in einer JSON-Datei.

**Aufgabe D — Export-Formate (fortgeschritten)**
Implementiere den Export eines Chats als:
1. Markdown-Datei (lesbar, schön formatiert)
2. XML-Datei (Übung für XML-Verständnis)
3. CSV-Datei (nur Metadaten: Timestamp, Role, Token-Count)

---

## Tag 10: Review & Sprint-Abschluss (2h)

### 10.1 Checkliste — Bin ich bereit für Sprint 2?

Gehe diese Liste durch. Wenn du 80%+ abhaken kannst, bist du bereit:

**Python-Grundlagen:**
- [ ] Ich kann Funktionen schreiben und aufrufen
- [ ] Ich verstehe Klassen (ChatSession) und was `self` bedeutet
- [ ] Ich kann mit Dictionaries und Listen arbeiten
- [ ] Ich kann Dateien lesen und schreiben (open, json.load/dump)
- [ ] Ich weiß was try/except macht
- [ ] Ich kann Packages installieren (pip) und importieren

**API & LLM:**
- [ ] Ich kann einen API-Call an Claude machen
- [ ] Ich verstehe was Tokens sind und warum sie Geld kosten
- [ ] Ich kann System Prompts schreiben und ihren Effekt beobachten
- [ ] Ich verstehe dass LLMs stateless sind und warum man den Verlauf mitschickt
- [ ] Ich kenne Zero-Shot, Few-Shot und Chain-of-Thought

**Git:**
- [ ] Ich kann committen, pushen, pullen
- [ ] Ich kann Branches erstellen und mergen
- [ ] Ich halte sensible Daten aus Git raus (.gitignore)

**Datenformate:**
- [ ] Ich kann JSON lesen, schreiben und parsen
- [ ] Ich kenne den Unterschied zwischen JSON und XML

### 10.2 Commit und weiter

```bash
git add .
git commit -m "feat: Sprint 1 abgeschlossen — CLI Chat mit Verlauf und Speicherung"
git push
```

---

## Was kommt in Sprint 2?

Du hast jetzt einen Chat, der lokal läuft. In Sprint 2 machst du daraus
einen Web-Service:

- **FastAPI** macht dein Tool über HTTP erreichbar
- **PostgreSQL** ersetzt die JSON-Dateien durch eine echte Datenbank
- **REST-Endpunkte** machen dein Tool für andere Programme nutzbar
- **SQL** lernst du an deinen eigenen Chat-Daten

→ Detaillierter Sprint-2-Plan folgt, wenn du Sprint 1 abgeschlossen hast.