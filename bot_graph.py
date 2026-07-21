import sqlite3
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import SystemMessage
from config import llm
from tools import TOOLS

# Bind defined tools to the LLM instance
llm_with_tools = llm.bind_tools(TOOLS)

# System Prompt specifying contextual constraints
SYSTEM_PROMPT = SystemMessage(
    content="You are a helpful travel assistant. The current year is 2026. "
            "When searching for events, flights, or news, always search for 2026 information."
)

def assistant_node(state: MessagesState):
    messages = [SYSTEM_PROMPT] + state["messages"]
    result = llm_with_tools.invoke(messages)
    return {"messages": [result]}

# Build the LangGraph workflow
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant_node)
builder.add_node("tools", ToolNode(TOOLS))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

# Configure SQLite Checkpointer for State Persistence
conn = sqlite3.connect("travel_bot_memory.db", check_same_thread=False)
memory = SqliteSaver(conn)

# Compile graph with persistence memory saver
travel_agent = builder.compile(checkpointer=memory)