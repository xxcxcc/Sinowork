"""
智工助手 - 配置管理
"""
import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "data", "config.json")

DEFAULT_CONFIG = {
    "ollama": {"base_url": "http://localhost:11434", "default_model": "qwen2.5:14b"},
    "deepseek": {"api_key": "", "base_url": "https://api.deepseek.com/v1", "model": "deepseek-chat"},
    "reasoning_mode": "fast",  # fast / deep
    "prefix_cache_enabled": True,
    "max_tokens": 4096,
    "temperature": 0.7,
    "sandbox": {
        "allowed_paths": ["~/.intelliengineer/", "~/Documents/"],
        "denied_commands": ["rm -rf", "format", "shutdown"]
    },
    "roles": {
        "engineer": {"subtypes": ["software", "electrical", "mechanical", "implementation", "simulation"]},
        "clerk": {},
        "accountant": {},
        "project_manager": {}
    }
}


def load_config() -> dict:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()


def save_config(config: dict):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
