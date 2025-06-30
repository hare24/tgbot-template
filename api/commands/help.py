# api/commands/help.py
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """显示所有可用命令的帮助信息。"""
    # 从 context.bot_data 中获取我们预设的命令列表
    commands = context.bot_data.get('bot_commands', [])
    
    if not commands:
        help_text = "当前没有可用的命令。"
    else:
        help_lines = ["你可以使用以下命令："]
        for command in commands:
            help_lines.append(f"/{command.command} - {command.description}")
        help_text = "\n".join(help_lines)
        
    await update.message.reply_text(help_text)

def register(app: Application):
    """将 /help 命令处理器注册到 application"""
    app.add_handler(CommandHandler("help", help_command))

    # 在这里，我们可以预设所有命令的描述，以便 /help 命令和 Telegram 客户端都能看到
    # 这是一个更高级、更优雅的方案
    bot_commands = [
        BotCommand("start", "开始与机器人对话"),
        BotCommand("help", "显示此帮助信息"),
        BotCommand("ask", "向AI提问"),
        BotCommand("t", "翻译文本内容"),
    ]
    # 我们将这个列表存储在 bot_data 中，这是一个可以在所有处理器之间共享数据的字典
    app.bot_data['bot_commands'] = bot_commands
    # 我们还应该调用 set_my_commands，这样在 Telegram 客户端的命令菜单里也会显示这些命令
    # app.post_init = app.bot.set_my_commands(bot_commands) # 这一行在 serverless 环境下需要小心使用，我们先用 bot_data 的方式
