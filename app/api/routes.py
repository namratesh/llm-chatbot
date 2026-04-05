from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from app.services.graph import graph
import json

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



@router.post("/chat/stream")
async def stream_chat(request: ChatRequest):
    async def event_generator():
        # 'stream_mode="messages"' tells LangGraph to stream LLM tokens
        # 'version="v2"' is the modern standard for 2026
        async for event in graph.astream(
            {"messages": [HumanMessage(content=request.message)]},
            stream_mode="messages",
        ):
            # Normalizing the event structure (handles both v1 and v2 formats)
            msg = event[0] if isinstance(event, tuple) else event
            if hasattr(msg, "content") and msg.content:
                yield msg.content

    return StreamingResponse(event_generator(), media_type="text/plain")