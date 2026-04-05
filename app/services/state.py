from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # 'add_messages' ensures new messages are appended, not overwritten
    messages: Annotated[list, add_messages]