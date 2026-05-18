"""
Agent引擎 - 核心推理服务
整合Ollama(本地)与DeepSeek(云端)，实现角色感知的对话生成
采用 DeepSeek-Reasonix 的 ImmutablePrefix + 成本颜色标记模式
"""
import hashlib
import time
from typing import Optional
from dataclasses import dataclass, field
from config import load_config
from services.prefix_cache import PrefixCache
from services.sandbox import PathGuard


@dataclass
class Session:
    id: str
    role: str
    messages: list = field(default_factory=list)
    created_at: float = field(default_factory=time.time)


class AgentEngine:
    def __init__(self):
        self.config = load_config()
        self.sessions: dict[str, Session] = {}
        self.prefix_cache = PrefixCache()
        self.path_guard = PathGuard(self.config.get("sandbox", {}))
        self._total_tokens = 0
        self._total_cost = 0.0

    async def chat(self, session_id: str, message: str, role: str, mode: str = "fast") -> dict:
        # 获取或创建会话
        session = self.sessions.get(session_id)
        if not session:
            session = Session(id=session_id, role=role)
            self.sessions[session_id] = session

        # 构建系统提示词（角色感知）
        system_prompt = self._build_system_prompt(role)
        full_prompt = f"{system_prompt}\n\n用户：{message}\n\n助手："

        # 前缀缓存检查（DeepSeek-Reasonix模式）
        prompt_hash = hashlib.md5(full_prompt.encode()).hexdigest()
        cached = self.prefix_cache.lookup(session_id, prompt_hash)

        if cached and self.config.get("prefix_cache_enabled", True):
            # 缓存命中 — 绿色成本标记(< $0.05)
            token_count = cached.get("token_count", len(message) // 2)
            cost = token_count * 0.000001  # 缓存命中极低成本
        else:
            # 调用AI模型生成回复
            content, token_count = await self._call_model(
                prompt=full_prompt, mode=mode
            )
            cost = self._estimate_cost(token_count, mode)
            # 存入前缀缓存
            self.prefix_cache.store(session_id, prompt_hash, {
                "token_count": token_count,
                "content": content
            })

        # 成本颜色标记：绿(<0.05) 黄(0.05-0.20) 红(>=0.20)
        cost_color = "green" if cost < 0.05 else ("yellow" if cost < 0.20 else "red")

        # 累计统计
        self._total_tokens += token_count
        self._total_cost += cost

        return {
            "session_id": session_id,
            "content": cached.get("content", "") if cached else content,
            "token_count": token_count,
            "cost_usd": round(cost, 6),
            "cached": bool(cached),
            "cost_color": cost_color,
        }

    async def _call_model(self, prompt: str, mode: str = "fast") -> tuple[str, int]:
        """调用AI模型（支持Ollama本地和DeepSeek云端）"""
        config = self.config
        model_type = config.get("active_model", "ollama")

        if model_type == "ollama":
            return await self._call_ollama(prompt, mode)
        else:
            return await self._call_deepseek(prompt, mode)

    async def _call_ollama(self, prompt: str, mode: str) -> tuple[str, int]:
        """调用Ollama本地模型"""
        try:
            import ollama
            ollama_config = self.config.get("ollama", {})
            model = ollama_config.get("default_model", "qwen2.5:14b")

            options = {"temperature": 0.7 if mode == "fast" else 0.3}
            response = ollama.generate(model=model, prompt=prompt, options=options)

            content = response.get("response", "")
            token_count = response.get("eval_count", len(content) // 2)
            return (content, token_count)
        except Exception as e:
            return (f"[本地模型调用失败: {e}]", 0)

    async def _call_deepseek(self, prompt: str, mode: str) -> tuple[str, int]:
        """调用DeepSeek云端API"""
        try:
            from openai import OpenAI
            ds_config = self.config.get("deepseek", {})
            client = OpenAI(
                api_key=ds_config.get("api_key", ""),
                base_url=ds_config.get("base_url", "https://api.deepseek.com/v1")
            )
            model = ds_config.get("model", "deepseek-chat")
            # flash默认 → auto升级 → pro按需
            actual_model = model if mode == "deep" else "deepseek-chat"

            response = client.chat.completions.create(
                model=actual_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config.get("max_tokens", 4096),
                temperature=self.config.get("temperature", 0.7)
            )
            content = response.choices[0].message.content or ""
            token_count = response.usage.total_tokens if response.usage else len(content) // 2
            return (content, token_count)
        except Exception as e:
            return (f"[云端模型调用失败: {e}]", 0)

    def _build_system_prompt(self, role: str) -> str:
        """构建角色感知的系统提示词"""
        prompts = {
            "engineer": "你是一位资深工程师，精通PLC编程(C#/Python)、工业标准(GB/GJB/IEC)、电气机械设计。请用专业、严谨的中文回答。",
            "clerk": "你是一位高效的办公室文员，擅长文档排版、会议纪要撰写、邮件处理、Excel数据分析。请用规范、礼貌的中文回答。",
            "accountant": "你是一位专业的财务会计，精通税务政策、财务报表编制、发票处理、成本核算。请用准确、合规的中文回答。",
            "project_manager": "你是一位经验丰富的项目经理，擅长进度管控、资源协调、风险管理、验收报告撰写。请用清晰、果断的中文回答。",
        }
        return prompts.get(role, "你是智工助手AI助理，用专业、准确的中文回答。")

    def _estimate_cost(self, token_count: int, mode: str) -> float:
        """估算Token成本"""
        if mode == "deep":
            return token_count * 0.000002  # DeepSeek深度模式约$2/M tokens
        return token_count * 0.0000005     # 缓存命中/本地模型极低成本

    def list_sessions(self) -> list:
        return [{"id": s.id, "role": s.role, "count": len(s.messages)} for s in self.sessions.values()]
