from langgraph.graph import StateGraph, START, END
from app.services.state import AgentState
from app.services.nodes import call_model

# 1. Define the Graph
workflow = StateGraph(AgentState)

# 2. Add the Node
workflow.add_node("chatbot", call_model)

# 3. Define the Flow
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)

# 4. Compile the Graph
graph = workflow.compile()