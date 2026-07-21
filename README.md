# Stateful Travel Assistant AI Agent

A production-ready, context-aware Travel Assistant built using **LangGraph**, **LangChain**, and **Streamlit**. The system leverages the **ReAct (Reason + Act)** pattern to seamlessly integrate real-time web search, weather APIs, and localized attraction lookup while maintaining long-term session state and conversation persistence.

---

## Key Features

- **State Persistence & Memory:** Powered by LangGraph's `SqliteSaver` checkpointer, allowing cross-session state retention and multi-thread chat resumption via unique Session IDs.
- **Autonomous Tool Functionality (ReAct):**
  - **Live Search Integration:** Uses Tavily Search API to fetch up-to-date 2026 travel information, news, and events.
  - **Weather Telemetry:** Live metrics fetched via OpenWeatherMap API with automatic failover fallback.
  - **Attraction Recommendations:** Filtered local POI retrieval based on query categories.
- **Containerized Architecture:** Fully dockerized with multi-stage builds and isolated environment orchestrations using `docker-compose`.
- **Exportable Itineraries:** Download formatted conversation history directly from the user interface.

---

## System Architecture & Workflow

[ User Input ]
│
▼
[ Streamlit UI ] ────── (Session Config / Thread ID)
│
▼
[ LangGraph Workflow ]
┌───┴────────────────────────┐
│ Assistant Node (LLM) │ ◄─── System Prompt Engine
└───┬────────────────────────┘
│
├──► (Tool Call Required?)
│ │
│ ├── YES ──► [ Tool Node ] ──► (Tavily / Weather / POIs)
│ │ │
│ └───────────◄────┘
│
└── NO ──► [ SqliteSaver Checkpointer ] ──► [ Streamlit Response ]

---

## Tech Stack

- **Orchestration & Framework:** LangGraph, LangChain, Pydantic
- **LLM Engine:** Llama 3.3 70B Instruct (via OpenRouter API)
- **Web UI:** Streamlit
- **Tools & Data Feeds:** Tavily Search API, OpenWeatherMap API
- **State Persistence:** SQLite (`langgraph-checkpoint-sqlite`)
- **Containerization:** Docker, Docker Compose

---

## Project Structure

```text
├── app.py                  # Streamlit UI interface & session management
├── bot_graph.py            # LangGraph workflow definition & checkpointer setup
├── config.py               # LLM instance initialization & environment loading
├── tools.py                # External tool definitions (Search, Weather, Attractions)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker build specification
├── docker-compose.yml      # Multi-container orchestration config
├── .env.example            # Environment variables template
└── README.md               # Project documentation

```
