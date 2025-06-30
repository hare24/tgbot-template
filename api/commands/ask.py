# /api/commands/ask.py

import os
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- 模板配置区域 ---
# ✨ 1. 从环境变量获取 API 密钥
# 对应服务商提供的 API Key。例如：sk-..., gsk-..., ds-...
API_KEY = os.getenv("AI_TOKEN") 

# ✨ 2. API 端点 (Base URL)
# 对于 OpenAI 兼容的服务 (如 DeepSeek), 修改这里即可。
# 对于 Gemini, URL 格式不同，需要特别处理。
BASE_URL = "https://api.openai.com/v1"  # 默认使用 OpenAI

# ✨ 3. 模型 ID
MODEL_ID = "gpt-3.5-turbo" # 例如: "gpt-4", "deepseek-chat", "gemini-1.5-pro-latest"

# ✨ 4. 命令触发词
COMMAND_TRIGGER = "ask"
# --- 模板配置区域结束 ---


async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理 /ask 命令，向 AI 提问"""
    if not update.message or not update.message.text:
        return

    user_prompt = " ".join(context.args)
    if not user_prompt:
        await update.message.reply_text(f"请在 `/{COMMAND_TRIGGER}` 后面输入你的问题。")
        return

    thinking_message = await update.message.reply_text("🤔 Thinking...")
    
    # --- API 请求构建 ---
    # 这部分是适配不同 API 的核心
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # 决定使用哪个 URL 和 Key
    # Gemini 的请求方式与其他家都不同，需要特殊处理
    if "gemini" in MODEL_ID.lower():
        # Gemini: Key 在 URL 参数里，Header 里不需要
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent?key={API_KEY}"
        
        # Gemini: 请求体结构也不同
        data = {
            "contents": [{
                "parts": [{"text": user_prompt}]
            }]
        }
    else:
        # OpenAI & 兼容服务 (如 DeepSeek): Key 在 Header 里
        headers["Authorization"] = f"Bearer {API_KEY}"
        api_url = f"{BASE_URL}/chat/completions" # 标准的 completions 端点
        
        # OpenAI & 兼容服务: 标准的 messages 结构
        data = {
            "model": MODEL_ID,
            "messages": [
                {"role": "user", "content": user_prompt}
            ],
            "stream": False
        }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(api_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            
            # --- 响应解析 ---
            # 这部分也需要适配
            if "gemini" in MODEL_ID.lower():
                # Gemini 的回复结构
                ai_reply = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "AI 未能提供有效回复。")
            else:
                # OpenAI & 兼容服务的回复结构
                ai_reply = result.get("choices", [{}])[0].get("message", {}).get("content", "AI 未能提供有效回复。")
            
            await context.bot.edit_message_text(
                text=ai_reply,
                chat_id=thinking_message.chat_id,
                message_id=thinking_message.message_id
            )

    except httpx.HTTPStatusError as e:
        error_details = e.response.text
        await context.bot.edit_message_text(
            text=f"请求 AI 时出错 (HTTP {e.response.status_code}):\n`{error_details}`",
            chat_id=thinking_message.chat_id,
            message_id=thinking_message.message_id,
            parse_mode='Markdown'
        )
    except Exception as e:
        await context.bot.edit_message_text(
            text=f"发生未知错误: {e}",
            chat_id=thinking_message.chat_id,
            message_id=thinking_message.message_id
        )

def register(app: Application):
    """将命令处理器注册到 application"""
    app.add_handler(CommandHandler(COMMAND_TRIGGER, ask_command))
