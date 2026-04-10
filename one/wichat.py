import os
import base64
import streamlit as st
from datetime import datetime

from config import (
    IMAGE_WIDTH, MODELS, DEFAULT_MODEL, DEFAULT_NICK_NAME,
    DEFAULT_CHARACTER, SYSTEM_PROMPT_TEMPLATE, USER_AVATAR, ASSISTANT_AVATAR,
)
from session import (
    get_timestamp, init_message, del_message, save_message,
    load_message, get_session_list,
)
from chat_client import stream_chat

# ============================================================
#  页面配置
# ============================================================
st.set_page_config(page_title="太阳之子", layout="centered", page_icon="☀️")

# 预加载备案图标（base64）
_ICON_PATH = os.path.join(os.path.dirname(__file__), "备案图标.png")
with open(_ICON_PATH, "rb") as _f:
    _ICON_B64 = base64.b64encode(_f.read()).decode("utf-8")

# ============================================================
#  CSS — 配合 config.toml 主题做微调（不再强改侧边栏底色/文字色）
# ============================================================
st.markdown("""
<style>
/* ===== 1. 顶部装饰条隐藏 ===== */
[data-testid="stDecoration"] {
    display: none !important;
}
header[data-testid="stHeader"] {
    background: transparent !important;
}

/* ===== 2. 布局微调 ===== */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 180px !important;
    max-width: 860px !important;
}

/* ===== 3. 标题渐变色 ===== */
h1 {
    background: linear-gradient(135deg, #667eea, #f5576c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800 !important;
}

/* ===== 4. 侧边栏按钮 ===== */
section[data-testid="stSidebar"] button {
    border-radius: 10px !important;
}
/* 侧边栏折叠按钮 — 深色可见 */
button[data-testid="stSidebarCollapseButton"],
button[data-testid="stSidebarNavCollapseButton"] {
    background: rgba(102,126,234,0.12) !important;
    border: 1px solid rgba(102,126,234,0.3) !important;
    border-radius: 8px !important;
}
button[data-testid="stSidebarCollapseButton"]:hover,
button[data-testid="stSidebarNavCollapseButton"]:hover {
    background: rgba(102,126,234,0.25) !important;
}
/* 普通按钮 — 白底描边 */
section[data-testid="stSidebar"] button[kind="secondary"] {
    background: #ffffff !important;
    border: 1.5px solid #c5cde0 !important;
}
section[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background: #eef1ff !important;
    border-color: #667eea !important;
}
/* 当前激活会话 — 主色填充 */
section[data-testid="stSidebar"] button[kind="primary"] {
    background: #667eea !important;
    color: #fff !important;
    border: none !important;
}
section[data-testid="stSidebar"] button[kind="primary"] p,
section[data-testid="stSidebar"] button[kind="primary"] span {
    color: #fff !important;
}

/* ===== 5. 聊天气泡 ===== */
[data-testid="stChatMessage"] {
    border-radius: 14px !important;
    margin: 5px 0 !important;
    padding: 6px 12px !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06) !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, #eef1ff, #f3eeff) !important;
    border-left: 3px solid #667eea !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: #ffffff !important;
    border-left: 3px solid #f5576c !important;
}

/* 时间戳 — 右对齐小字 */
[data-testid="stChatMessage"] [data-testid="stCaptionContainer"] {
    text-align: right !important;
}
[data-testid="stChatMessage"] [data-testid="stCaptionContainer"] p {
    font-size: 0.72rem !important;
    color: #999 !important;
    -webkit-text-fill-color: #999 !important;
}

/* ===== 6. 底部文件上传区 ===== */
[data-testid="stFileUploaderDropzone"] {
    border: 1.5px dashed rgba(102,126,234,0.35) !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #667eea !important;
}

/* ===== 7. 备案栏 ===== */
.beian-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 999;
    background: rgba(248, 249, 255, 0.95);
    backdrop-filter: blur(8px);
    border-top: 1px solid rgba(102, 126, 234, 0.15);
    padding: 5px 0 4px;
    text-align: center;
    font-size: 0.72rem;
    color: #888;
    line-height: 1.8;
}
.beian-footer a {
    color: #667eea;
    text-decoration: none;
    margin: 0 6px;
}
.beian-footer a:hover {
    text-decoration: underline;
}
.beian-footer img {
    vertical-align: middle;
    margin-right: 3px;
    width: 16px;
    height: 16px;
}
.beian-sep {
    color: #ccc;
    margin: 0 4px;
}

/* ===== 8. 聊天输入框 ===== */
[data-testid="stChatInput"] {
    border: 1.5px solid rgba(102,126,234,0.28) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #667eea !important;
    box-shadow: 0 4px 20px rgba(102,126,234,0.15) !important;
}
[data-testid="stChatInput"] textarea {
    border: none !important;
    box-shadow: none !important;
}
/* 发送按钮 */
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    border: none !important;
    border-radius: 10px !important;
    margin: 5px 6px 5px 0 !important;
}
[data-testid="stChatInput"] button svg {
    fill: #fff !important;
}
</style>
""", unsafe_allow_html=True)

