# /api/commands/translate.py

import os
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- 模板配置区域 ---
# ✨ 1. 从环境变量获取 API 密钥
API_KEY = os.getenv("AI_TOKEN") 

# ✨ 2. API 端点 (Base URL)
BASE_URL = "https://api.openai.com/v1"

# ✨ 3. 模型 ID
# 对于翻译任务，使用一个能力强、速度快的模型即可。
MODEL_ID = "gpt-3.5-turbo" # 或 "gemini-1.5-flash-latest"

# ✨ 4. 命令触发词
COMMAND_TRIGGER = "t" # 使用 "t" 作为快捷命令
# --- 模板配置区域结束 ---


async def translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理 /t 命令，调用 AI 进行翻译"""
    if not update.message or not update.message.text:
        return

    text_to_translate = " ".join(context.args)
    if not text_to_translate:
        await update.message.reply_text(f"请在 `/{COMMAND_TRIGGER}` 后面输入需要翻译的内容。")
        return

    thinking_message = await update.message.reply_text("⏳ Translating...")

    # --- API 请求构建 ---
    headers = { "Content-Type": "application/json" }
    
    # 定义一个强大的系统提示，让 AI 专注翻译
    system_prompt = "你是一个专业的、精通多种语言的翻译引擎。请将用户提供的文本进行中英互译。你的任务是：1. 自动检测源语言。2. 将其翻译成另一种语言（中文翻译成英文，英文翻译成中文）。3. 只返回翻译后的纯文本结果，不要包含任何多余的解释、说明、原文或任何形式的客套话。"

    # 根据模型适配请求
    if "gemini" in MODEL_ID.lower():
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent?key={API_KEY}"
        # Gemini 的 System Prompt 在 "systemInstruction" 字段中
        data = {
            "contents": [{"parts": [{"text": text_to_translate}]}],
            "systemInstruction": {"parts": [{"text": system_prompt}]}
        }
    else:
        headers["Authorization"] = f"Bearer {API_KEY}"
        api_url = f"{BASE_URL}/chat/completions"
        # OpenAI & 兼容服务的 System Prompt 在 messages 数组的第一个元素
        data = {
            "model": MODEL_ID,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text_to_translate}
            ],
            "stream": False
        }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(api_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            
            # --- 响应解析 ---
            if "gemini" in MODEL_ID.lower():
                ai_reply = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "AI 未能提供有效翻译。")
            else:
                ai_reply = result.get("choices", [{}])[0].get("message", {}).get("content", "AI 未能提供有效翻译。")
            
            await context.bot.edit_message_text(
                text=ai_reply,
                chat_id=thinking_message.chat_id,
                message_id=thinking_message.message_id
            )

    except httpx.HTTPStatusError as e:
        error_details = e.response.text
        await context.bot.edit_message_text(
            text=f"翻译时出错 (HTTP {e.response.status_code}):\n`{error_details}`",
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
    app.add_handler(CommandHandler(COMMAND_TRIGGER, translate_command))
