# ========================================
#  API 客户端 — 封装模型调用
# ========================================

import os
from openai import OpenAI
from config import MODELS

_clients: dict[str, OpenAI] = {}


def get_client(model_key: str) -> OpenAI:
    """按模型名获取/缓存 OpenAI 客户端"""
    if model_key not in _clients:
        cfg = MODELS[model_key]
        _clients[model_key] = OpenAI(
            api_key=os.environ.get(cfg["api_key_env"]),
            base_url=cfg["base_url"],
        )
    return _clients[model_key]


def stream_chat(model_key: str, messages: list):
    """流式调用模型"""
    cfg = MODELS[model_key]
    client = get_client(model_key)
    return client.chat.completions.create(
        model=cfg["model"],
        messages=messages,
        stream=True,
    )
