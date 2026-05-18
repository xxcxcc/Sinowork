"""
对话接口 - 处理用户消息并调用AI引擎
"""
from fastapi import APIRouter
from pydantic import BaseModel
from services.agent import AgentEngine

router = APIRouter()
agent = AgentEngine()


class ChatRequest(BaseModel):
    session_id: str
    message: str
    role: str = "engineer"  # engineer / clerk / accountant / project_manager
    mode: str = "fast"      # fast / deep


class ChatResponse(BaseModel):
    session_id: str
    content: str
    token_count: int = 0
    cost_usd: float = 0.0


@router.post("", response_model=ChatResponse)
async def send_message(req: ChatRequest):
    response = await agent.chat(
        session_id=req.session_id,
        message=req.message,
        role=req.role,
        mode=req.mode
    )
    return response


@router.get("/sessions")
async def list_sessions():
    return agent.list_sessions()
