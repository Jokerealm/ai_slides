# AI Slides - AI 驱动的 PPT 生成平台

<div align="center">

![Version](https://img.shields.io/badge/version-0.1.6-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![License](https://img.shields.io/badge/license-Apache--2.0-orange.svg)

**只需输入主题和需求，AI 即可自动生成专业的 PPT 演示文稿**

[功能特性](#功能特性) • [快速开始](#快速开始) • [使用指南](#使用指南) • [API 文档](#api-文档) • [开发指南](#开发指南)

</div>

---

## 📖 目录

- [项目简介](#项目简介)
- [功能特性](#功能特性)
- [技术架构](#技术架构)
- [快速开始](#快速开始)
- [使用指南](#使用指南)
- [核心功能](#核心功能)
- [API 文档](#api-文档)
- [配置说明](#配置说明)
- [开发指南](#开发指南)
- [常见问题](#常见问题)
- [更新日志](#更新日志)
- [许可证](#许可证)

---

## 🎯 项目简介

AI Slides 是一个基于人工智能的 PPT 自动生成平台，通过先进的 AI 技术，帮助用户快速创建专业、美观的演示文稿。

### 核心优势

- 🚀 **快速生成**: 几分钟内完成从主题到成品的全流程
- 🎨 **智能设计**: AI 自动优化布局、配色和内容结构
- 🔄 **灵活编辑**: 支持在线编辑和实时预览
- 📦 **多格式导出**: 支持 HTML、PPTX 等多种格式
- 🌐 **API 集成**: 提供 OpenAI 兼容的 API 接口
- 💾 **项目管理**: 完整的项目版本控制和协作功能

---

## ✨ 功能特性

### 🤖 AI 智能生成

- **自动大纲生成**: 根据主题和需求自动生成 PPT 大纲
- **智能内容填充**: AI 自动生成每页幻灯片的内容
- **图片智能匹配**: 自动搜索和生成相关图片
- **样式自动优化**: 智能选择配色方案和布局

### 🎨 模板与样式

- **多场景模板**: 支持商业汇报、教育培训、产品发布等多种场景
- **自定义模板**: 支持创建和管理自定义模板
- **全局模板库**: 内置丰富的模板资源
- **样式一键切换**: 快速更换整体风格

### 📊 内容管理

- **项目管理**: 完整的项目生命周期管理
- **版本控制**: 支持多版本管理和回滚
- **TODO 看板**: 可视化的任务进度跟踪
- **协作编辑**: 支持团队协作和评论

### 🖼️ 图片服务

- **本地图库**: 管理和使用本地图片资源
- **网络搜索**: 集成 Pixabay、Unsplash 等图片源
- **AI 生成**: 支持 DALL-E、Pollinations 等 AI 图片生成
- **智能选择**: 根据内容自动匹配最佳图片

### 📄 文件处理

- **文档解析**: 支持上传 PDF、Word、Markdown 等文档
- **内容提取**: 智能提取文档关键信息
- **PDF 转 PPTX**: 将 PDF 文件转换为可编辑的 PPT
- **批量处理**: 支持多文件批量上传和处理

### 🌐 导出功能

- **HTML 导出**: 导出为可在浏览器中查看的 HTML 格式
- **PPTX 导出**: 导出为 PowerPoint 格式，支持编辑
- **PDF 导出**: 导出为 PDF 格式，便于分享
- **演讲稿导出**: 导出 Word 或 Markdown 格式的演讲稿

### 🔌 API 集成

- **OpenAI 兼容 API**: 完全兼容 OpenAI API 规范
- **RESTful API**: 标准的 REST API 接口
- **WebSocket 支持**: 实时通信和进度推送
- **完整文档**: 交互式 API 文档

---

## 🏗️ 技术架构

### 后端技术栈

- **Web 框架**: FastAPI - 高性能异步 Web 框架
- **AI 集成**: 
  - OpenAI GPT-3.5/4 - 内容生成
  - Google Gemini - 多模态 AI
  - LangChain - AI 应用框架
  - LangGraph - 工作流编排
- **数据库**: 
  - SQLAlchemy - ORM 框架
  - SQLite/PostgreSQL - 数据存储
  - Alembic - 数据库迁移
- **PPT 处理**:
  - python-pptx - PPT 生成和编辑
  - Apryse SDK - PDF 转 PPTX
  - Playwright - 网页截图和 PDF 生成
- **图片处理**:
  - PIL/Pillow - 图片处理
  - ONNX Runtime - AI 模型推理
- **其他工具**:
  - Pydantic - 数据验证
  - Jinja2 - 模板引擎
  - aiohttp - 异步 HTTP 客户端

### 前端技术栈

- **模板引擎**: Jinja2
- **样式**: CSS3 + 自定义主题系统
- **交互**: 原生 JavaScript + Fetch API
- **UI 组件**: 自定义组件库

### 项目结构

```
ai_slides/
├── src/ai_slides/              # 主应用代码
│   ├── api/                    # API 路由层
│   │   ├── openai_compat.py   # OpenAI 兼容 API
│   │   ├── ai_slides_api.py   # AI Slides 专用 API
│   │   ├── database_api.py    # 数据库管理 API
│   │   ├── config_api.py      # 配置管理 API
│   │   └── image_api.py       # 图片服务 API
│   ├── services/               # 业务逻辑层
│   │   ├── enhanced_ppt_service.py    # PPT 生成服务
│   │   ├── ai_service.py              # AI 服务
│   │   ├── file_processor.py          # 文件处理服务
│   │   ├── pdf_to_pptx_converter.py   # PDF 转换服务
│   │   ├── project_manager.py         # 项目管理服务
│   │   └── image/                     # 图片服务模块
│   ├── database/               # 数据访问层
│   │   ├── models.py          # 数据模型
│   │   ├── database.py        # 数据库连接
│   │   └── migrations.py      # 数据库迁移
│   ├── web/                    # Web 界面
│   │   ├── routes.py          # Web 路由
│   │   └── templates/         # HTML 模板
│   ├── core/                   # 核心配置
│   │   └── config.py          # 配置管理
│   ├── ai/                     # AI 提供者
│   │   └── providers/         # AI 提供者实现
│   ├── utils/                  # 工具函数
│   └── main.py                 # 应用入口
├── services/                   # 独立服务模块
├── docs/                       # 文档
├── temp/                       # 临时文件
├── template_examples/          # 模板示例
├── .env                        # 环境配置
├── pyproject.toml             # 项目配置
├── uv.toml                    # UV 配置
└── run.py                     # 启动脚本
```

---

## 🚀 快速开始

### 环境要求

- Python 3.9 或更高版本
- 推荐使用 [uv](https://docs.astral.sh/uv/) 包管理器

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/Jokerealm/ai_slides.git
cd ai_slides
```

#### 2. 安装依赖

**使用 uv（推荐）**:

```bash
# 安装 uv（如果还没有安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 同步依赖
uv sync
```

**使用 pip**:

```bash
pip install -e .
```

#### 3. 配置环境变量

编辑 `.env` 文件，配置必要的 API 密钥：

```env
# AI 提供者配置
DEFAULT_AI_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo

# 数据库配置
DATABASE_URL=sqlite:///./ai_slides.db

# 服务器配置
HOST=127.0.0.1
PORT=8000
DEBUG=false
RELOAD=false
```

#### 4. 启动服务器

**使用 uv**:

```bash
uv run python run.py
```

**或使用启动脚本**:

```bash
# Windows
start_server.bat

# Linux/Mac
./start_server.sh
```

#### 5. 访问应用

- **Web 界面**: http://localhost:8000/web
- **API 文档**: http://localhost:8000/docs
- **OpenAPI 规范**: http://localhost:8000/openapi.json

---

## 📚 使用指南

### 创建第一个 PPT

#### 方式 1: 通过 Web 界面

1. **访问首页**
   - 打开浏览器访问 http://localhost:8000/web

2. **选择场景**
   - 点击"创建新项目"
   - 选择适合的场景（商业汇报、教育培训、产品发布等）

3. **输入需求**
   - 输入 PPT 主题
   - 描述具体需求和目标受众
   - 设置页数范围

4. **生成大纲**
   - AI 自动生成 PPT 大纲
   - 可以编辑和调整大纲结构

5. **生成 PPT**
   - 确认大纲后，AI 自动生成完整 PPT
   - 实时查看生成进度

6. **编辑和导出**
   - 在线编辑幻灯片内容
   - 导出为 HTML 或 PPTX 格式

#### 方式 2: 通过 API

```python
import requests

# 创建项目
response = requests.post('http://localhost:8000/api/projects', json={
    'topic': '人工智能发展趋势',
    'scenario': 'business',
    'requirements': '面向技术团队，重点介绍 AI 在各行业的应用',
    'page_count_mode': 'range',
    'min_pages': 10,
    'max_pages': 15
})

project = response.json()
project_id = project['project_id']

# 查询项目状态
status = requests.get(f'http://localhost:8000/api/projects/{project_id}')
print(status.json())
```

### 上传文档生成 PPT

1. **准备文档**
   - 支持 PDF、Word、Markdown 等格式

2. **上传文件**
   - 在 Web 界面选择"从文件生成"
   - 上传文档文件

3. **AI 分析**
   - AI 自动提取文档关键信息
   - 生成结构化大纲

4. **生成 PPT**
   - 基于文档内容生成 PPT
   - 保留原文档的逻辑结构

### 使用模板

1. **浏览模板库**
   - 访问"模板管理"页面
   - 浏览内置模板和自定义模板

2. **应用模板**
   - 在创建项目时选择模板
   - 或在编辑时切换模板

3. **自定义模板**
   - 创建新模板
   - 设置样式、布局和配色
   - 保存为可复用模板

---

## 🔧 核心功能

### 1. 项目管理

#### 项目列表
- 查看所有项目
- 按状态筛选（草稿、进行中、已完成、已归档）
- 快速操作（编辑、预览、导出、删除）

#### 项目详情
- 查看项目完整信息
- 查看生成进度和 TODO 看板
- 管理项目版本
- 归档或删除项目

#### TODO 看板
- 可视化任务进度
- 实时更新任务状态
- 查看每个阶段的详细信息

### 2. PPT 编辑

#### 在线编辑器
- 实时预览
- 拖拽排序
- 富文本编辑
- 图片上传和管理

#### 幻灯片操作
- 添加/删除幻灯片
- 复制/移动幻灯片
- 批量编辑
- AI 优化内容

#### 样式设置
- 主题切换
- 字体设置
- 配色方案
- 布局调整

### 3. 导出功能

#### HTML 导出
- 导出为 ZIP 压缩包
- 包含索引页和所有幻灯片
- 支持浏览器直接查看
- 适合在线分享

#### PPTX 导出
- 导出为 PowerPoint 格式
- 保留所有样式和布局
- 支持在 Office 中编辑
- 适合正式演示

#### PDF 导出
- 导出为 PDF 格式
- 高质量渲染
- 适合打印和存档

#### 演讲稿导出
- 导出为 Word 或 Markdown
- 包含每页的演讲要点
- 便于演讲准备

### 4. 图片服务

#### 本地图库
- 上传和管理本地图片
- 图片分类和标签
- 快速搜索和筛选

#### 网络搜索
- 集成 Pixabay API
- 集成 Unsplash API
- 自动版权筛选
- 高质量图片源

#### AI 生成
- DALL-E 图片生成
- Pollinations AI 生成
- 自定义提示词
- 批量生成

### 5. 文件处理

#### 文档上传
- 支持多文件上传
- 自动格式识别
- 进度显示

#### 内容提取
- 智能提取关键信息
- 保留文档结构
- 生成摘要

#### PDF 转换
- PDF 转 PPTX
- 保留原始布局
- 支持批量转换

---

## 🔌 API 文档

### OpenAI 兼容 API

AI Slides 提供完全兼容 OpenAI API 的接口，可以无缝集成到现有工具中。

#### Chat Completions

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "user", "content": "生成一个关于人工智能的 PPT 大纲"}
    ]
  }'
```

#### Models

```bash
curl http://localhost:8000/v1/models
```

### AI Slides 专用 API

#### 创建项目

```bash
POST /api/projects
Content-Type: application/json

{
  "topic": "人工智能发展趋势",
  "scenario": "business",
  "requirements": "面向技术团队",
  "page_count_mode": "range",
  "min_pages": 10,
  "max_pages": 15
}
```

#### 获取项目列表

```bash
GET /api/projects?status=completed&page=1&page_size=10
```

#### 获取项目详情

```bash
GET /api/projects/{project_id}
```

#### 导出项目

```bash
# HTML 导出
GET /api/projects/{project_id}/export/html

# PPTX 导出
GET /api/projects/{project_id}/export/pptx

# PDF 导出
GET /api/projects/{project_id}/export/pdf
```

#### 上传文件生成 PPT

```bash
POST /api/projects/from-file
Content-Type: multipart/form-data

file: <file>
topic: "文档主题"
scenario: "business"
```

### 完整 API 文档

访问 http://localhost:8000/docs 查看交互式 API 文档。

---

## ⚙️ 配置说明

### 环境变量

#### AI 提供者配置

```env
# 默认 AI 提供者（openai 或 google）
DEFAULT_AI_PROVIDER=openai

# OpenAI 配置
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo

# Google Gemini 配置
GOOGLE_API_KEY=your_google_api_key
GOOGLE_MODEL=gemini-1.5-flash
```

#### 数据库配置

```env
# SQLite（默认）
DATABASE_URL=sqlite:///./ai_slides.db

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/ai_slides

# MySQL
DATABASE_URL=mysql://user:password@localhost/ai_slides
```

#### 服务器配置

```env
HOST=127.0.0.1
PORT=8000
DEBUG=false
RELOAD=false
LOG_LEVEL=INFO
```

#### 图片服务配置

```env
# 启用图片服务
ENABLE_IMAGE_SERVICE=true
ENABLE_LOCAL_IMAGES=true
ENABLE_NETWORK_SEARCH=true
ENABLE_AI_GENERATION=true

# 图片源 API 密钥
PIXABAY_API_KEY=your_pixabay_key
UNSPLASH_ACCESS_KEY=your_unsplash_key
POLLINATIONS_API_TOKEN=your_pollinations_token

# 默认图片提供者
DEFAULT_AI_IMAGE_PROVIDER=pollinations
DEFAULT_NETWORK_SEARCH_PROVIDER=pixabay
```

#### PDF 转换配置

```env
# Apryse SDK 许可证
APRYSE_LICENSE_KEY=your_apryse_license_key
```

### 高级配置

#### AI 生成参数

```env
MAX_TOKENS=10086
TEMPERATURE=0.7
TOP_P=1.0
```

#### 文件上传限制

```env
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIR=uploads
```

#### 缓存设置

```env
CACHE_TTL=3600  # 1小时
```

---

## 👨‍💻 开发指南

### 开发环境设置

#### 1. 安装开发依赖

```bash
uv sync --extra dev
```

#### 2. 启用开发模式

```env
DEBUG=true
RELOAD=true
LOG_LEVEL=DEBUG
```

#### 3. 运行开发服务器

```bash
uv run python run.py
```

### 代码规范

#### 格式化代码

```bash
# 使用 black 格式化
black src/

# 使用 isort 排序导入
isort src/
```

#### 代码检查

```bash
# 使用 flake8 检查
flake8 src/

# 使用 mypy 类型检查
mypy src/
```

### 测试

#### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行特定测试
uv run pytest tests/test_api.py

# 生成覆盖率报告
uv run pytest --cov=src --cov-report=html
```

#### 测试 API

```bash
# 测试服务器连接
uv run python test_server.py

# 测试 HTML 导出
uv run python test_html_export.py
```

### 数据库迁移

#### 创建迁移

```bash
alembic revision --autogenerate -m "描述"
```

#### 应用迁移

```bash
alembic upgrade head
```

#### 回滚迁移

```bash
alembic downgrade -1
```

### 添加新功能

#### 1. 创建 API 路由

```python
# src/ai_slides/api/my_api.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/my-endpoint")
async def my_endpoint():
    return {"message": "Hello"}
```

#### 2. 注册路由

```python
# src/ai_slides/main.py
from .api.my_api import router as my_router

app.include_router(my_router, prefix="/api", tags=["My API"])
```

#### 3. 添加服务逻辑

```python
# src/ai_slides/services/my_service.py
class MyService:
    async def do_something(self):
        pass
```

#### 4. 添加测试

```python
# tests/test_my_api.py
def test_my_endpoint():
    response = client.get("/api/my-endpoint")
    assert response.status_code == 200
```

---

## ❓ 常见问题

### Q1: 如何更换 AI 提供者？

修改 `.env` 文件中的 `DEFAULT_AI_PROVIDER`:

```env
# 使用 OpenAI
DEFAULT_AI_PROVIDER=openai

# 使用 Google Gemini
DEFAULT_AI_PROVIDER=google
```

### Q2: 如何使用自己的 API 密钥？

在 `.env` 文件中配置相应的 API 密钥：

```env
OPENAI_API_KEY=sk-your-key-here
GOOGLE_API_KEY=your-google-key-here
```

### Q3: 数据存储在哪里？

默认使用 SQLite 数据库，文件位于项目根目录的 `ai_slides.db`。

可以通过修改 `DATABASE_URL` 使用其他数据库。

### Q4: 如何保留旧数据？

如果从旧版本升级，将旧的数据库文件重命名为 `ai_slides.db` 即可。

### Q5: 端口被占用怎么办？

修改 `.env` 文件中的 `PORT`:

```env
PORT=8001
```

### Q6: 如何启用图片生成功能？

在 `.env` 文件中配置：

```env
ENABLE_IMAGE_SERVICE=true
ENABLE_AI_GENERATION=true
DEFAULT_AI_IMAGE_PROVIDER=pollinations
```

### Q7: 导出功能不工作？

确保已安装 Playwright 浏览器：

```bash
playwright install chromium
```

### Q8: 如何提高生成速度？

1. 使用更快的 AI 模型（如 gpt-3.5-turbo）
2. 减少页数范围
3. 禁用图片生成功能
4. 使用本地 AI 模型

---

## 📝 更新日志

### v0.1.6 (2025-12-19)

#### 新增功能
- ✨ 项目列表页面添加导出功能
- ✨ 项目详情页面添加导出功能
- ✨ 支持 HTML 和 PPTX 双格式导出
- ✨ 添加导出菜单和加载提示

#### 修复问题
- 🐛 修复 PPTX 导出 405 错误
- 🐛 修复 HTML 导出功能
- 🐛 修复导出按钮无响应问题
- 🐛 修复路由重复定义问题

#### 优化改进
- ⚡ 优化导出流程和用户体验
- ⚡ 改进错误处理和提示
- 📝 完善文档和使用说明
- 🎨 优化 UI 交互和动画效果

### v0.1.5

#### 新增功能
- ✨ 添加 PDF 转 PPTX 功能
- ✨ 支持文件上传生成 PPT
- ✨ 添加演讲稿导出功能

#### 修复问题
- 🐛 修复模板加载问题
- 🐛 修复数据库迁移问题

### v0.1.0

- 🎉 首次发布
- ✨ 基础 PPT 生成功能
- ✨ Web 界面
- ✨ OpenAI 兼容 API

---

## 📄 许可证

本项目采用 [Apache-2.0](LICENSE) 许可证。

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

### 贡献方式

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 报告问题

如果发现 bug 或有功能建议，请在 [Issues](https://github.com/Jokerealm/ai_slides/issues) 页面提交。

---

## 📞 联系方式

- **GitHub**: https://github.com/Jokerealm/ai_slides
- **Issues**: https://github.com/Jokerealm/ai_slides/issues
- **Email**: contact@ai-slides.com

---

## 🙏 致谢

感谢以下开源项目：

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的 Web 框架
- [LangChain](https://www.langchain.com/) - AI 应用开发框架
- [python-pptx](https://python-pptx.readthedocs.io/) - PPT 处理库
- [Playwright](https://playwright.dev/) - 浏览器自动化工具

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个 Star！⭐**

Made with ❤️ by AI Slides Team

</div>
