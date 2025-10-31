<div align="center">
  <h1>DeepSeek-OCR Studio</h1>
  <span><a href="./README_zh.md">中文</a> | English</span>
</div>

## ✨ Overview

DeepSeek-OCR Studio is a document understanding toolkit powered by the DeepSeek-OCR models.  
It combines a modern React/Vite frontend with a FastAPI backend to deliver accurate OCR, table parsing, chart understanding, and Markdown reconstruction for PDFs and images.

<div align="center">
  <img src="assets/项目图片.png" width="720" alt="DeepSeek-OCR Studio UI preview" />
</div>

## 📌 Features

- **Multi-format ingestion** &mdash; Upload PDFs or images (PNG/JPG) and process multi-page files seamlessly.
- **High-precision OCR** &mdash; Uses DeepSeek-OCR for multilingual text recognition and grounding tags cleanup.
- **Layout-aware Markdown** &mdash; Converts content into structured Markdown while fixing image paths.
- **Table & chart extraction** &mdash; Handles tabular data and infers insights from charts or diagrams.
- **Interactive workspace** &mdash; File explorer, preview pane, and prompt templates for refined control.
- **Processing telemetry** &mdash; Real-time task polling, deduplicated page merging, and downloadable outputs.

## 🧱 Architecture

- **Frontend** (Vite + React + Tailwind)  
  Handles uploads, prompt presets, preview rendering, and toast notifications.
- **Backend** (FastAPI)  
  Manages uploads, task orchestration, DeepSeek API calls, result caching, and static serving.
- **DeepSeek API**  
  Provides OCR inference; responses are cleaned for pagination overlap before being persisted.
- **Workspace** (`workspace/`)  
  Persists uploaded files, OCR outputs, logs, and per-task metadata.

```text
DeepSeek-OCR-Web/
├── backend/                # FastAPI service, OCR runner, utilities
├── frontend/               # React application and build scripts
├── packages/               # Optional offline installers (see below)
├── start.sh, install.sh    # Helper scripts for automated setup/startup
├── requirements.txt        # Python runtime dependencies
└── README.md               # Project documentation
```

## 🖼️ Demo Gallery

<div align="center">

**PDF Document Parsing - Handles images, tables, and rich layouts**

<img src="assets/文档解析.gif" width="600" alt="PDF Document Parsing">

</div>

<div align="center">

| Multi-language Text Parsing | Chart & Table Parsing |
|:---:|:---:|
| <img src="assets/多语种.gif" width="400" alt="Multi-language Text Parsing"> | <img src="assets/表格解析.gif" width="400" alt="Chart & Table Parsing"> |

</div>

<div align="center">

| Professional CAD / Diagram Understanding | Data Visualization Reverse Parsing |
|:---:|:---:|
| <img src="assets/CAD图纸语义解析.gif" width="400" alt="CAD Semantic Parsing"> | <img src="assets/图表逆向表格.gif" width="400" alt="Chart to Table Reconstruction"> |

</div>

## ✅ Requirements

- **Operating System**: Linux (recommended for GPU-enabled inference)
- **GPU**: ≥7 GB VRAM (16–24 GB preferred for large PDFs); RTX 50 series currently unsupported
- **Python**: 3.10–3.12 (3.10/3.11 recommended)
- **CUDA**: 11.8 or 12.1/12.2 to match GPU driver and PyTorch build
- **Node.js**: ≥18.x (needed for the Vite frontend)
- **DeepSeek API**: Valid API key and reachable base URL

## 🚀 Quick Start (One-click Scripts)

```bash
# Install model weights and dependencies
bash install.sh

# Start backend and frontend services
bash start.sh
```

Services are launched with default ports (`backend`: 8002, `frontend`: 3000).  
Visit `http://localhost:3000` after both services report that they are running.

## 🔧 Manual Setup

### 1. Configure DeepSeek Credentials

Create `.env` in the project root:

```env
DEEPSEEK_API_KEY=your_api_key
DEEPSEEK_BASE_URL=https://api.siliconflow.cn/v1
DEEPSEEK_MODEL_ID=deepseek-ai/DeepSeek-OCR
```

> Adjust `DEEPSEEK_BASE_URL` or `DEEPSEEK_MODEL_ID` only if you use a custom deployment.

### 2. Backend Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8002 --reload
```

Backend endpoints are now available at `http://localhost:8002`.

### 3. Frontend Environment

```bash
cd frontend
npm install
npm run dev  # start on http://localhost:3000
```

## 📂 Output & Logs

- **Uploads**: `workspace/uploads/`
- **OCR results**: `workspace/results/<task_id>/`
- **Task states & logs**: `workspace/logs/` (created on demand)
- **Runtime logs**: `backend.log`, `frontend.log` (safe to delete when troubleshooting is complete)

## 📦 Optional Offline Packages

`packages/` holds artefacts for air-gapped deployments:

- `node-v22.21.0-linux-x64.tar.xz` &mdash; Node.js bundle for Linux hosts without internet access.
- `vllm-0.8.5+cu118-cp38-abi3-manylinux1_x86_64.whl` &mdash; CUDA 11.8 vLLM wheel for GPU inference.

If your environment can run `npm install` and `pip install` online, you can remove these files.

## 🛠 Troubleshooting

- **“Address already in use” on startup**  
  Another process occupies the port. Stop existing services (e.g., `pkill -f uvicorn` / `pkill -f node`) or change the port via CLI flags.
- **Repeated table rows in merged Markdown**  
  Pagination overlap is automatically trimmed by `_remove_page_overlap` in `backend/inference_runner.py`.  
  Update to the latest version if you still see duplicates.
- **Large bundle warning during `npm run build`**  
  Vite warns when the main bundle exceeds 500 kB. This is expected given the rich UI set; consider code splitting if you customize further.

## 🙈 Contributing

Contributions via pull requests or GitHub Issues are welcome.  
Bug fixes, new features, and documentation improvements all help the community.

## 😎 Technical Communication

Scan to add our assistant. Reply “DeepSeekOCR” to join the technical community and chat with other builders.

<div align="center">
  <img src="assets/afe0e4d094987b00012c5129a38ade24.png" width="200" alt="Technical Communication Group QR Code">
</div>
