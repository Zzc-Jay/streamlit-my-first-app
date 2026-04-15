# ========================================
#  全局配置 — 模型、常量、提示词模板
# ========================================

IMAGE_WIDTH = 300

# 可用模型列表（名称 → 配置）
MODELS = {
    "豆包 (doubao-seed-vision)": {
        "model": "doubao-seed-1-6-vision-250815",
        "api_key_env": "ARK_API_KEY",
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
    },
    "千问 (qwen-vl-plus)": {
        "model": "qwen-vl-plus",
        "api_key_env": "DASHSCOPE_API_KEY",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    },
}

DEFAULT_MODEL = "千问 (qwen-vl-plus)"

# 系统提示词
SYSTEM_PROMPT_TEMPLATE = (
    "你的名字是：{nick_name}，你需要以一个朋友的视角和我对话，"
    "尽量简洁，涉及代码相关的问题可以详细说明，你的性格是：{character}"
)

DEFAULT_NICK_NAME = "太阳之子"
DEFAULT_CHARACTER = "理性的编程大佬，带有一些幽默感"

# 头像
USER_AVATAR = "🥷🏻"
ASSISTANT_AVATAR = "🤪"
