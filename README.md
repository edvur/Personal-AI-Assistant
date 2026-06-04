# 🎯 AI Engineer Lernplan — Personal AI Assistant Project

> **Ein Projekt. Viele Technologien. Echtes Können.**
> Dieses Dokument ist dein Kompass. Es lebt in deinem GitHub-Repo und wächst mit dir.

---

## Übersicht

| | |
|---|---|
| **Projekt** | Personal AI Assistant — vom CLI-Tool zum Cloud-deployed Agent-System |
| **Dauer** | ~20 Wochen bei 8–10h/Woche |
| **Ziel** | Agentic AI beherrschen, eigene Produkte bauen können, Rolle erweitern |
| **Setup** | VS Code + GitHub Repo + Python 3.11+ + Node.js 20+ |
| **Kosten** | ~10–20 €/Monat (API-Kosten, siehe Abschnitt unten) |

---

## Grundregeln

1. **60/40**: 60% eigener Code schreiben, 40% lernen (Docs, Videos, Tutorials)
2. **Jeden Tag 2h** statt ein langes Wochenende — Routine schlägt Motivation
3. **Build → Break → Fix**: Wenn etwas funktioniert, versuch es kaputtzumachen
4. **Learning Journal**: Jeden Tag 3 Sätze (Was gelernt? Was war schwer? Was morgen?)
5. **Claude Code erst ab Sprint 4** — vorher manuell coden, um zu verstehen was passiert

---

## Repo-Struktur

```
ai-assistant/
├── README.md              ← Dieses Dokument
├── journal/               ← Tägliche Lernnotizen
│   └── YYYY-MM-DD.md
├── src/
│   ├── cli/               ← Sprint 1: CLI-Tool
│   ├── api/               ← Sprint 2: FastAPI Backend
│   ├── rag/               ← Sprint 3: RAG Pipeline
│   ├── agents/            ← Sprint 4: Agent System
│   ├── frontend/          ← Sprint 5: React Dashboard
│   └── mcp/               ← Sprint 4: MCP Server
├── docs/
│   ├── architektur.md     ← Architektur-Entscheidungen
│   ├── security.md        ← Security-Notizen (OWASP etc.)
│   └── vergleiche.md      ← Tool-/Sprach-Vergleiche
├── tests/                 ← Tests für jeden Sprint
├── docker-compose.yml     ← Sprint 6: Container-Setup
├── .github/workflows/     ← Sprint 6: CI/CD Pipeline
└── .env.example           ← API-Keys Template (nie .env committen!)
```

---

## Sprint-Plan

### Sprint 1 — Dein erster AI-Call (Woche 1–2)

**Ziel:** In Woche 1 hast du ein Tool, das mit einem LLM spricht.

**Technologien:** `Python` · `APIs` · `HTTP` · `JSON` · `GIT` · `Tokens` · `Prompting` · `Kontext`

#### Aufgaben

- [ ] Python-Umgebung aufsetzen: `python -m venv venv`, pip, VS Code Extensions
- [ ] Git-Repo erstellen, `.gitignore` für Python, erster Commit
- [ ] Anthropic API Key holen, in `.env` speichern (→ `python-dotenv`)
- [ ] Ersten API-Call machen: Einfache Frage → Antwort ausgeben
- [ ] Token-Zähler einbauen: Input/Output Tokens pro Anfrage anzeigen
- [ ] System Prompts verstehen: Verschiedene Personas testen
- [ ] Prompt-Techniken üben: Zero-Shot, Few-Shot, Chain-of-Thought
- [ ] Kontext-Management: Gesprächsverlauf als Liste mitführen
- [ ] Chat-Verlauf als JSON speichern und laden
- [ ] Git: Feature-Branch erstellen, Änderungen committen, mergen

#### 🔐 Security in diesem Sprint
- [ ] API-Keys niemals in Code oder Git → `.env` + `.gitignore`
- [ ] Input-Validierung: Was passiert bei leerem Input? Zu langem Input?

#### Ergebnis
Ein CLI-Chat-Tool, das Gespräche mit einem LLM führt, den Verlauf speichert,
und Token-Verbrauch anzeigt.

