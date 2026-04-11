# ========================================
#  API 客户端 — LangChain 版本
# ========================================

import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from config import MODELS

_llm_cache: dict[str, ChatOpenAI] = {}


def get_llm(model_key: str) -> ChatOpenAI:
    """按模型名获取/缓存 LangChain ChatOpenAI 实例"""
    if model_key not in _llm_cache:
        cfg = MODELS[model_key]
        _llm_cache[model_key] = ChatOpenAI(
            model=cfg["model"],
            api_key=os.environ.get(cfg["api_key_env"]),
            base_url=cfg["base_url"],
            streaming=True,
        )
    return _llm_cache[model_key]


def stream_chat(model_key: str, messages: list[BaseMessage]):
    """流式调用 LangChain LLM，返回 AIMessageChunk 迭代器"""
    llm = get_llm(model_key)
    return llm.stream(messages)
