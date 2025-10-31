

<div align="center">
  <h1>DeepSeek-OCR 可视化系统</h1>
  <span>中文 | <a href="./README.md">English</a></span>
</div>

## ⚡ 项目简介

本项目是基于 DeepSeek-OCR 的多模态文档解析工具。采用 FastAPI 后端 + React 前端
![项目图片](assets/项目图片.png)
该工具能够高效地处理 PDF 文档和图片，提供强大的光学字符识别（OCR）功能，支持多语种文字识别、表格解析、图表分析等多种功能。
### 主要功能

- **多格式文档解析**：支持 PDF、图片等多种格式的文档上传和解析
- **智能 OCR 识别**：基于 DeepSeek-OCR 模型，提供高精度的文字识别
- **版面分析**：智能识别文档版面结构，准确提取内容布局
- **多语种支持**：支持中文、英文等多种语言的文字识别
- **表格&图表解析**：专业的表格识别和图表数据提取功能
- **专业领域图纸识别**：支持各类专业领域图纸的语义识别
- **数据可视化**：支持数据分析可视化图的逆向解析
- **Markdown 转换**：将 PDF 内容转换为结构化的 Markdown 格式

## 👀 项目演示

<div align="center">

**PDF文档解析 - 支持图片、表格等复杂内容**

<img src="assets/文档解析.gif" width="600" alt="文档解析">

</div>

<div align="center">

| 多语种文字解析 | 图表&表格解析 |
|:---:|:---:|
| <img src="assets/多语种.gif" width="400" alt="多语种文字解析"> | <img src="assets/表格解析.gif" width="400" alt="图表&表格解析"> |

</div>

<div align="center">

| 专业领域图纸语义识别（支持CAD、流程图、装饰图等） | 数据分析可视化图逆向解析 |
|:---:|:---:|
| <img src="assets/CAD图纸语义解析.gif" width="400" alt="CAD图纸语义识别"> | <img src="assets/图表逆向表格.gif" width="400" alt="数据可视化图逆向解析"> |

</div>

## 🚀 使用指南

### 系统要求

⚠️ **重要提示**：
- **操作系统**：需要在 Linux 系统下运行
- **显卡要求**：GPU ≥ 7 GB 显存（大图/多页 PDF 建议 16–24 GB）
- **兼容性说明**：50 系显卡目前不兼容，请使用其他型号显卡
- **Python 版本**：3.10–3.12（推荐 3.10/3.11）
- **CUDA 版本**：11.8 或 12.1/12.2（需与显卡驱动匹配）
- **PyTorch**：需安装与 CUDA 匹配的预编译版本

### 快速开始
#### 方法一、脚本一键启动（推荐）
执行以下脚本即可一键启动

```bash
#安装模型权重及环境依赖
bash install.sh
#启动服务
bash start.sh
```

#### 方法二、手动安装并运行

##### 步骤 1：配置 DeepSeek API
在项目根目录下创建 `.env` 文件，并填写以下字段：

```
DEEPSEEK_API_KEY=你的API密钥
DEEPSEEK_BASE_URL=https://api.siliconflow.cn/v1
DEEPSEEK_MODEL_ID=deepseek-ai/DeepSeek-OCR
```

> 除非使用自建代理或自定义模型，一般保持默认的 `DEEPSEEK_BASE_URL` 与 `DEEPSEEK_MODEL_ID` 即可。

##### 步骤 2：运行环境搭建
创建并激活 Python 虚拟环境，安装依赖：

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

##### 步骤 3：启动后端服务


开启后端
```bash
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```


##### 步骤 4：启动前端服务
安装前端依赖
```bash
npm install
```

开启前端
```bash
npm run dev
```

启动成功后，在浏览器中访问前端地址即可使用。


## 🙈 贡献
欢迎通过GitHub提交 PR 或者issues来对项目进行贡献。我们非常欢迎任何形式的贡献，包括功能改进、bug修复或是文档优化。

## 😎 技术交流
扫描添加小可爱，回复“DeepSeekOCR”加入技术交流群，与其他小伙伴一起交流学习。

<div align="center">
<img src="assets\afe0e4d094987b00012c5129a38ade24.png" width="200" alt="技术交流群二维码">
<div>
