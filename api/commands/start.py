# api/commands/start.py
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """当用户发送 /start 时，回复一条欢迎消息。"""
    if update.effective_user:
        user_name = update.effective_user.mention_html()
        await update.message.reply_html(
            f"你好, {user_name}! 很高兴为你服务。"
        )
    else:
        await update.message.reply_text("你好! 很高兴为你服务。")

def register(app: Application):
    """将 /start 命令处理器注册到 application"""
    app.add_handler(CommandHandler("start", start_command))
