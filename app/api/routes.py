from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
import json

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    thread_id: str | None = Field(None, description="Optional thread identifier")

@router.post("/chat")
async def chat_endpoint(chat_request: ChatRequest, request: Request):
    # Access the graph from app.state
    graph = request.app.state.graph
    
    # Initialize state with the user message
    initial_state = {"messages": [HumanMessage(content=chat_request.message)]}
    
    # Configure with thread_id. Default to "default" if not provided,
    # because the checkpointer requires a thread_id.
    thread_id = chat_request.thread_id or "default"
    config = {"configurable": {"thread_id": thread_id}}
    
    # Run the LangGraph
    result = await graph.ainvoke(initial_state, config=config)
    
    # Get the last message (the AI's response)
    final_message = result["messages"][-1].content
    return {"response": final_message}

@router.post("/chat/stream")
async def stream_chat(chat_request: ChatRequest, request: Request):
    # Access the graph from app.state
    graph = request.app.state.graph
    
    # Provide a default thread_id if missing to prevent checkpointer crash
    thread_id = chat_request.thread_id or "default"
    config = {"configurable": {"thread_id": thread_id}}

    async def event_generator():
        # Note: We only send the NEW message. 
        # LangGraph handles loading the old ones from the DB.
        async for chunk in graph.astream(
            {"messages": [HumanMessage(content=chat_request.message)]},
            config,
            stream_mode="messages",
            version="v2"
        ):
            # The v2 'messages' mode yields (BaseMessage, metadata)
            if chunk["type"] == "messages":
                msg, metadata = chunk["data"]
                if hasattr(msg, "content") and msg.content:
                    yield msg.content
    return StreamingResponse(event_generator(), media_type="text/plain")