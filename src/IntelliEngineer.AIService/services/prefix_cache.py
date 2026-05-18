"""
前缀缓存引擎 - DeepSeek-Reasonix ImmutablePrefix模式移植
保持对话前缀不变以最大化DeepSeek缓存命中率(目标≥95%)
"""
from collections import OrderedDict
from typing import Optional


class PrefixCache:
    """
    实现ImmutablePrefix + AppendOnlyLog模式
    缓存键: (session_id, prompt_hash) → token数据
    """
    def __init__(self, max_entries: int = 1000):
        self._cache: OrderedDict[str, dict] = OrderedDict()
        self._max_entries = max_entries
        self._hit_count = 0
        self._miss_count = 0

    def lookup(self, session_id: str, prompt_hash: str) -> Optional[dict]:
        key = f"{session_id}:{prompt_hash}"
        if key in self._cache:
            self._hit_count += 1
            # LRU: 移到末尾
            self._cache.move_to_end(key)
            return self._cache[key]
        self._miss_count += 1
        return None

    def store(self, session_id: str, prompt_hash: str, data: dict):
        key = f"{session_id}:{prompt_hash}"
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = data

        # 淘汰最久未使用的条目
        while len(self._cache) > self._max_entries:
            self._cache.popitem(last=False)

    @property
    def hit_rate(self) -> float:
        total = self._hit_count + self._miss_count
        if total == 0:
            return 0.0
        return self._hit_count / total

    def clear(self):
        self._cache.clear()
        self._hit_count = 0
        self._miss_count = 0