#### Ressourcen
- [Anthropic API Docs](https://docs.anthropic.com)
- [Python dotenv](https://pypi.org/project/python-dotenv/)
- [Git Grundlagen](https://git-scm.com/book/de/v2)

---

### Sprint 2 — API & Datenbank (Woche 3–4)

**Ziel:** Dein CLI-Tool wird zum Web-Service mit persistenter Datenhaltung.

**Technologien:** `REST` · `HTTP` · `APIs` · `SQL` · `PostgreSQL` · `Python` · `Node.js`

#### Aufgaben

- [ ] FastAPI installieren und ersten Endpunkt bauen (`GET /health`)
- [ ] REST-Endpunkte designen:
  - [ ] `POST /chat` — Neue Nachricht senden
  - [ ] `GET /conversations` — Alle Gespräche abrufen
  - [ ] `GET /conversations/{id}` — Einzelnes Gespräch
  - [ ] `DELETE /conversations/{id}` — Gespräch löschen
- [ ] HTTP-Methoden und Statuscodes verstehen und korrekt einsetzen
- [ ] PostgreSQL lokal aufsetzen (oder Docker)
- [ ] Datenbankschema designen: `conversations`, `messages`, `metadata`
- [ ] SQL üben an echten Daten:
  - [ ] JOINs: Gespräche mit ihren Nachrichten laden
  - [ ] Aggregationen: Token-Verbrauch pro Tag/Woche
  - [ ] Window Functions: Laufende Summe der Kosten
- [ ] SQLAlchemy oder Prisma als ORM einbinden
- [ ] Swagger/OpenAPI Dokumentation ansehen (FastAPI generiert automatisch)
- [ ] Gleiche API-Endpunkte als Node.js/Express nachbauen (Vergleich)

#### 🔐 Security in diesem Sprint
- [ ] SQL Injection verstehen und verhindern (Parameterized Queries)
- [ ] Input-Validierung mit Pydantic (FastAPI)
- [ ] Rate Limiting einbauen
- [ ] CORS konfigurieren

#### Ergebnis
Eine REST-API, die LLM-Gespräche führt und in PostgreSQL speichert.
Abrufbar über HTTP mit sauberer Dokumentation.

#### Ressourcen
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [SQL Übungen](https://sqlbolt.com/)

---

### Sprint 3 — RAG: Dein Wissen anschließen (Woche 5–7)

**Ziel:** Die KI kennt DEINE Dokumente — nicht nur allgemeines Wissen.

**Technologien:** `RAG` · `VectorDb` · `Pinecone` · `LangChain` · `LlamaIndex` · `GenAI` · `LLMs`

#### Aufgaben

- [ ] Embeddings verstehen: Was sind Vektoren? Cosine Similarity?
- [ ] Dokumente vorbereiten: PDFs, Markdown, Textdateien sammeln
- [ ] Text Splitting: Verschiedene Chunk-Größen und Overlap testen
- [ ] Embeddings erzeugen (OpenAI `text-embedding-3-small` oder HuggingFace)
- [ ] ChromaDB lokal aufsetzen (kostenlos, gut zum Lernen)
- [ ] Pinecone Account erstellen, Vektoren hochladen und suchen
- [ ] LangChain RAG-Pipeline bauen:
  - [ ] Document Loader → Text Splitter → Embeddings → Vector Store
  - [ ] Retriever → Prompt Template → LLM → Antwort
- [ ] LlamaIndex: Gleiche Pipeline nachbauen
- [ ] Vergleich dokumentieren: LangChain vs. LlamaIndex (Stärken/Schwächen)
- [ ] Hybrid Search: Semantische Suche + Keyword-Suche kombinieren
- [ ] Retrieval-Qualität messen:
  - [ ] Sind die zurückgegebenen Chunks relevant?
  - [ ] Precision / Recall / MRR berechnen
- [ ] RAG in die bestehende API integrieren (neuer Endpunkt `POST /rag/query`)

#### 🔐 Security in diesem Sprint
- [ ] Prompt Injection bei RAG verstehen (manipulierte Dokumente)
- [ ] Zugriffskontrolle: Wer darf welche Dokumente abfragen?

#### Ergebnis
Ein RAG-System, das auf eigene Dokumente antwortet —
integriert in die bestehende API.

#### Ressourcen
- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [LlamaIndex Starter](https://docs.llamaindex.ai/en/stable/getting_started/)
- [Pinecone Quickstart](https://docs.pinecone.io/guides/get-started/quickstart)

---

### Sprint 4 — Agents: Die KI handelt (Woche 8–10)

**Ziel:** Vom Chatbot zum Agenten — die KI plant, entscheidet und nutzt Tools.

**Technologien:** `Agenten` · `LangGraph` · `Skills` · `Plugins` · `MCP` · `Evaluation`

> **Ab hier kannst du Claude Code einsetzen** — du verstehst jetzt genug,
> um den Output zu beurteilen. Nutze es als Pair-Programming-Partner, nicht als Autopilot.

#### Aufgaben

- [ ] Tool-Calling verstehen: Function Calling bei Anthropic/OpenAI API
- [ ] Einfachen Agent bauen: LLM entscheidet, welches Tool es nutzt
- [ ] Custom Tools als Python-Funktionen:
  - [ ] Web-Suche Tool
  - [ ] Rechner / Mathematik Tool
  - [ ] Datenbank-Abfrage Tool
  - [ ] Dateisystem-Tool (Dateien lesen/schreiben)
- [ ] LangGraph lernen:
  - [ ] State Machine Konzept verstehen
  - [ ] Nodes, Edges, Conditional Routing
  - [ ] Agent Loop: Observe → Think → Act → Observe
- [ ] MCP (Model Context Protocol) Server implementieren:
  - [ ] MCP-Spezifikation lesen und verstehen
  - [ ] Eigenen MCP-Server in Python bauen
  - [ ] Tools über MCP verfügbar machen
- [ ] Multi-Agent-System designen:
  - [ ] Planner Agent: Zerlegt Aufgaben in Schritte
  - [ ] Researcher Agent: Sammelt Informationen
  - [ ] Writer Agent: Erzeugt Output
  - [ ] Orchestrator: Koordiniert die Agents
- [ ] Evaluation Framework aufbauen:
  - [ ] Test-Cases definieren (Input → erwarteter Output)
  - [ ] Agent-Outputs automatisiert bewerten
  - [ ] Erfolgsrate messen und verbessern
- [ ] Guardrails einbauen:
  - [ ] Max. Iterationen pro Agent-Run
  - [ ] Fehlerbehandlung bei Tool-Failures
  - [ ] Human-in-the-Loop für kritische Entscheidungen

#### 🔐 Security in diesem Sprint
- [ ] OWASP Top 10 for LLM Applications durcharbeiten
- [ ] Prompt Injection Angriffe auf Agents testen
- [ ] Tool-Permissions: Agent darf nicht alles
- [ ] Sandbox für Code-Ausführung

#### Ergebnis
Ein Agent-System mit Tool-Calling, MCP-Server,
Multi-Agent-Workflows und Evaluation-Framework.

#### Ressourcen
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

---

### Sprint 5 — Frontend & Full-Stack (Woche 11–13)

**Ziel:** Dein Agent bekommt ein React-Dashboard.

**Technologien:** `React` · `JavaScript` · `Node.js` · `KPIs` · `REST`

#### Aufgaben

- [ ] React-Grundlagen: Create React App oder Vite, JSX, Components
- [ ] State Management: useState, useEffect, useContext
- [ ] Chat-Interface bauen:
  - [ ] Nachrichten-Liste mit Streaming-Antworten
  - [ ] Markdown-Rendering für LLM-Antworten
  - [ ] Code-Highlighting
- [ ] RAG-Bereich: Dokumente hochladen und verwalten
- [ ] Agent-Dashboard:
  - [ ] Laufende Agent-Tasks anzeigen
  - [ ] Tool-Calls visualisieren (welches Tool, Input, Output)
  - [ ] Agent-Logs in Echtzeit
- [ ] KPI-Panel:
  - [ ] Token-Verbrauch über Zeit
  - [ ] Kosten pro Gespräch
  - [ ] Response-Zeiten
  - [ ] Erfolgsrate der Agent-Tasks
- [ ] API-Anbindung: Fetch/Axios, Error Handling, Loading States
- [ ] Responsive Design: Mobile + Desktop

#### Ergebnis
Eine vollständige Web-App mit Chat, RAG-Upload,
Agent-Dashboard und KPI-Monitoring.

#### Ressourcen
- [React Docs](https://react.dev/learn)
- [Vite](https://vitejs.dev/guide/)

---

### Sprint 6 — Cloud & DevOps (Woche 14–16)

**Ziel:** Alles läuft live in der Cloud — automatisch deployed.

**Technologien:** `Docker` · `CI/CD` · `AWS` · `GCP` · `Azure` · `Cloud` · `FaaS` · `GIT`

#### Aufgaben

- [ ] Dockerfile schreiben für FastAPI-Backend
- [ ] Dockerfile für React-Frontend (Multi-Stage Build)
- [ ] Docker Compose: App + PostgreSQL + ChromaDB
- [ ] CI/CD Pipeline mit GitHub Actions:
  - [ ] Lint + Tests bei jedem Push
  - [ ] Docker Image bauen
  - [ ] Automatisch deployen bei Merge auf main
- [ ] Cloud-Deployment (mindestens einen Anbieter):
  - [ ] AWS: ECS/Fargate oder EC2 + Docker
  - [ ] GCP: Cloud Run (Container as a Service)
  - [ ] Azure: App Service oder Container Apps
- [ ] FaaS/Serverless ausprobieren:
  - [ ] Eine Funktion als AWS Lambda oder GCP Cloud Function
  - [ ] Wann Serverless vs. Container? Dokumentieren
- [ ] Cloud-Vergleich dokumentieren: Pricing, DX, Vor-/Nachteile
- [ ] Monitoring: Logging, Health Checks, Alerts einrichten
- [ ] Secrets Management: Keine Passwörter im Code

#### 🔐 Security in diesem Sprint
- [ ] Container-Security: Non-root User, minimale Base Images
- [ ] Network Security: VPC, Security Groups, Firewalls
- [ ] Secrets: AWS Secrets Manager / GCP Secret Manager
- [ ] HTTPS/TLS konfigurieren
- [ ] OWASP Top 10 (Web) durcharbeiten

#### Ergebnis
Deine App läuft in der Cloud mit automatischer CI/CD-Pipeline,
Monitoring und Security Best Practices.

#### Ressourcen
- [Docker Getting Started](https://docs.docker.com/get-started/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

---

### Sprint 7 — Erweiterung & Vertiefung (Woche 17–20)

**Ziel:** Breite aufbauen, Lücken schließen, Portfolio abrunden.

**Technologien:** `Make.com` · `Zapier` · `Airtable` · `MongoDB` · `NoSQL` · `RabbitMQ` ·
`Messaging Systems` · `Spark` · `Databricks` · `Snowflake` · `PowerBI` · `Tableau` ·
`ETL` · `ELT` · `C#` · `.NET` · `Java` · `Netzwerke` · `Architekturen`

> Dieser Sprint ist modular — wähle die Module, die für dein Ziel am wichtigsten sind.

#### Modul A: Automation & No-Code
- [ ] Make.com: Mehrstufigen Workflow bauen (z.B. Webhook → Agent → E-Mail)
- [ ] Zapier: Gleichen Workflow nachbauen → Vergleich dokumentieren
- [ ] Airtable: Als No-Code-Datenbank für Agent-Outputs
- [ ] Eigene API als Webhook-Trigger einbinden

#### Modul B: Daten & Analytics
- [ ] MongoDB: Unstrukturierte Agent-Logs speichern → NoSQL vs. SQL Vergleich
- [ ] ETL vs. ELT Konzepte an einem realen Beispiel durchspielen
- [ ] Spark/Databricks: Große Datenmengen verarbeiten (PySpark Basics)
- [ ] Snowflake: Data Warehouse Grundlagen
- [ ] Power BI oder Tableau: Dashboard an deine Daten anbinden

#### Modul C: Messaging & Architektur
- [ ] RabbitMQ in Docker: Queues, Exchanges, Producer/Consumer
- [ ] Async Task-Queue für lang laufende Agent-Jobs
- [ ] Architektur-Patterns dokumentieren: Monolith, Microservices, Event-Driven
- [ ] Netzwerk-Grundlagen: TCP/IP, DNS, Load Balancing

#### Modul D: Andere Sprachen
- [ ] C#/.NET: Einen Microservice aus Sprint 2 nachbauen
- [ ] Java/Spring Boot: Gleicher Service → Dreifach-Vergleich (Python/C#/Java)
- [ ] Unterschiede dokumentieren: Ökosystem, Typsystem, Performance, DX

---

## Cybersecurity Lernpfad

> Security ist kein separates Thema — es ist in jedem Sprint eingebaut.
> Zusätzlich diese Ressourcen parallel durcharbeiten:

### Grundlagen (parallel zu Sprint 1–2)
- [ ] OWASP Top 10 Web Application Security lesen
- [ ] CIA Triad verstehen: Confidentiality, Integrity, Availability
- [ ] Authentifizierung vs. Autorisierung verstehen
- [ ] HTTPS/TLS: Wie funktioniert Verschlüsselung?

### AI Security (parallel zu Sprint 3–4)
- [ ] OWASP Top 10 for LLM Applications durcharbeiten
- [ ] Prompt Injection: Arten, Beispiele, Schutzmaßnahmen
- [ ] Data Poisoning bei RAG-Systemen verstehen
- [ ] Responsible AI: Bias, Fairness, Transparenz

### Infrastruktur Security (parallel zu Sprint 5–6)
- [ ] Container Security Best Practices
- [ ] Cloud Security Fundamentals (AWS/GCP/Azure)
- [ ] Secrets Management und Key Rotation
- [ ] Dependency Scanning (Dependabot, Snyk)

### Weiterführend (nach Sprint 7)
- [ ] Penetration Testing Grundlagen (eigene Systeme!)
- [ ] Security Headers (CSP, HSTS, etc.)
- [ ] Zero Trust Architecture Konzepte
- [ ] Bug Bounty Programme anschauen (HackerOne)

---

## Kostenübersicht

| Posten | Kosten/Monat | Hinweis |
|---|---|---|
| Anthropic API (Haiku) | ~10–15 € | Entwicklung & Tests |
| Anthropic API (Sonnet) | ~5–10 € | Nur für finale Outputs |
| Pinecone | 0 € | Free Tier reicht zum Lernen |
| AWS/GCP/Azure | 0–10 € | Free Tiers nutzen! |
| PostgreSQL | 0 € | Lokal oder Docker |
| Docker | 0 € | Docker Desktop kostenlos |
| GitHub | 0 € | Free Tier reicht |
| **Gesamt** | **~15–35 €** | |

### Kosten-Spartipps
- Haiku ($1/$5 pro MTok) zum Entwickeln, Sonnet ($3/$15) nur für Produktion
- Prompt Caching aktivieren → 90% Ersparnis auf wiederholte Inputs
- Batch API nutzen für Evaluations → 50% günstiger
- Cloud Free Tiers ausreizen (AWS 12 Monate, GCP $300 Guthaben)
- ChromaDB statt Pinecone zum Lernen (lokal, kostenlos)

---

## Fortschritts-Tracker

| Sprint | Status | Start | Ende | Notizen |
|---|---|---|---|---|
| 1 — Erster AI-Call | ⬜ Offen | | | |
| 2 — API & Datenbank | ⬜ Offen | | | |
| 3 — RAG | ⬜ Offen | | | |
| 4 — Agents | ⬜ Offen | | | |
| 5 — Frontend | ⬜ Offen | | | |
| 6 — Cloud & DevOps | ⬜ Offen | | | |
| 7 — Erweiterung | ⬜ Offen | | | |

Statuswerte: ⬜ Offen · 🟡 In Arbeit · ✅ Abgeschlossen

---

## Werkzeuge & Setup

### Ab Tag 1
- **VS Code** mit Extensions: Python, Pylance, GitLens, Thunder Client
- **Git + GitHub** für Versionskontrolle
- **Python 3.11+** mit venv
- **Terminal** (bash/zsh/PowerShell)

### Ab Sprint 2
- **PostgreSQL** (lokal oder Docker)
- **Postman** oder **Thunder Client** (API-Testing)

### Ab Sprint 4
- **Claude Code** als Pair-Programming-Partner
- **Docker Desktop**

### Ab Sprint 5
- **Node.js 20+** für React-Frontend

---

## Entscheidungslog

> Dokumentiere hier wichtige Entscheidungen und WARUM du sie getroffen hast.

| Datum | Entscheidung | Warum | Alternativen betrachtet |
|---|---|---|---|
| | | | |

---

## Vergleichs-Notizen

> Wenn du zwei Technologien vergleichst, halte die Ergebnisse hier fest.

### LangChain vs. LlamaIndex
_(Sprint 3 — nach dem Vergleich ausfüllen)_

### SQL vs. NoSQL
_(Sprint 2 + Sprint 7 — nach dem Vergleich ausfüllen)_

### AWS vs. GCP vs. Azure
_(Sprint 6 — nach dem Vergleich ausfüllen)_

### Python vs. C# vs. Java
_(Sprint 7 — nach dem Vergleich ausfüllen)_

---

*Letzte Aktualisierung: Juni 2026*
*Erstellt als lebendes Dokument — wächst mit jedem Sprint.*
