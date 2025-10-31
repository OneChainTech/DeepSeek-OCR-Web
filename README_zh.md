<div align="center">
  <h1>DeepSeek-OCR 可视化平台</h1>
  <span>中文 | <a href="./README.md">English</a></span>
</div>

## ✨ 项目概览

DeepSeek-OCR 可视化平台是一个基于 DeepSeek-OCR 模型的文档理解工具，  
前端采用 React/Vite，后端采用 FastAPI，能够对 PDF、图片等多模态文档进行高精度识别，  
并输出结构化 Markdown、图表/表格解析等结果。

<div align="center">
  <img src="assets/项目图片.png" width="720" alt="DeepSeek-OCR Studio 界面预览" />
</div>

## 📌 核心能力

- **多格式输入**：支持上传 PDF、PNG、JPG 等格式，并自动拆分多页文件。
- **高精度 OCR**：调用 DeepSeek-OCR 模型，兼容多语言识别，自动清洗 Grounding 标签。
- **结构化 Markdown**：识别结果按页合并，修复图片路径，输出可编辑的 Markdown。
- **表格/图表解析**：针对表格、数据可视化图反向生成结构化内容。
- **交互式工作区**：包含文件树、结果预览、提示词模板和通知提示。
- **任务追踪**：后台轮询任务进度，避免重复分页内容，输出可下载文件。

## 🧱 架构与目录

- **前端**（Vite + React + Tailwind）  
  负责上传、提示词管理、结果预览与通知展示。
- **后端**（FastAPI）  
  处理文件上传、任务管理、调用 DeepSeek API、结果落盘与静态文件服务。
- **DeepSeek API**  
  提供 OCR 推理能力，后台会在合并阶段去除分页重叠内容。
- **工作空间**（`workspace/`）  
  存储上传文件、识别结果、日志与任务状态。

```text
DeepSeek-OCR-Web/
├── backend/                # FastAPI 服务、OCR 执行器、工具函数
├── frontend/               # React 应用及构建脚本
├── packages/               # 离线安装包（见下文）
├── start.sh, install.sh    # 一键安装 / 启动脚本
├── requirements.txt        # Python 依赖清单
└── README.md / README_zh.md
```

## 🖼️ 功能演示

<div align="center">

**PDF 文档解析 - 处理图片、表格等复杂排版**

<img src="assets/文档解析.gif" width="600" alt="PDF 文档解析">

</div>

<div align="center">

| 多语种文字解析 | 图表 & 表格解析 |
|:---:|:---:|
| <img src="assets/多语种.gif" width="400" alt="多语种文字解析"> | <img src="assets/表格解析.gif" width="400" alt="图表 & 表格解析"> |

</div>

<div align="center">

| 专业 CAD / 流程图解析 | 数据可视化逆向表格 |
|:---:|:---:|
| <img src="assets/CAD图纸语义解析.gif" width="400" alt="CAD 图纸语义解析"> | <img src="assets/图表逆向表格.gif" width="400" alt="数据可视化逆向表格"> |

</div>

## ✅ 环境要求

- **操作系统**：推荐 Linux（便于 GPU 推理）
- **GPU**：显存 ≥ 7 GB（大文件建议 16–24 GB），暂不支持 RTX 50 系列
- **Python**：3.10–3.12（推荐 3.10/3.11）
- **CUDA**：11.8 或 12.1/12.2，需与驱动及 PyTorch 版本匹配
- **Node.js**：≥ 18.x（用于 Vite 前端）
- **DeepSeek API**：需要有效的 API Key 与可访问的 Base URL

## 🚀 快速体验（脚本方式）

```bash
# 安装模型权重与依赖
bash install.sh

# 启动前后端服务
bash start.sh
```

默认端口：后端 8002，前端 3000。待日志输出成功后，访问 `http://localhost:3000`。

## 🔧 手动部署步骤

### 1. 配置 DeepSeek 凭证

在项目根目录创建 `.env`：

```env
DEEPSEEK_API_KEY=你的API密钥
DEEPSEEK_BASE_URL=https://api.siliconflow.cn/v1
DEEPSEEK_MODEL_ID=deepseek-ai/DeepSeek-OCR
```

> 如需自建代理或自定义模型，再修改以上地址与模型 ID。

### 2. 后端环境

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8002 --reload
```

后端接口默认暴露在 `http://localhost:8002`。

### 3. 前端环境

```bash
cd frontend
npm install
npm run dev  # 启动后端口默认 3000
```

## 📂 输出目录与日志

- **上传文件**：`workspace/uploads/`
- **识别结果**：`workspace/results/<task_id>/`
- **任务状态 & 日志**：`workspace/logs/`
- **运行日志**：`backend.log` / `frontend.log`（排障时使用，用完可删）

## 📦 可选离线安装包

`packages/` 目录包含离线部署时使用的资源：

- `node-v22.21.0-linux-x64.tar.xz` &mdash; Linux 下的 Node.js 安装包，适用于无网络环境。
- `vllm-0.8.5+cu118-cp38-abi3-manylinux1_x86_64.whl` &mdash; 针对 CUDA 11.8 的 vLLM GPU 预编译包。

如果部署环境能直接 `npm install` 和 `pip install`，可以删除这些包以节约空间。

## 🛠 常见问题

- **启动报 “Address already in use”**  
  端口已被占用。可停止相关进程（如 `pkill -f uvicorn`/`pkill -f node`）或修改启动端口。
- **合并 Markdown 出现表格末行重复**  
  最新版本已在 `backend/inference_runner.py` 的 `_remove_page_overlap` 中自动去重，请保持更新。
- **`npm run build` 提示 chunk 过大**  
  Vite 默认在打包体积超过 500 kB 时提示警告，属于正常现象；如需进一步优化可按需拆包。

## 🙈 参与贡献

欢迎通过 GitHub 提交 Issue 或 Pull Request。  
无论是功能迭代、Bug 修复还是文档改进，都是对社区的帮助。

## 😎 技术交流

扫码添加助理，回复 “DeepSeekOCR” 即可加入技术交流群，与更多伙伴沟通交流。

<div align="center">
  <img src="assets/afe0e4d094987b00012c5129a38ade24.png" width="200" alt="技术交流群二维码">
</div>
