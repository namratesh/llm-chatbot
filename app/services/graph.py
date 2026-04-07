from langgraph.graph import StateGraph, START, END
from app.services.state import AgentState
from app.services.nodes import call_model

# 1. Define the Graph Structure
workflow = StateGraph(AgentState)

# 2. Add Nodes
workflow.add_node("chatbot", call_model)

# 3. Define Flow
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)

# Note: No compilation here.
# Compilation with AsyncSqliteSaver happens in app/main.py lifespan.