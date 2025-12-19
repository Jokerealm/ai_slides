# Implementation Plan

- [ ] 1. 设置项目结构和核心接口
  - 创建 `src/ai_slides/services/pptx_export/` 目录结构
  - 定义数据模型类（SlideContent, Background, TextFormat, ImageInfo, MasterTemplate）
  - 设置测试框架（pytest, hypothesis）
  - _Requirements: 1.1, 2.1_

- [ ] 2. 实现 Apryse SDK 封装器
  - [ ] 2.1 创建 ApryseSDKWrapper 类
    - 实现 `__init__` 和 `initialize()` 方法
    - 实现 `validate_license()` 方法
    - 添加错误处理和日志记录
    - _Requirements: 2.1, 2.2_

  - [ ]* 2.2 编写 Apryse SDK 初始化的属性测试
    - **Property 3: 引擎选择正确性**
    - **Validates: Requirements 2.2, 2.3**

  - [ ] 2.3 实现 HTML 到 PPTX 转换方法
    - 实现 `html_to_pptx()` 方法
    - 处理样式转换
    - 处理图片嵌入
    - _Requirements: 1.1, 1.2, 1.5_

  - [ ]* 2.4 编写样式保留的属性测试
    - **Property 1: 完整样式保留**
    - **Validates: Requirements 1.2, 1.3, 1.4**

  - [ ] 2.5 实现模板应用方法
    - 实现 `apply_template_to_pptx()` 方法
    - 支持布局和配色方案应用
    - _Requirements: 3.1, 3.2, 3.3_

  - [ ]* 2.6 编写模板应用的属性测试
    - **Property 5: 模板应用完整性**
    - **Validates: Requirements 3.1, 3.2, 3.3**

- [ ] 3. 实现 HTML 样式解析器
  - [ ] 3.1 创建 HTMLStyleParser 类
    - 实现 `parse_slide_html()` 方法
    - 实现 `extract_styles()` 方法
    - 实现 `extract_background()` 方法
    - _Requirements: 1.2, 1.3, 4.1_

  - [ ] 3.2 实现文本格式提取
    - 实现 `extract_text_formats()` 方法
    - 支持粗体、斜体、颜色、大小提取
    - _Requirements: 1.4, 4.1_

  - [ ] 3.3 实现图片提取
    - 实现 `extract_images()` 方法
    - 支持 base64 和 URL 图片
    - 提取位置和大小信息
    - _Requirements: 1.5, 4.2_

  - [ ]* 3.4 编写图片布局保留的属性测试
    - **Property 2: 图片布局保留**
    - **Validates: Requirements 1.5**

  - [ ] 3.5 实现列表和表格提取
    - 提取 HTML 列表结构
    - 提取 HTML 表格结构
    - _Requirements: 4.3, 4.4_

  - [ ]* 3.6 编写内容转换的属性测试
    - **Property 7: 内容类型转换**
    - **Validates: Requirements 4.1, 4.2, 4.3, 4.4**

- [ ] 4. 实现模板管理器
  - [ ] 4.1 创建 TemplateManager 类
    - 实现 `load_template()` 方法
    - 实现 `get_default_template()` 方法
    - 添加模板缓存机制
    - _Requirements: 3.1, 3.4_

  - [ ]* 4.2 编写默认模板应用的属性测试
    - **Property 6: 默认模板应用**
    - **Validates: Requirements 3.4**

  - [ ] 4.3 实现模板样式应用
    - 实现 `apply_template_styles()` 方法
    - 支持不同幻灯片类型的布局
    - _Requirements: 3.2, 3.3_

  - [ ] 4.4 创建默认模板文件
    - 设计简洁的默认 PPTX 模板
    - 定义默认配色方案和布局
    - _Requirements: 3.4_

