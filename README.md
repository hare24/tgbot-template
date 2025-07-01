<div align="center">

# 🤖 Telegram Bot Template

**一个为现代云平台优化的、高性能、可复用的 Telegram 机器人模板**<br>
**A high-performance, reusable Telegram Bot template optimized for modern cloud platforms.**

<br>

<!-- All badges are now written in pure HTML for consistent rendering -->
<p>
    <a href="https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fhare24%2Ftgbot-template">
      <img src="https://vercel.com/button" alt="Deploy with Vercel"/>
    </a>
     
    <a href="https://shields.io/badge/python-3.9%2B-blue?logo=python&logoColor=white">
      <img alt="Python Version" src="https://img.shields.io/badge/python-3.9%2B-blue?logo=python&logoColor=white">
    </a>
     
    <a href="https://shields.io/badge/Framework-Starlette-05998b?logo=fastapi&logoColor=white">
      <img alt="Framework" src="https://img.shields.io/badge/Framework-Starlette-05998b?logo=fastapi&logoColor=white">
    </a>
     
    <a href="https://github.com/<你的GitHub用户名>/<你的仓库名>/blob/main/LICENSE">
      <img alt="License" src="https://img.shields.io/github/license/hare24/tgbot-template">
    </a>
</p>

</div>

---

## 📖 项目简介 | Overview

这不仅仅是又一个 Telegram 机器人。这是一个经过反复调试与优化的 **Serverless-First** 架构模板，旨在解决在 Vercel 等现代无服务器平台上部署异步 Python 应用时可能遇到的所有常见陷阱。

This is more than just another Telegram bot. It's a **Serverless-First** architectural template, meticulously debugged and optimized to solve all the common pitfalls encountered when deploying asynchronous Python applications on modern serverless platforms like Vercel.

**核心哲学：拥抱无状态 (Embracing Statelessness)**
我们没有试图在“阅后即焚”的无服务器环境中构建一个需要持久状态的应用，而是为每一次请求创建一个全新的、独立的机器人实例。这保证了最佳的性能、稳定性和资源利用率。

Our core philosophy is to embrace the stateless nature of serverless environments. Instead of trying to maintain a persistent state, we create a fresh, isolated bot instance for every single incoming request. This ensures maximum performance, stability, and resource efficiency.

---

## ✨ 项目特色 | Features

- **🚀 极速响应 (Blazing Fast)**: 基于 `Starlette` 的全异步架构，几乎可以瞬时响应 Telegram 的 Webhook 请求。
- **🧩 优雅的模块化 (Elegant Modularity)**: 所有命令逻辑都分离在 `api/commands/` 目录中。添加或修改命令无需触及核心代码，真正实现“即插即用”。
- **🤖 AI 集成模板 (AI-Ready)**: 内置了与大语言模型 (LLM) 交互的标准模板 (`ask.py`, `translate.py`)，以 OpenAI API 格式为标准，并内置了对 Gemini 的适配。
- **☁️ Vercel 深度优化 (Vercel-Optimized)**: `vercel.json` 和项目结构都为 Vercel 的构建和路由系统量身定制。
- **🎯 专注与纯粹 (Focused & Pure)**: 摒弃了本地运行的复杂性，专注于“一键部署到云端”这一核心目标，对初学者极其友好。

---

## 🚀 部署指南 | Deployment Guide

本项目推荐使用 Vercel 进行一键部署。

### 1. 部署到 Vercel | Deploy to Vercel

点击下方按钮，Vercel 将引导你完成所有步骤。

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fhare24%2Ftgbot-template)

### 2. 配置环境变量 | Configure Environment Variables

在 Vercel 的项目配置页面，你需要设置以下两个环境变量：

| 变量名 (Variable) | 必填 (Required) | 描述 (Description)                                 |
|------------------|:--------------:|----------------------------------------------------|
| `TELEGRAM_TOKEN` |       ✅       | 你的 Telegram Bot Token，从 [@BotFather](https://t.me/BotFather) 获取。 Your Telegram Bot Token from @BotFather. |
| `AI_TOKEN`       |       ✅       | 你选择的 AI 服务的 API Key。 Your chosen AI service's API Key. |

### 3. 设置 Webhook | Set Up Webhook

部署成功后，Vercel 会提供一个唯一的部署 URL (例如 `https://your-project.vercel.app`)。你需要执行以下命令，将你的机器人指向这个地址。**记得在 URL 末尾加上斜杠 `/`**。

```bash
curl "https://api.telegram.org/bot<你的TELEGRAM_TOKEN>/setWebhook?url=<你的Vercel部署URL>/"

```
## 🛠️ 如何扩展 | How to Extend

### 添加新命令 | Adding a New Command

1.  在 `api/commands/` 目录下创建一个新的 Python 文件 (例如 `ping.py`)。
2.  在该文件中，编写命令处理函数，并导出一个 `register` 函数。
    ```python
    # /api/commands/ping.py
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes

    async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Pong!")

    def register(app: Application):
        app.add_handler(CommandHandler("ping", ping_command))
    ```
3.  **完成！** 提交代码到 GitHub，Vercel 会自动重新部署，新的 `/ping` 命令即刻生效。

### 修改 AI 命令 | Modifying AI Commands

打开 `api/commands/ask.py` 或 `translate.py`。文件顶部的“模板配置区域”允许你轻松更换 `MODEL_ID` 或 `BASE_URL` 来适配不同的 AI 服务。

---

## 📄 许可协议 | License

本项目遵循 [MIT License](./LICENSE)。

This project is licensed under the MIT License.
```
