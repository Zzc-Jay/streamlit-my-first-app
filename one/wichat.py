import json
import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import base64

IMAGE_WIDTH = 300

def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def init_message():
    st.session_state.messages = []
    st.session_state.current_session = get_timestamp()
    st.session_state.nick_name = ""
    st.session_state.character = ""


def del_message(file):
    if os.path.exists(f"message_list/{file}.json"):
        os.remove(f"message_list/{file}.json")
    # 保存历史对话，重置新对话
    init_message()


def save_message():
    session_info = {
        "current_session": st.session_state.current_session,
        "nick_name": st.session_state.nick_name,
        "character": st.session_state.character,
        "messages": st.session_state.messages
    }
    if not os.path.exists("message_list"):
        os.mkdir("message_list")
    if st.session_state.messages:
        with open(f"message_list/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_info, f, ensure_ascii=False, indent=4)

    # 保存历史对话，重置新对话
    init_message()


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


# @st.cache_data
# def get_message_files():
#     """缓存消息文件列表"""
#     if not os.path.exists("message_list"):
#         return []
#     files = [f[:-5] for f in os.listdir("message_list") if f.endswith(".json")]
#     return sorted(files, reverse=True)

# @st.cache_resource
# def get_audio_base64(file_path):
#     """缓存音频文件的 base64 编码"""
#     try:
#         with open(file_path, "rb") as f:
#             return base64.b64encode(f.read()).decode()
#     except FileNotFoundError:
#         st.error(f"音频文件不存在：{file_path}")
#         return None

# 调用deepseek
# client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'), base_url="https://api.deepseek.com")

# 调用火山大模型
MODEL_NAME = "doubao-seed-1-6-vision-250815"
client = OpenAI(api_key=os.environ.get('ARK_API_KEY'), base_url="https://ark.cn-beijing.volces.com/api/v3")

# 页面布局
st.set_page_config(page_title="太阳之子", layout="centered", page_icon="☀️")

st.title("太阳之子AI助手")
st.write("哎呦，不错哦")
st.logo("☀️")

# 给session_state设置初始值，用于保存会话信息
if "nick_name" not in st.session_state:
    st.session_state.nick_name = ""
if "character" not in st.session_state:
    st.session_state.character = ""
if "current_session" not in st.session_state:
    st.session_state.current_session = get_timestamp()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

for message in st.session_state.messages:
    if isinstance(message["content"], list):
        # 展示图片
        for item in message["content"]:
            if item.get("type") == "image_url":
                img_url = item["image_url"]["url"]
                # 提取 base64 部分（去掉 data:image/jpeg;base64, 前缀）
                base64_data = img_url.split(",", 1)[1]
                # 解码为字节
                image_bytes = base64.b64decode(base64_data)
                # 现在 image_bytes 就等于 uploaded_file.getvalue()
                st.chat_message(message["role"]).image(image_bytes, width=IMAGE_WIDTH)
            elif item.get("type") == "text":
                st.chat_message(message["role"]).write(item["text"])
    else:
        st.chat_message(message["role"]).write(message["content"])

# 性格初始化
nature = """
    你的名字是：%s，你需要以一个朋友的视角和我对话，尽量简洁，涉及代码相关的问题可以详细说明，你的性格是：%s
"""
# 侧边栏布局
with st.sidebar:
    # 音乐播放 Start-----------------------
    # b64_audio = get_audio_base64("sources/晴天.mp3")
    # audio_html = f"""
    # <audio autoplay="true" loop="true" controls style="width: 100%;">
    #     <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mpeg">
    # </audio>
    # """
    # st.markdown(audio_html, unsafe_allow_html=True)
    # 音乐播放 End-----------------------

    new_message = st.button("新建会话", icon="✏️", width="stretch")
    st.divider()
    st.subheader("会话历史")

    # 循环遍历文件夹，输出文件名
    files = []
    if os.path.exists("message_list"):
        files = [f[:-5] for f in os.listdir("message_list") if f.endswith(".json")]
    files.sort(reverse=True)
    for file in files:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.button(file, key=f"load_{file}", width="stretch",
                      type="primary" if file == st.session_state.current_session else "secondary",
                      on_click=lambda f=file: load_message(f))
        with col2:
            st.button("", key=f"del_{file}", icon="❌️", width="stretch", on_click=lambda f=file: del_message(f))

    st.divider()
    st.subheader("AI 基础设置")
    nick_name = st.text_input("AI 昵称", placeholder="请输入 AI 昵称", value=st.session_state.nick_name)
    st.session_state.nick_name = nick_name
    character = st.text_area("AI 性格", placeholder="请输入 AI 性格", value=st.session_state.character)
    st.session_state.character = character

    if new_message:
        save_message()
        st.rerun()

# 底部固定区域
with st._bottom:
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], key="image_uploader")
    prompt = st.chat_input(placeholder="请输入您想问的问题")

# 构建消息
messages = [{"role": "system",
             "content": nature % (st.session_state.nick_name if st.session_state.nick_name else "凡特吸",
                                  st.session_state.character if st.session_state.character else "ai助理")}]

temp_content = []
# 图片管理
if uploaded_file and not st.session_state.uploaded_file:
    st.session_state.uploaded_file = uploaded_file
if st.session_state.uploaded_file:
    # 处理图片
    image_data = st.session_state.uploaded_file.getvalue()
    st.chat_message("user").image(image_data, width=IMAGE_WIDTH)
    if image_data:
        # 上传图片
        base64_image = base64.b64encode(image_data).decode('utf-8')
        # 本地图片
        # base64_image = base64.b64encode(open(image_path, "rb").read()).decode()
        messages = messages + st.session_state.messages
        temp_content = [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
        ]
    st.session_state.uploaded_file = None
# 处理文本
if prompt:

    st.chat_message("user").write(f"{prompt}")

    temp_message = {
        "role": "user",
        "content": [
            *temp_content,
            {"type": "text", "text": prompt}
        ] if temp_content else prompt
    }

    messages.append(temp_message)
    st.session_state.messages.append(temp_message)

    temp_content = []
    st.session_state.uploaded_file = None

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        stream=True
    )

    # 流式输出解析格式
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            stream=True
        )

        response_message = ""
        response_empty = st.empty()
        for ms in response:
            if ms.choices[0].delta.content is not None:
                response_message += ms.choices[0].delta.content
                response_empty.chat_message("assistant").write(response_message)

        st.session_state.messages.append({"role": "assistant", "content": response_message})
    except Exception as e:
        st.error(f"API 调用失败：{str(e)}")
        st.session_state.messages.append({"role": "assistant", "content": f"抱歉，出现错误：{str(e)}"})
