"""
inference_runner.py
-------------------
DeepSeek OCR 后端核心执行器
支持：
- 自动识别 PDF / 图片
- 实时进度回调
- 任务状态 JSON 持久化
"""

from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path
from typing import Callable, Optional, Dict, Any, List, Tuple

import fitz  # PyMuPDF
from PIL import Image

from backend.config_loader import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MODEL_ID,
    LOGS_DIR,
)
from backend.deepseek_api import call_deepseek_ocr, DeepSeekAPIError, detect_mime_type
from backend.file_manager import detect_file_type, create_result_dir, list_result_files


# ====== 任务状态持久化 ======
def write_task_state(task_id: str, state: Dict[str, Any]):
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    state_path = LOGS_DIR / f"task_{task_id}.json"
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    return state_path


def read_task_state(task_id: str) -> Optional[Dict[str, Any]]:
    state_path = LOGS_DIR / f"task_{task_id}.json"
    if not state_path.exists():
        return None
    try:
        with open(state_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


# ====== 工具方法 ======
def _convert_pdf_to_images(pdf_path: Path, dpi: int = 144) -> List[bytes]:
    """
    将 PDF 每一页渲染为 PNG 格式的字节流。
    """
    images: List[bytes] = []
    doc = fitz.open(pdf_path)
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)

    for page_index in range(doc.page_count):
        page = doc[page_index]
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        images.append(pix.tobytes("png"))

    doc.close()
    return images


def _prepare_image_bytes(image_path: Path) -> Tuple[bytes, str]:
    """
    读取图片文件并返回字节流与 MIME 类型。
    """
    mime_type = detect_mime_type(str(image_path))
    data = image_path.read_bytes()

    # 某些情况下 MIME type 猜测失败或返回未知类型，这里统一转换为 PNG
    if not mime_type.startswith("image/"):
        with Image.open(BytesIO(data)) as im:
            buffer = BytesIO()
            im.save(buffer, format="PNG")
            data = buffer.getvalue()
            mime_type = "image/png"

    return data, mime_type


# ====== 核心任务执行 ======
def run_ocr_task(
    input_path: str,
    task_id: str,
    on_progress: Optional[Callable[[int], None]] = None,
    prompt: str = "<image>\nFree OCR.",
) -> Dict[str, Any]:
    """执行 OCR 任务"""
    try:
        result_dir = create_result_dir(prefix=f"ocr_task_{task_id}")
        write_task_state(task_id, {"status": "running", "result_dir": str(result_dir)})

        file_type = detect_file_type(input_path)
        print(f"🚀 启动 DeepSeek OCR 任务 ({file_type.upper()})")
        print(f"📁 输出路径: {result_dir}")

        pages: List[Tuple[bytes, str]] = []
        input_file = Path(input_path)

        if file_type == "pdf":
            print("📄 检测到 PDF，开始逐页渲染...")
            page_images = _convert_pdf_to_images(input_file)
            pages = [(img, "image/png") for img in page_images]
        else:
            print("🖼️ 检测到图片，准备调用 OCR API...")
            pages.append(_prepare_image_bytes(input_file))

        total_pages = len(pages)
        if total_pages == 0:
            raise RuntimeError("未生成任何可识别的图片页面。")

        markdown_sections: List[str] = []
        page_output_dir = Path(result_dir) / "pages"
        page_output_dir.mkdir(parents=True, exist_ok=True)

        for idx, (image_bytes, mime_type) in enumerate(pages, start=1):
            print(f"🔍 正在识别第 {idx}/{total_pages} 页 ...")
            try:
                content = call_deepseek_ocr(
                    api_key=DEEPSEEK_API_KEY,
                    base_url=DEEPSEEK_BASE_URL,
                    model_id=DEEPSEEK_MODEL_ID,
                    image_bytes=image_bytes,
                    mime_type=mime_type,
                    prompt=prompt,
                )
            except DeepSeekAPIError as exc:
                raise RuntimeError(f"第 {idx} 页识别失败: {exc}") from exc

            section_header = f"## Page {idx}\n"
            markdown_sections.append(f"{section_header}\n{content.strip()}\n")

            page_file = page_output_dir / f"page_{idx}.md"
            page_file.write_text(content.strip() + "\n", encoding="utf-8")

            progress = int(idx / total_pages * 100)
            write_task_state(
                task_id,
                {
                    "status": "running",
                    "result_dir": str(result_dir),
                    "progress": progress,
                    "current_page": idx,
                    "total_pages": total_pages,
                },
            )

            if on_progress:
                on_progress(progress)

        final_markdown = "\n".join(markdown_sections).strip() + "\n"
        combined_path = Path(result_dir) / "result.md"
        combined_path.write_text(final_markdown, encoding="utf-8")

        metadata = {
            "pages": total_pages,
            "prompt": prompt,
            "model": DEEPSEEK_MODEL_ID,
        }
        metadata_path = Path(result_dir) / "metadata.json"
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

        files = list_result_files(result_dir)
        write_task_state(
            task_id,
            {
                "status": "finished",
                "result_dir": str(result_dir),
                "files": files,
                "progress": 100,
            },
        )

        print(f"✅ 任务完成：{task_id}")
        return {"status": "finished", "task_id": task_id, "result_dir": str(result_dir), "files": files}

    except Exception as e:
        write_task_state(task_id, {"status": "error", "message": str(e)})
        print(f"❌ 任务异常 {task_id}: {e}")
        return {"status": "error", "message": str(e)}
