import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from app.api.routes import router
from app.services.graph import workflow
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Ensure the data directory exists (relevant for non-mapped local dev)
    os.makedirs("/app/data", exist_ok=True)
    
    # 2. Initialize AsyncSqliteSaver from a persistent path
    async with AsyncSqliteSaver.from_conn_string("/app/data/chatbot.db") as checkpointer:
        # 3. Setup database tables
        await checkpointer.setup()
        
        # 4. Compile the graph with the checkpointer and store it in app.state
        app.state.graph = workflow.compile(checkpointer=checkpointer)
        
        yield

app = FastAPI(title="Staff AI Research Agent", lifespan=lifespan)

# Include routes
app.include_router(router, prefix="/v1")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)