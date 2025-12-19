# Requirements Document

## Introduction

本需求文档旨在改进 AI Slides 项目的 PPT 导出功能。当前系统使用 python-pptx 库导出 PPT，但导出的文件只包含纯文本内容，缺少排版、样式和背景。用户需要导出包含完整设计元素的专业 PPT 文件。

## Glossary

- **AI Slides System**: AI 驱动的 PPT 生成平台系统
- **python-pptx**: Python 库，用于创建和修改 PowerPoint 文件，但功能有限
- **Apryse SDK**: 专业的文档处理 SDK（原 PDFTron），支持高级 PPT 操作和转换
- **HTML Slides**: 系统中存储的幻灯片 HTML 内容，包含完整的样式和布局
- **Master Template**: PPT 母版模板，定义幻灯片的整体设计风格
- **Slide Layout**: 幻灯片布局，定义内容在幻灯片上的位置和样式

## Requirements

### Requirement 1

**User Story:** 作为用户，我想导出包含完整设计的 PPT 文件，以便我可以直接使用而无需重新设计。

#### Acceptance Criteria

1. WHEN 用户点击导出 PPT 按钮 THEN AI Slides System SHALL 生成包含背景、样式和排版的 PPTX 文件
2. WHEN 导出 PPT THEN AI Slides System SHALL 保留 HTML Slides 中定义的颜色方案和字体样式
3. WHEN 导出 PPT THEN AI Slides System SHALL 保留幻灯片的背景图片或背景色
4. WHEN 导出 PPT THEN AI Slides System SHALL 保留文本的格式（粗体、斜体、颜色、大小）
5. WHEN 导出 PPT THEN AI Slides System SHALL 保留图片的位置和大小

### Requirement 2

**User Story:** 作为开发者，我想使用 Apryse SDK 来增强 PPT 导出功能，以便支持更复杂的文档操作。

#### Acceptance Criteria

1. WHEN AI Slides System 初始化 THEN THE System SHALL 检查 Apryse License Key 是否已配置
2. WHEN Apryse License Key 已配置 THEN THE System SHALL 使用 Apryse SDK 进行 PPT 导出
3. WHEN Apryse License Key 未配置 THEN THE System SHALL 降级使用 python-pptx 进行基本导出
4. WHEN 使用 Apryse SDK 导出失败 THEN THE System SHALL 记录错误日志并尝试降级到 python-pptx

### Requirement 3

**User Story:** 作为用户，我想导出的 PPT 能够应用项目的 Master Template，以便保持一致的设计风格。

#### Acceptance Criteria

1. WHEN 项目有关联的 Master Template THEN AI Slides System SHALL 在导出时应用该模板
2. WHEN 应用 Master Template THEN THE System SHALL 使用模板定义的 Slide Layout
3. WHEN 应用 Master Template THEN THE System SHALL 使用模板定义的配色方案
4. WHEN 项目没有关联的 Master Template THEN THE System SHALL 使用默认的简洁设计

### Requirement 4

**User Story:** 作为用户，我想导出过程能够处理各种内容类型，以便所有幻灯片元素都能正确显示。

#### Acceptance Criteria

1. WHEN HTML Slides 包含文本内容 THEN AI Slides System SHALL 正确提取并格式化文本
2. WHEN HTML Slides 包含图片 THEN THE System SHALL 提取并嵌入图片到 PPTX
3. WHEN HTML Slides 包含列表 THEN THE System SHALL 转换为 PPT 的项目符号列表
4. WHEN HTML Slides 包含表格 THEN THE System SHALL 转换为 PPT 表格
5. WHEN HTML Slides 包含特殊字符 THEN THE System SHALL 正确处理编码

### Requirement 5

**User Story:** 作为系统管理员，我想配置 Apryse SDK 的许可证，以便启用高级导出功能。

#### Acceptance Criteria

1. WHEN 管理员访问 AI 配置页面 THEN AI Slides System SHALL 显示 Apryse License Key 输入框
2. WHEN 管理员输入 License Key THEN THE System SHALL 验证密钥格式
3. WHEN License Key 有效 THEN THE System SHALL 保存到配置文件
4. WHEN License Key 无效 THEN THE System SHALL 显示错误提示
5. WHEN License Key 已保存 THEN THE System SHALL 在重启后自动加载

### Requirement 6

**User Story:** 作为用户，我想导出过程有清晰的进度反馈，以便了解导出状态。

#### Acceptance Criteria

1. WHEN 用户开始导出 THEN AI Slides System SHALL 显示进度提示
2. WHEN 导出过程中 THEN THE System SHALL 更新进度百分比
3. WHEN 导出成功 THEN THE System SHALL 自动下载文件并显示成功消息
4. WHEN 导出失败 THEN THE System SHALL 显示具体的错误信息
5. WHEN 导出超时 THEN THE System SHALL 提示用户重试
