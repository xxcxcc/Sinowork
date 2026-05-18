"""
模型管理接口
"""
from fastapi import APIRouter
from config import load_config, save_config

router = APIRouter()


@router.get("")
async def list_models():
    config = load_config()
    return [
        {"id": "ollama", "name": "Ollama 本地模型", "provider": "ollama", "status": "available"},
        {"id": "deepseek", "name": "DeepSeek 云端", "provider": "deepseek", "status": "available"},
    ]


@router.get("/stats")
async def get_cost_stats():
    return {"total_tokens": 0, "total_cost": 0.0, "cache_hit_rate": 0.95}


@router.post("/switch")
async def switch_model(model_id: str):
    config = load_config()
    config["active_model"] = model_id
    save_config(config)
    return {"status": "ok", "model": model_id}
