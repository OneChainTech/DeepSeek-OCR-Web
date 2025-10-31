"""
config_loader.py
----------------
该模块负责：
1. 从 .env 文件中加载 DeepSeek OCR API 所需配置；
2. 自动创建 workspace 目录结构（uploads / results / logs）；
3. 校验关键配置项并输出当前配置状态；
4. 提供全局常量供其他模块导入使用。
"""

import os
from pathlib import Path
from dotenv import load_dotenv


# ========== Step 1. 定义路径常量 ==========
BASE_DIR = Path(__file__).resolve().parent.parent   # 项目根目录（DeepSeek-OCR）
WORKSPACE_PATH = BASE_DIR / "workspace"
UPLOAD_DIR = WORKSPACE_PATH / "uploads"
RESULTS_DIR = WORKSPACE_PATH / "results"
LOGS_DIR = WORKSPACE_PATH / "logs"


# ========== Step 2. 自动创建 .env.example 文件 ==========
ENV_FILE = BASE_DIR / ".env"
EXAMPLE_ENV_FILE = BASE_DIR / ".env.example"

if not EXAMPLE_ENV_FILE.exists():
    with open(EXAMPLE_ENV_FILE, "w", encoding="utf-8") as f:
        f.write(
            "# DeepSeek-OCR 后端配置文件示例\n"
            "# 请复制为 .env 并填写下列 API 信息。\n\n"
            "DEEPSEEK_API_KEY=\n"
            "DEEPSEEK_BASE_URL=https://api.siliconflow.cn/v1\n"
            "DEEPSEEK_MODEL_ID=deepseek-ai/DeepSeek-OCR\n"
            "MAX_CONCURRENCY=5\n"
        )


# ========== Step 3. 加载 .env 文件 ==========
if not ENV_FILE.exists():
    print("[⚠️ Warning] 未找到 .env 文件，已创建示例 .env.example。")
    print("请复制 .env.example → .env 并填写 DeepSeek API 相关配置后重启服务。")

load_dotenv(ENV_FILE)


# ========== Step 4. 读取配置项 ==========
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.siliconflow.cn/v1")
DEEPSEEK_MODEL_ID = os.getenv("DEEPSEEK_MODEL_ID", "deepseek-ai/DeepSeek-OCR")
MAX_CONCURRENCY = int(os.getenv("MAX_CONCURRENCY", "5"))


# ========== Step 5. 校验配置 ==========
missing_keys = []
if not DEEPSEEK_API_KEY:
    missing_keys.append("DEEPSEEK_API_KEY")

if missing_keys:
    joined = ", ".join(missing_keys)
    raise ValueError(f"❌ 未在 .env 中设置必要的 API 配置，请补充: {joined}")


# ========== Step 6. 自动创建工作目录 ==========
for directory in [WORKSPACE_PATH, UPLOAD_DIR, RESULTS_DIR, LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)


# ========== Step 7. 调试输出（打印当前有效配置） ==========
print("=" * 60)
print("🔧 DeepSeek-OCR API 配置加载完成")
print(f"🔑 已检测到 API Key: {'是' if DEEPSEEK_API_KEY else '否'}")
print(f"🌐 Base URL:        {DEEPSEEK_BASE_URL}")
print(f"🧠 模型 ID:         {DEEPSEEK_MODEL_ID}")
print(f"⚙️  最大并发任务数: {MAX_CONCURRENCY}")
print(f"📂 工作区路径:      {WORKSPACE_PATH}")
print("=" * 60)


# ========== Step 8. 导出可供全局调用的常量 ==========
__all__ = [
    "DEEPSEEK_API_KEY",
    "DEEPSEEK_BASE_URL",
    "DEEPSEEK_MODEL_ID",
    "MAX_CONCURRENCY",
    "WORKSPACE_PATH",
    "UPLOAD_DIR",
    "RESULTS_DIR",
    "LOGS_DIR",
]
