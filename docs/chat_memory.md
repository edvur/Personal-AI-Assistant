# 🧠 Chat-Memory: Lernplan-Entwicklung

> Zusammenfassung des Gesprächsverlaufs, in dem der gesamte Lernplan entstanden ist.
> Dient als Referenz für zukünftige Gespräche mit Claude.

---

## Ausgangslage

**Wer:** Lernender mit Python/JS-Grundlagen, wenig praktischer Erfahrung
**Verfügbare Zeit:** 8–10 Stunden pro Woche
**Ziele:**
- Rolle in Richtung AI/Data erweitern
- Eigene Produkte und Prototypen bauen können
- Agentic AI intensiv lernen (Kernziel)
- Tech-Stack weiterentwickeln und up-to-date bleiben
- Cybersecurity-Grundlagen aufbauen

**GitHub Repo:** https://github.com/edvur/Personal-AI-Assistant.git
**Tooling:** VS Code + uv (statt pip/venv) + GitHub

---

## Technologie-Liste (Ausgangspunkt)

Der Lernplan deckt folgende Begriffe ab:

LLMs, RAG, APIs, SQL, REST, AWS, CI/CD, C#, .NET, MCP, GIT, NoSQL, ELT, ETL,
GCP, KPIs, HTTP, automatisierte Workflows, Agenten, Skills, Plugins, Cloud,
VectorDb, GenAI, LangChain, Azure, Python, Java, JavaScript, Tokens, Spark,
Evaluation, JSON/XML, Prompting, React, Kontext, Make.com, Airtable, Zapier,
LlamaIndex, Node.js, PostgreSQL, MongoDB, Messaging Systems, Netzwerke,
Architekturen, RabbitMQ, Docker, Databricks, PowerBI, Tableau, Pinecone,
FaaS, Snowflake, LangGraph

---

## Getroffene Entscheidungen

### 1. Ein Projekt statt vieler
**Entscheidung:** Alle Technologien werden in einem einzigen wachsenden Projekt gelernt
(Personal AI Assistant), nicht in 13 separaten Projekten.

**Begründung:** Technologien im Kontext eines echten Projekts zu lernen verankert
das Wissen besser. Jede Woche wird das Projekt mächtiger, und neue Technologien
werden genau dann eingeführt, wenn sie gebraucht werden.

### 2. Sprint-Struktur (7 Sprints, ~20 Wochen)
| Sprint | Fokus | Technologien |
|---|---|---|
| 1 (Wo 1–2) | Erster AI-Call, CLI-Tool | Python, APIs, Tokens, Prompting, JSON, Git |
| 2 (Wo 3–4) | REST-API & Datenbank | FastAPI, REST, HTTP, SQL, PostgreSQL |
| 3 (Wo 5–7) | RAG Knowledge Base | RAG, VectorDB, Pinecone, LangChain, LlamaIndex |
| 4 (Wo 8–10) | Agents & MCP | LangGraph, Agents, MCP, Skills, Plugins, Evaluation |
| 5 (Wo 11–13) | Frontend & Full-Stack | React, JavaScript, Node.js, KPIs |
| 6 (Wo 14–16) | Cloud & DevOps | Docker, CI/CD, AWS, GCP, Azure, FaaS |
| 7 (Wo 17–20) | Erweiterung & Vertiefung | Make.com, Zapier, MongoDB, RabbitMQ, Spark, etc. |

### 3. uv statt pip/venv
**Entscheidung:** uv als Python-Paketmanager verwenden.

**Begründung:** Schneller (10–100x), ersetzt pip + venv + pyenv in einem Tool,
wird zunehmend zum Standard. Einfacherer Einstieg.

### 4. Claude Code erst ab Sprint 4
**Entscheidung:** In Sprint 1–3 manuell coden, ab Sprint 4 Claude Code als
Pair-Programming-Partner einsetzen.

**Begründung:** Man muss verstehen, was Code tut, bevor man ihn generieren lässt.
Ab Sprint 4 ist genug Grundverständnis da, um Claude-Code-Output zu beurteilen.

### 5. Cybersecurity integriert, nicht separiert
**Entscheidung:** Security wird in jedem Sprint mitgelernt, nicht als eigene Phase.

**Details pro Sprint:**
- Sprint 1–2: API-Key-Management, Input-Validierung, SQL Injection
- Sprint 3–4: OWASP Top 10 for LLM, Prompt Injection, Data Poisoning
- Sprint 5–6: Container Security, Cloud Security, Secrets Management, OWASP Top 10 Web
- Parallel: CIA Triad, Authentifizierung vs. Autorisierung, Zero Trust Konzepte

### 6. Sprint-Guides einzeln und detailliert
**Entscheidung:** Jeder Sprint wird als eigenes, extrem detailliertes Dokument
erstellt — mit exakten Befehlen, Code-Beispielen und Erklärungen.
Nächster Sprint wird erst erstellt, wenn der vorherige abgeschlossen ist.

**Begründung:** Tempo und Schwerpunkte verändern sich. Besser anpassen als
200 Seiten im Voraus produzieren, die veralten.

---

## Kosten-Einschätzung

| Posten | Kosten/Monat |
|---|---|
| Anthropic API (Haiku zum Entwickeln) | ~10–15 € |
| Anthropic API (Sonnet für Produktion) | ~5–10 € |
| Cloud/Pinecone/Tools | 0 € (Free Tiers) |
| **Gesamt** | **~15–25 €** |

**Spartipps:** Prompt Caching (90% Ersparnis), Batch API (50% Rabatt),
Haiku zum Entwickeln / Sonnet nur für finalen Output.

---

## Erstellte Dateien

| Datei | Zweck |
|---|---|
| `AI-Engineer-Lernplan.md` | Hauptdokument: Übersicht, alle Sprints, Tracker, Referenzen |
| `sprint-01-detail.md` | Sprint 1 im Detail: Tag-für-Tag-Anleitung mit Code |
| `chat-memory.md` | Diese Datei: Zusammenfassung aller Entscheidungen |

---

## Offene Punkte / Nächste Schritte

- [ ] Sprint 1 beginnen (Tag 1: uv installieren, Repo-Struktur aufsetzen)
- [ ] Nach Abschluss Sprint 1: Sprint 2 detailliert erstellen lassen
- [ ] Detaillierte Sprints 2–7 werden jeweils on-demand erstellt
- [ ] Interaktiver Lernplan (React-Artifact) als optionale Referenz vorhanden

---

## Lernprinzipien (vereinbart)

1. **60/40-Regel:** 60% eigener Code, 40% lernen
2. **2h täglich** statt 10h am Wochenende
3. **Build → Break → Fix:** Wenn es funktioniert, versuch es kaputtzumachen
4. **Learning Journal:** Jeden Tag 3 Sätze (gelernt / schwierig / morgen)
5. **Nie Technologie isoliert lernen** — immer im Kontext des Projekts

---

*Erstellt: Juni 2026*
*Letzter Chat: Lernplan-Entwicklung und Sprint-1-Detail*