import os
import logging
import importlib
from telegram import Update
from telegram.ext import Application
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response

# --- 全局配置 ---
# 只有这些配置信息是全局的，它们是无状态的
logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN environment variable not set!")

# --- Starlette 应用 ---
# 我们只在全局创建一个空的 Web 应用骨架
app = Starlette()

# --- 核心 Webhook 逻辑 ---
@app.route("/", methods=["POST"])
async def webhook(request: Request) -> Response:
    """
    为每个请求创建一个全新的、独立的 Application 实例。
    这是在无服务器环境中最健壮的模式。
    """
    
    # 1. 在函数内部创建 application，它的生命周期与本次请求相同
    application = Application.builder().token(TOKEN).build()

    # 2. 动态加载所有命令处理器到这个新实例上
    commands_dir = os.path.join(os.path.dirname(__file__), 'commands')
    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"api.commands.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "register"):
                    module.register(application)
            except Exception as e:
                logging.error(f"Failed to load module {module_name}: {e}")
    
    # 3. 在处理请求前，先初始化这个全新的 application
    await application.initialize()
    
    try:
        # 4. 正常处理请求
        data = await request.json()
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        
        return Response(content="OK", status_code=200)
    
    except Exception as e:
        logging.error(f"Error processing update: {e}", exc_info=True)
        return Response(content="Internal Server Error", status_code=500)
    
    finally:
        # 5. 在请求结束时，无论成功与否，都优雅地关闭 application
        # 这会正确地清理所有网络连接，避免“事件循环已关闭”的错误
        await application.shutdown()
