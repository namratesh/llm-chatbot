from app.services.llm import get_model
from app.services.state import AgentState

async def call_model(state: AgentState):
    model = get_model()
    response = await model.ainvoke(state["messages"])
    return {"messages": [response]}