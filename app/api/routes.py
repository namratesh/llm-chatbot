from fastapi import APIRouter
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from app.services.graph import graph

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Initialize state with the user message
    initial_state = {"messages": [HumanMessage(content=request.message)]}
    
    # Run the LangGraph
    result = await graph.ainvoke(initial_state)
    
    # Get the last message (the AI's response)
    final_message = result["messages"][-1].content
    return {"response": final_message}