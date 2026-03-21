# Please install OpenAI SDK first: `pip3 install openai`
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY'),
    base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "你好"},
    ],
    stream=False
)
# client = OpenAI(
#     # api_key=os.environ.get('OPENAI_API_KEY'),
#     base_url="http://localhost:11434/api/chat")
#
# response = client.chat.completions.create(
#     model="deepseek-r1:1.5b",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant"},
#         {"role": "user", "content": "你好"},
#     ],
#     stream=False
# )

print(response.choices[0].message.content)