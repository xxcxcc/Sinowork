"""
记忆管理接口
"""
from fastapi import APIRouter
from services.memory_store import MemoryStore

router = APIRouter()
memory_store = MemoryStore()


@router.get("")
async def list_memories(level: str = "global"):
    return memory_store.list_by_level(level)


@router.post("")
async def add_memory(key: str, value: str, level: str = "global"):
    return memory_store.add(key, value, level)


@router.delete("/{memory_id}")
async def delete_memory(memory_id: str):
    return memory_store.delete(memory_id)