- [ ] 5. 实现 PPTXExportManager
  - [ ] 5.1 创建 PPTXExportManager 类
    - 实现 `__init__` 和 `_initialize_apryse()` 方法
    - 实现 `check_apryse_availability()` 方法
    - _Requirements: 2.1, 2.2_

  - [ ] 5.2 实现主导出方法
    - 实现 `export_project()` 方法
    - 协调 HTML 解析、模板加载、PPTX 生成
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

  - [ ] 5.3 实现 Apryse 导出路径
    - 实现 `_export_with_apryse()` 方法
    - 集成 ApryseSDKWrapper
    - 集成 HTMLStyleParser
    - _Requirements: 2.2, 1.1_

  - [ ] 5.4 实现 python-pptx 降级路径
    - 实现 `_export_with_python_pptx()` 方法
    - 保留现有的 python-pptx 逻辑
    - 添加基本的样式支持
    - _Requirements: 2.3_

  - [ ] 5.5 实现错误处理和降级逻辑
    - 添加 try-catch 块
    - 实现 Apryse 失败时的降级
    - 添加详细的错误日志
    - _Requirements: 2.4_

  - [ ]* 5.6 编写错误降级的属性测试
    - **Property 4: 错误降级处理**
    - **Validates: Requirements 2.4**

- [ ] 6. 更新配置管理
  - [ ] 6.1 更新 AIConfig 类
    - 确保 `apryse_license_key` 字段存在
    - 添加 license key 验证方法
    - _Requirements: 5.2, 5.3_

  - [ ] 6.2 更新配置服务
    - 更新 `config_service.py` 中的配置定义
    - 确保 license key 可以保存和加载
    - _Requirements: 5.3, 5.5_

  - [ ]* 6.3 编写 License Key 持久化的属性测试
    - **Property 8: License Key 持久化 Round-trip**
    - **Validates: Requirements 5.5**

  - [ ] 6.4 更新 AI 配置页面
    - 确保 Apryse License Key 输入框正常工作
    - 添加 license key 格式验证
    - 添加保存成功/失败的提示
    - _Requirements: 5.1, 5.2, 5.4_

- [ ] 7. 更新 Web 路由
  - [ ] 7.1 更新 `/api/projects/{id}/export/pptx` 路由
    - 替换现有的 python-pptx 实现
    - 集成 PPTXExportManager
    - 添加进度反馈支持
    - _Requirements: 1.1, 6.1, 6.2_

  - [ ] 7.2 添加错误处理
    - 处理各种导出错误
    - 返回清晰的错误消息
    - _Requirements: 6.4, 6.5_

  - [ ] 7.3 更新前端导出逻辑
    - 更新 `project_slides_editor.html` 中的导出函数
    - 添加进度显示
    - 改进错误提示
    - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [ ] 8. Checkpoint - 确保所有测试通过
  - 确保所有测试通过，如有问题请询问用户

- [ ] 9. 集成测试和优化
  - [ ]* 9.1 编写端到端集成测试
    - 测试完整的导出流程
    - 测试 Apryse 和 python-pptx 两种路径
    - 测试模板应用
    - _Requirements: 1.1, 2.2, 2.3, 3.1_

  - [ ] 9.2 性能优化
    - 添加模板缓存
    - 优化 HTML 解析性能
    - 考虑并行处理多个幻灯片
    - _Requirements: 1.1_

  - [ ] 9.3 添加日志和监控
    - 添加详细的 INFO 日志
    - 添加性能指标记录
    - _Requirements: 2.4, 6.2_

- [ ] 10. 文档和部署准备
  - [ ] 10.1 更新 README
    - 添加 Apryse SDK 配置说明
    - 添加 license key 获取指南
    - 更新导出功能说明
    - _Requirements: 5.1_

  - [ ] 10.2 创建配置示例
    - 创建 `.env.example` 更新
    - 添加 Apryse license key 配置示例
    - _Requirements: 5.1, 5.5_

  - [ ] 10.3 准备部署检查清单
    - 验证所有依赖已安装
    - 验证配置文件正确
    - 验证测试全部通过
    - _Requirements: 2.1_

- [ ] 11. Final Checkpoint - 确保所有测试通过
  - 确保所有测试通过，如有问题请询问用户
