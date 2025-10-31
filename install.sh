#!/bin/bash
###############################################################################
# DeepSeek-OCR-Web 一键初始化脚本（API 版本）
# 功能：
#  - 创建 Python 虚拟环境
#  - 安装后端依赖
#  - 可选：安装前端依赖
#  - 初始化 .env 并写入 DeepSeek API 配置信息
###############################################################################

set -e

GREEN="\033[1;32m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
RESET="\033[0m"

info()  { echo -e "${GREEN}$1${RESET}"; }
warn()  { echo -e "${YELLOW}$1${RESET}"; }
error() { echo -e "${RED}$1${RESET}"; }

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_DIR="${ROOT_DIR}/.venv"

info "============================================================"
info "🚀 DeepSeek-OCR-Web 环境初始化开始..."
info "============================================================"

# 1️⃣ 创建 Python 虚拟环境
if [ ! -d "$ENV_DIR" ]; then
  warn ">>> Step 1. 创建 Python 虚拟环境 (.venv)"
  python3 -m venv "$ENV_DIR"
else
  warn ">>> Step 1. 检测到已存在的 .venv，跳过创建"
fi

# shellcheck disable=SC1091
source "${ENV_DIR}/bin/activate"

# 2️⃣ 安装后端依赖
warn ">>> Step 2. 安装后端依赖 (requirements.txt)"
pip install --upgrade pip
pip install -r requirements.txt

# 3️⃣ 初始化 .env
ENV_FILE="${ROOT_DIR}/.env"
warn ">>> Step 3. 初始化 .env 配置"
if [ ! -f "$ENV_FILE" ]; then
  cat > "$ENV_FILE" <<'EOF'
DEEPSEEK_API_KEY=
DEEPSEEK_BASE_URL=https://api.siliconflow.cn/v1
DEEPSEEK_MODEL_ID=deepseek-ai/DeepSeek-OCR
EOF
  info "✅ 已生成 .env 文件，请填写真实的 DEEPSEEK_API_KEY。"
else
  info "ℹ️ 检测到已有 .env 文件，未做改动。"
fi

# 4️⃣ 安装前端依赖（可选）
if [ -d "${ROOT_DIR}/frontend" ]; then
  read -r -p "是否安装前端依赖 (npm install)? [y/N] " install_frontend
  if [[ "$install_frontend" =~ ^[Yy]$ ]]; then
    warn ">>> Step 4. 安装前端依赖"
    pushd "${ROOT_DIR}/frontend" >/dev/null
    npm install
    popd >/dev/null
    info "✅ 前端依赖安装完成"
  else
    warn "⚠️ 已跳过前端依赖安装，可在 frontend/ 目录自行执行 npm install"
  fi
else
  warn "⚠️ 未找到 frontend 目录，跳过前端依赖安装步骤"
fi

info "============================================================"
info "🎉 初始化完成！请确认并填写 .env 中的 DEEPSEEK_API_KEY 后启动项目。"
info "============================================================"