st.title("太阳之子 AI 助手")
st.caption("哎呦，不错哦 ✨")

# ============================================================
#  Session State 初始化
# ============================================================
_defaults = {
    "nick_name": "",
    "character": "",
    "session_title": "",
    "current_session": get_timestamp(),
    "messages": [],
    "uploaded_file": None,
    "selected_model": DEFAULT_MODEL,
    "regenerate": False,
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ============================================================
#  辅助函数
# ============================================================
def _now_display():
    """当前时间，用于消息时间戳显示"""
    return datetime.now().strftime("%m-%d %H:%M")


def _trigger_regenerate():
    """弹出最后一条 AI 回复，标记重新生成"""
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
        st.session_state.messages.pop()
        st.session_state.regenerate = True


def _build_api_messages():
    """构建发给 API 的消息列表（system + 历史），剥离 timestamp 字段"""
    system_msg = {
        "role": "system",
        "content": SYSTEM_PROMPT_TEMPLATE.format(
            nick_name=st.session_state.nick_name or DEFAULT_NICK_NAME,
            character=st.session_state.character or DEFAULT_CHARACTER,
        ),
    }
    api_msgs = [system_msg]
    for msg in st.session_state.messages:
        api_msgs.append({"role": msg["role"], "content": msg["content"]})
    return api_msgs


# ============================================================
#  渲染历史消息
# ============================================================
for _i, _msg in enumerate(st.session_state.messages):
    _avatar = USER_AVATAR if _msg["role"] == "user" else ASSISTANT_AVATAR
    _ts = _msg.get("timestamp", "")

    with st.chat_message(_msg["role"], avatar=_avatar):
        if isinstance(_msg["content"], list):
            for _item in _msg["content"]:
                if _item.get("type") == "image_url":
                    _b64 = _item["image_url"]["url"].split(",", 1)[1]
                    st.image(base64.b64decode(_b64), width=IMAGE_WIDTH)
                elif _item.get("type") == "text":
                    st.write(_item["text"])
        else:
            st.write(_msg["content"])
        if _ts:
            st.caption(f"🕐 {_ts}")

# 重新生成按钮（仅当最后一条是 AI 回复时显示）
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    if st.button("🔄 重新生成", key="regen_btn", help="重新生成最后一条回答"):
        _trigger_regenerate()
        st.rerun()


# ============================================================
#  侧边栏
# ============================================================
with st.sidebar:
    # —— 新建会话
    _new_msg = st.button("✏️ 新建会话", use_container_width=True)

    st.divider()

    # —— 会话历史
    st.subheader("💬 会话历史")
    _sessions = get_session_list()
    for _s in _sessions:
        _c1, _c2 = st.columns([4, 1])
        with _c1:
            st.button(
                _s["title"],
                help=f"🕐 {_s['time']}  |  💬 {_s['count']} 条消息",
                key=f"load_{_s['id']}",
                use_container_width=True,
                type="primary" if _s["id"] == st.session_state.current_session else "secondary",
                on_click=lambda f=_s["id"]: load_message(f),
            )
        with _c2:
            st.button(
                "", key=f"del_{_s['id']}", icon="❌",
                use_container_width=True,
                on_click=lambda f=_s["id"]: del_message(f),
            )

    st.divider()

    # —— 会话设置
    st.subheader("⚙️ 会话设置")
    _title = st.text_input(
        "会话标题", placeholder="留空则自动生成",
        value=st.session_state.session_title,
    )
    st.session_state.session_title = _title

    _nick = st.text_input(
        "AI 昵称", placeholder="请输入 AI 昵称",
        value=st.session_state.nick_name,
    )
    st.session_state.nick_name = _nick

    _char = st.text_area(
        "AI 性格", placeholder="请输入 AI 性格",
        value=st.session_state.character,
    )
    st.session_state.character = _char

    if _new_msg:
        save_message()
        st.rerun()


# ============================================================
#  底部输入区
# ============================================================
with st._bottom:
    _uploaded = st.file_uploader(
        "", type=["jpg", "png", "jpeg"], key="image_uploader",
    )
    _prompt = st.chat_input(placeholder="请输入您想问的问题")


# ============================================================
#  消息处理 & API 调用
# ============================================================
_temp_content = []

# —— 图片暂存
if _uploaded and not st.session_state.uploaded_file:
    st.session_state.uploaded_file = _uploaded
if st.session_state.uploaded_file:
    _img_data = st.session_state.uploaded_file.getvalue()
    st.chat_message("user", avatar=USER_AVATAR).image(_img_data, width=IMAGE_WIDTH)
    if _img_data:
        _b64_img = base64.b64encode(_img_data).decode("utf-8")
        _temp_content = [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{_b64_img}"}},
        ]
    st.session_state.uploaded_file = None

# —— 判断是否需要调用 API
_should_call = False

if _prompt:
    st.chat_message("user", avatar=USER_AVATAR).write(_prompt)
    _user_msg = {
        "role": "user",
        "content": [*_temp_content, {"type": "text", "text": _prompt}] if _temp_content else _prompt,
        "timestamp": _now_display(),
    }
    st.session_state.messages.append(_user_msg)
    st.session_state.uploaded_file = None
    _should_call = True

elif st.session_state.regenerate:
    st.session_state.regenerate = False
    _should_call = True

# —— 调用 API（流式输出）
if _should_call:
    _api_msgs = _build_api_messages()
    try:
        _resp = stream_chat(st.session_state.selected_model, _api_msgs)
        _resp_text = ""
        _placeholder = st.empty()

        for _chunk in _resp:
            _delta = _chunk.choices[0].delta.content
            if _delta is not None:
                _resp_text += _delta
                # 带闪烁光标的流式输出
                _placeholder.chat_message("assistant", avatar=ASSISTANT_AVATAR).markdown(
                    _resp_text + " ▌"
                )

        # 最终渲染（去掉光标，加时间戳）
        _resp_ts = _now_display()
        with _placeholder.chat_message("assistant", avatar=ASSISTANT_AVATAR):
            st.write(_resp_text)
            st.caption(f"🕐 {_resp_ts}")

        st.session_state.messages.append({
            "role": "assistant",
            "content": _resp_text,
            "timestamp": _resp_ts,
        })

    except Exception as _e:
        st.error(f"API 调用失败：{str(_e)}")
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"抱歉，出现错误：{str(_e)}",
            "timestamp": _now_display(),
        })

# ============================================================
#  底部备案信息
# ============================================================
st.markdown(f"""
<div class="beian-footer">
    <a href="https://beian.miit.gov.cn/" rel="noreferrer" target="_blank">赣ICP备2026005927号</a>
    <span class="beian-sep">|</span>
    <a href="https://beian.mps.gov.cn/#/query/webSearch?code=36082602000254" rel="noreferrer" target="_blank">
        <img src="data:image/png;base64,{_ICON_B64}" alt="备案图标" />赣公网安备36082602000254号
    </a>
</div>
""", unsafe_allow_html=True)
