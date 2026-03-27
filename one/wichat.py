import json
import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import base64


def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def del_message(file):
    if os.path.exists(f"message_list/{file}.json"):
        os.remove(f"message_list/{file}.json")
    # 保存历史对话，重置新对话
    st.session_state.messages = []
    st.session_state.current_session = get_timestamp()
    st.session_state.nick_name = ""
    st.session_state.character = ""


def save_message():
    sessino_info = {
        "current_session": st.session_state.current_session,
        "nick_name": st.session_state.nick_name,
        "character": st.session_state.character,
        "messages": st.session_state.messages
    }
    if not os.path.exists("message_list"):
        os.mkdir("message_list")
    if st.session_state.messages:
        with open(f"message_list/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(sessino_info, f, ensure_ascii=False, indent=4)

    # 保存历史对话，重置新对话
    st.session_state.messages = []
    st.session_state.current_session = get_timestamp()
    st.session_state.nick_name = ""
    st.session_state.character = ""


def load_message(file):
    # 先保存当前会话
    save_current = {
        "current_session": st.session_state.current_session,
        "nick_name": st.session_state.nick_name,
        "character": st.session_state.character,
        "messages": st.session_state.messages
    }
    # 如果有消息，先保存
    if st.session_state.messages:
        with open(f"message_list/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(save_current, f, ensure_ascii=False, indent=4)
    # 加载目标会话
    with open(f"message_list/{file}.json", "r", encoding="utf-8") as f:
        message = json.load(f)
    st.session_state.current_session = message["current_session"]
    st.session_state.nick_name = message["nick_name"]
    st.session_state.character = message["character"]
    st.session_state.messages = message["messages"]

# 调用deepseek
# client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'), base_url="https://api.deepseek.com")

# 调用火山大模型
client = OpenAI(api_key=os.environ.get('ARK_API_KEY'), base_url="https://ark.cn-beijing.volces.com/api/v3")

# 页面布局
st.title("太阳之子AI助手")
st.write("哎呦，不错哦")
st.logo("☀️")
st.set_page_config(page_title="太阳之子", layout="centered", page_icon="☀️")

# 给session_state设置初始值，用于保存会话信息
if "nick_name" not in st.session_state:
    st.session_state.nick_name = ""
if "character" not in st.session_state:
    st.session_state.character = ""
if "current_session" not in st.session_state:
    st.session_state.current_session = get_timestamp()
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if isinstance(message["content"], list):
        st.chat_message(message["role"]).write(message["content"][1].get("text"))
    else:
        st.chat_message(message["role"]).write(message["content"])

# 性格初始化
natrue = """
    你的名字是：%s，你需要以一个朋友的视角和我对话，尽量简洁，涉及代码相关的问题可以详细说明，你的性格是：%s
"""
# 侧边栏布局
with st.sidebar:
    new_message = st.button("新建会话", icon="✏️", width="stretch")
    st.divider()
    st.text("会话历史")

    # 循环遍历文件夹，输出文件名
    file_path = []
    if os.path.exists("message_list"):
        for file in os.listdir("message_list"):
            if file.endswith(".json"):
                file_path.append(file[0:-5:1])
    for file in file_path:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.button(file, key=f"load_{file}", width="stretch",
                      type="primary" if file == st.session_state.current_session else "secondary",
                      on_click=lambda f=file: load_message(f))
        with col2:
            st.button("", key=f"del_{file}", icon="❌️", width="stretch", on_click=lambda f=file: del_message(f))

    st.divider()
    st.subheader("AI基础设置")
    nick_name = st.text_input("AI昵称", placeholder="请输入AI昵称", value=st.session_state.nick_name)
    st.session_state.nick_name = nick_name
    character = st.text_area("AI性格", placeholder="请输入AI性格", value=st.session_state.character)
    st.session_state.character = character

    # 音乐播放 Start-----------------------
    b64_audio = base64.b64encode(open("sources/晴天.mp3", "rb").read()).decode()

    if "is_playing" not in st.session_state:
        st.session_state.is_playing = False

    col1, col2 = st.columns([50, 1])
    with col1:
        if st.button("⏸️" if st.session_state.is_playing else "▶️", type="secondary", key="play_btn"):
            st.session_state.is_playing = not st.session_state.is_playing
            st.rerun()

    audio_container = st.empty()

    if st.session_state.is_playing:
        # 自动播放 + 完全隐藏控制条
        audio_html = f"""
                <audio id="music_player" 
                       autoplay="true" 
                       loop="false"
                       style="display: none;">
                    <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mpeg">
                </audio>
            """
        audio_container.markdown(audio_html, unsafe_allow_html=True)
    else:
        # 暂停时什么都不显示（或显示一个空的容器）
        audio_container.empty()
    # 音乐播放 End-----------------------

    if new_message:
        save_message()
        st.rerun()

# 底部固定区域
with st._bottom:
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], key="image_uploader")
    prompt = st.chat_input(placeholder="请输入您想问的问题")

# 构建消息
messages = [{"role": "system",
             "content": natrue % (st.session_state.nick_name if st.session_state.nick_name else "凡特吸",
                                  st.session_state.character if st.session_state.character else "ai助理")}]
temp_content = []
# 文件管理
if uploaded_file:
    # 处理图片
    image_data = uploaded_file.getvalue()

    # 如果有图片，添加到消息中
    temp_messgae = {}
    if image_data:
        # 上传图片
        base64_image = base64.b64encode(image_data).decode('utf-8')
        # 本地图片
        # base64_image = base64.b64encode(open(image_path, "rb").read()).decode()
        messages = messages + st.session_state.messages
        temp_content = [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
        ]

# 处理文本
if prompt:
    st.chat_message("user").write(f"{prompt}")

    if temp_content:
        temp_messgae = {
            "role": "user",
            "content": [
                *temp_content,
                {"type": "text", "text": prompt}
            ]
        }
    else:
        temp_messgae = {"role": "user", "content": prompt}

    messages.append(temp_messgae)
    st.session_state.messages.append(temp_messgae)

    response = client.chat.completions.create(
        model="doubao-seed-1-6-vision-250815",
        messages=messages,
        stream=True
    )

    # 流式输出解析格式
    response_message = ""
    response_empty = st.empty()
    for ms in response:
        if ms.choices[0].delta.content is not None:
            response_message += ms.choices[0].delta.content
            response_empty.chat_message("assistant").write(response_message)

    st.session_state.messages.append({"role": "assistant", "content": response_message})
