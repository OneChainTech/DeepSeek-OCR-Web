"""
deepseek_api.py
---------------
封装 DeepSeek OCR API 的调用逻辑，提供统一的请求与异常处理。
"""

import base64
import mimetypes
from typing import Optional

import requests


class DeepSeekAPIError(RuntimeError):
    """DeepSeek OCR API 请求异常。"""


def detect_mime_type(file_path: str, fallback: str = "image/png") -> str:
    """根据文件后缀估计 MIME 类型，默认使用 PNG。"""
    mime, _ = mimetypes.guess_type(file_path)
    return mime or fallback


def build_image_data_url(file_bytes: bytes, mime_type: str) -> str:
    """将图片二进制数据编码为 data URL。"""
    encoded = base64.b64encode(file_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def call_deepseek_ocr(
    *,
    api_key: str,
    base_url: str,
    model_id: str,
    image_bytes: bytes,
    mime_type: str,
    prompt: Optional[str] = None,
    timeout: int = 120,
) -> str:
    """
    调用 DeepSeek OCR，返回模型输出的文本内容。

    Args:
        api_key: DeepSeek API Key。
        base_url: API 基础地址，例如 https://api.siliconflow.cn/v1。
        model_id: 模型标识。
        image_bytes: 待识别图片的二进制内容。
        mime_type: 图片的 MIME 类型。
        prompt: 可选提示词。
        timeout: 请求超时时间（秒）。
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data_url = build_image_data_url(image_bytes, mime_type)
    prompt_text = prompt or "<image>\\nFree OCR."

    payload = {
        "model": model_id,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            }
        ],
    }

    endpoint = base_url.rstrip("/") + "/chat/completions"

    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=timeout)
    except requests.RequestException as exc:
        raise DeepSeekAPIError(f"请求 DeepSeek OCR API 失败: {exc}") from exc

    if response.status_code != 200:
        raise DeepSeekAPIError(
            f"DeepSeek OCR API 返回错误状态码 {response.status_code}: {response.text}"
        )

    try:
        data = response.json()
        choices = data.get("choices", [])
        if not choices:
            raise KeyError("choices 为空")
        message = choices[0].get("message", {})
        content = message.get("content")
        if not isinstance(content, str):
            raise KeyError("content 缺失或格式错误")
    except Exception as exc:
        raise DeepSeekAPIError(f"解析 DeepSeek OCR API 响应失败: {exc} -> {response.text}") from exc

    return content.strip()


__all__ = ["DeepSeekAPIError", "call_deepseek_ocr", "build_image_data_url", "detect_mime_type"]
