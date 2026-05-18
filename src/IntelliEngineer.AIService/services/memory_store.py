"""
记忆存储 - 四级记忆系统
global / project / role / enterprise
"""
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MemoryEntry:
    id: str
    key: str
    value: str
    level: str  # global / project / role / enterprise
    created_at: str = ""
    tags: list = field(default_factory=list)


class MemoryStore:
    def __init__(self):
        self._memories: dict[str, MemoryEntry] = {}

    def list_by_level(self, level: str = "global") -> list:
        return [
            {"id": m.id, "key": m.key, "value": m.value, "level": m.level}
            for m in self._memories.values() if m.level == level
        ]

    def add(self, key: str, value: str, level: str = "global") -> dict:
        mem = MemoryEntry(
            id=str(uuid.uuid4())[:8],
            key=key,
            value=value,
            level=level
        )
        self._memories[mem.id] = mem
        return {"id": mem.id, "key": mem.key}

    def delete(self, memory_id: str) -> dict:
        if memory_id in self._memories:
            del self._memories[memory_id]
            return {"status": "deleted"}
        return {"error": "未找到"}
