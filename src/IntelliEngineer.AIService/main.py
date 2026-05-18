"""
智工助手 v0.1 - Python AI 服务入口
FastAPI REST API, 运行于 localhost:8000，由 WPF 桌面壳管理生命周期
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import chat, skill, memory, model

app = FastAPI(
    title="智工助手 AI 引擎",
    version="0.1.0",
    description="本地AI推理服务，集成Ollama本地模型与DeepSeek云端API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(chat.router, prefix="/api/chat", tags=["对话"])
app.include_router(skill.router, prefix="/api/skill", tags=["技能"])
app.include_router(memory.router, prefix="/api/memory", tags=["记忆"])
app.include_router(model.router, prefix="/api/model", tags=["模型"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}
