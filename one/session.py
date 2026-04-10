# ========================================
#  会话管理 — 增删改查、列表展示
# ========================================

import json
import os
import streamlit as st
from datetime import datetime

MESSAGE_DIR = "message_list"


def get_timestamp():
    """生成会话 ID（时间戳格式）"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def format_display_time(file_id):
    """将文件名时间戳转为可读格式  20260409_143022 → 04-09 14:30"""
    try:
        dt = datetime.strptime(file_id, "%Y%m%d_%H%M%S")
        return dt.strftime("%m-%d %H:%M")
    except ValueError:
        return file_id


def _ensure_dir():
    if not os.path.exists(MESSAGE_DIR):
        os.makedirs(MESSAGE_DIR)


def _session_path(session_id):
    return os.path.join(MESSAGE_DIR, f"{session_id}.json")


# ------------------------------------------
#  CRUD
# ------------------------------------------

def init_message():
    """重置当前会话为全新空白会话"""
    st.session_state.messages = []
    st.session_state.current_session = get_timestamp()
    st.session_state.nick_name = ""
    st.session_state.character = ""
    st.session_state.session_title = ""


def _build_session_dict():
    return {
        "current_session": st.session_state.current_session,
        "nick_name": st.session_state.nick_name,
        "character": st.session_state.character,
        "session_title": st.session_state.get("session_title", ""),
        "messages": st.session_state.messages,
    }


def save_message():
    """保存当前会话到文件，然后重置为新会话"""
    _ensure_dir()
    if st.session_state.messages:
        with open(_session_path(st.session_state.current_session), "w", encoding="utf-8") as f:
            json.dump(_build_session_dict(), f, ensure_ascii=False, indent=4)
    init_message()


def _save_current_silently():
    """静默保存当前会话（不重置），用于切换会话前"""
    _ensure_dir()
    if st.session_state.messages:
        with open(_session_path(st.session_state.current_session), "w", encoding="utf-8") as f:
            json.dump(_build_session_dict(), f, ensure_ascii=False, indent=4)


def load_message(file):
    """保存当前会话后加载目标会话"""
    _save_current_silently()
    with open(_session_path(file), "r", encoding="utf-8") as f:
        data = json.load(f)
    st.session_state.current_session = data["current_session"]
    st.session_state.nick_name = data.get("nick_name", "")
    st.session_state.character = data.get("character", "")
    st.session_state.session_title = data.get("session_title", "")
    st.session_state.messages = data.get("messages", [])


def del_message(file):
    """删除会话文件，若删的是当前会话则重置"""
    path = _session_path(file)
    if os.path.exists(path):
        os.remove(path)
    if file == st.session_state.current_session:
        init_message()


# ------------------------------------------
#  列表
# ------------------------------------------

def _extract_title(data, file_id):
    """提取会话标题：优先自定义标题 → 首条用户消息 → 文件 ID"""
    custom = data.get("session_title", "")
    if custom:
        return custom[:8] + "…" if len(custom) > 8 else custom

    for msg in data.get("messages", []):
        if msg["role"] != "user":
            continue
        content = msg["content"]
        if isinstance(content, list):
            for item in content:
                if item.get("type") == "text":
                    t = item["text"]
                    return t[:8] + "…" if len(t) > 8 else t
        else:
            t = str(content)
            return t[:8] + "…" if len(t) > 8 else t
    return file_id


def get_session_list():
    """返回历史会话列表 [{id, title, count, time}]"""
    if not os.path.exists(MESSAGE_DIR):
        return []
    sessions = []
    fnames = sorted(
        [f for f in os.listdir(MESSAGE_DIR) if f.endswith(".json")],
        reverse=True,
    )
    for fname in fnames:
        file_id = fname[:-5]
        try:
            with open(os.path.join(MESSAGE_DIR, fname), "r", encoding="utf-8") as fp:
                data = json.load(fp)
            sessions.append({
                "id": file_id,
                "title": _extract_title(data, file_id),
                "count": len(data.get("messages", [])),
                "time": format_display_time(file_id),
            })
        except Exception:
            sessions.append({"id": file_id, "title": file_id, "count": 0, "time": ""})
    return sessions
