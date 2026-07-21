import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from bot_graph import travel_agent

st.set_page_config(page_title="Stateful Travel Bot", page_icon="✈️", layout="wide")

# Sidebar configurations
st.sidebar.title("⚙️ Travel Bot Settings")
thread_id = st.sidebar.text_input("Session / Thread ID", value="user_session_1")
config = {"configurable": {"thread_id": thread_id}}

if st.sidebar.button("Clear Screen Chat"):
    st.session_state.messages = []
    st.rerun()

st.title("✈️ Stateful Travel Assistant with Memory")
st.caption("Plan your trip, check weather, and ask for recommendations!")

# Initialize session state for UI display
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat history
for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    if getattr(msg, "content", None):
        st.chat_message(role).write(msg.content)

# Process user input
if user_input := st.chat_input("Ask me about travel, weather, or itineraries..."):
    st.chat_message("user").write(user_input)
    
    user_message = HumanMessage(content=user_input)
    result = travel_agent.invoke({"messages": [user_message]}, config)
    
    bot_response = result["messages"][-1].content
    
    st.session_state.messages.append(user_message)
    st.session_state.messages.append(AIMessage(content=bot_response))
    
    st.chat_message("assistant").write(bot_response)

# Download itinerary summary functionality
if st.session_state.messages:
    chat_export = "\n\n".join([f"{m.type.upper()}: {m.content}" for m in st.session_state.messages if m.content])
    st.sidebar.download_button("📥 Download Itinerary Summary", chat_export, file_name="my_travel_plan.txt")