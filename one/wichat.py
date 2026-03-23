import streamlit as st
import os
from openai import OpenAI

if st.session_state.get("messages") is None:
    st.session_state.setdefault("messages", [])
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
        messages=[{"role": "system", "content": "You are a helpful assistant"},
                  *st.session_state.messages],
        stream=True
    )
    # #非流式输出解析格式
    # response_message = response.choices[0].message.content
    # print(response_message)
    # st.chat_message("assistant").write(response_message)

    #流式输出解析格式
    response_message = ""
    response_empty = st.empty()
    for ms in response:
        if ms.choices[0].delta.content is not None:
            response_message += ms.choices[0].delta.content
            response_empty.chat_message("assistant").write(response_message)

    st.session_state.messages.append({"role": "assistant", "content": response_message})

    print(ms)
