import json

import select
import streamlit as st
import os
from openai import OpenAI
from datetime import datetime

# 页面布局
st.title("三家村AI助手")
st.write("这里是一个AI助手，你可以输入任何问题，AI会进行回答")
st.set_page_config(page_title="AI", layout="centered", page_icon="🤖")

# 侧边栏ai消息控制
if "nick_name" not in st.session_state:
    st.session_state.nick_name = ""
if "character" not in st.session_state:
    st.session_state.character = ""


def save_session():
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

    #保存历史对话，重置新对话
    st.session_state.messages = []
    st.session_state.current_session = get_timestamp()
    st.session_state.nick_name = ""
    st.session_state.character = ""


def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def load_message(file):
    save_session()
    with open(f"message_list/{file}.json", "r", encoding="utf-8") as f:
        message = json.load(f)
    st.session_state.current_session = message["current_session"]
    st.session_state.nick_name = message["nick_name"]
    st.session_state.character = message["character"]
    st.session_state.messages = message["messages"]
    # print(file)


# 侧边栏布局
with st.sidebar:
    st.subheader("AI基础设置")
    new_message = st.button("新建会话", icon="✏️", width="stretch")
    st.text("会话历史")

    file_path = []
    if os.path.exists("message_list"):
        for file in os.listdir("message_list"):
            if file.endswith(".json"):
                file_path.append(file[0:-5:1])

    for file in file_path:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.button(file, key=f"load_{file}", width="stretch", type="primary", on_click=lambda f=file: load_message(f))
            print(file)
        with col2:
            st.button("", key=f"del_{file}", icon="🗑️", width="stretch")

    nick_name = st.text_input("请输入姓名", placeholder="请输入你的昵称", value=st.session_state.nick_name)
    st.session_state.nick_name = nick_name
    character = st.text_area("请输入性格", placeholder="请输入你的性格", value=st.session_state.character)
    st.session_state.character = character

    if "current_session" not in st.session_state:
        st.session_state.current_session = get_timestamp()
    if new_message:
        save_session()
        st.rerun()

# 性格初始化
natrue = """
    你的名字是：%s，你需要以一个朋友的视角和我对话，尽量简洁，涉及代码相关的问题可以详细说明，你的性格是：%s
"""

# 控制chat展示元素
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'), base_url="https://api.deepseek.com")

prompt = st.chat_input("请输入您想问的问题")
if prompt:
    # 用户信息
    st.chat_message("user").write(f"{prompt}")
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system",
                   "content": natrue % (st.session_state.nick_name, st.session_state.character)},
                  *st.session_state.messages],
        stream=True
    )
    # #非流式输出解析格式
    # response_message = response.choices[0].message.content
    # print(response_message)
    # st.chat_message("assistant").write(response_message)

    # 流式输出解析格式
    response_message = ""
    response_empty = st.empty()
    for ms in response:
        if ms.choices[0].delta.content is not None:
            response_message += ms.choices[0].delta.content
            response_empty.chat_message("assistant").write(response_message)

    st.session_state.messages.append({"role": "assistant", "content": response_message})

    print(ms)
