# Design Document: PPT Export Enhancement

## Overview

本设计文档描述了如何增强 AI Slides 系统的 PPT 导出功能，从当前仅支持基本文本导出的 python-pptx 实现，升级为支持完整设计元素（背景、样式、排版）的 Apryse SDK 实现，同时保留 python-pptx 作为降级方案。

### Current State

- 使用 python-pptx 库进行 PPT 导出
- 只能导出纯文本内容和简单布局
- 无法保留 HTML slides 中的样式、背景和复杂排版
- 已安装 apryse-sdk 但未使用

### Target State

- 使用 Apryse SDK 作为主要导出引擎
- 支持完整的设计元素导出（背景、样式、排版）
- 支持 Master Template 应用
- 保留 python-pptx 作为降级方案
- 提供清晰的配置和错误处理

## Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Layer (routes.py)                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  /api/projects/{id}/export/pptx                        │ │
│  └────────────────────────────────────────────────────────┘ │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Enhanced PPT Export Service                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  PPTXExportManager                                     │ │
│  │  - check_apryse_availability()                         │ │
│  │  - export_with_apryse()                                │ │
│  │  - export_with_python_pptx()                           │ │
│  │  - apply_master_template()                             │ │
│  └────────────────────────────────────────────────────────┘ │
└───────────┬─────────────────────────────┬───────────────────┘
            │                             │
            ▼                             ▼
┌───────────────────────┐    ┌──────────────────────────────┐
│   Apryse SDK Wrapper  │    │  Python-PPTX Wrapper         │
│  - initialize()       │    │  - create_presentation()     │
│  - html_to_pptx()     │    │  - add_slide()               │
│  - apply_template()   │    │  - format_text()             │
└───────────────────────┘    └──────────────────────────────┘
            │                             │
            ▼                             ▼
┌───────────────────────┐    ┌──────────────────────────────┐
│   HTML Parser         │    │  Template Manager            │
│  - parse_styles()     │    │  - load_template()           │
│  - extract_content()  │    │  - get_layout()              │
│  - extract_images()   │    │  - get_color_scheme()        │
└───────────────────────┘    └──────────────────────────────┘
```

### Data Flow

1. **Export Request**: 用户点击导出按钮 → Web Layer 接收请求
2. **Configuration Check**: PPTXExportManager 检查 Apryse License Key
3. **Engine Selection**: 
   - 如果 License Key 有效 → 使用 Apryse SDK
   - 如果 License Key 无效或未配置 → 使用 python-pptx
4. **Template Loading**: 如果项目有 Master Template，加载模板
5. **Content Processing**: 解析 HTML slides，提取内容、样式、图片
6. **PPTX Generation**: 使用选定的引擎生成 PPTX 文件
7. **Response**: 返回 PPTX 文件流给客户端

## Components and Interfaces

### 1. PPTXExportManager

主要的导出管理器，负责协调整个导出流程。

```python
class PPTXExportManager:
    """Manages PPTX export with Apryse SDK and python-pptx fallback"""
    
    def __init__(self, config: AIConfig):
        self.config = config
        self.apryse_wrapper = None
        self.python_pptx_wrapper = PythonPPTXWrapper()
        self._initialize_apryse()
    
    def _initialize_apryse(self) -> bool:
        """Initialize Apryse SDK if license key is available"""
        
    async def export_project(
        self, 
        project: PPTProject,
        use_template: bool = True
    ) -> BytesIO:
        """Export project to PPTX with full styling"""
        
    def check_apryse_availability(self) -> bool:
        """Check if Apryse SDK is available and licensed"""
        
    async def _export_with_apryse(
        self, 
        project: PPTProject,
        template: Optional[MasterTemplate]
    ) -> BytesIO:
        """Export using Apryse SDK"""
        
    async def _export_with_python_pptx(
        self, 
        project: PPTProject,
        template: Optional[MasterTemplate]
    ) -> BytesIO:
        """Fallback export using python-pptx"""
```

### 2. ApryseSDKWrapper

封装 Apryse SDK 的功能，提供简化的接口。

```python
class ApryseSDKWrapper:
    """Wrapper for Apryse SDK functionality"""
    
    def __init__(self, license_key: str):
        self.license_key = license_key
        self.initialized = False
    
    def initialize(self) -> bool:
        """Initialize Apryse SDK with license key"""
        
    async def html_to_pptx(
        self,
        html_content: str,
        styles: Dict[str, Any],
        output_stream: BytesIO
    ) -> bool:
        """Convert HTML content to PPTX with styles"""
        
    async def apply_template_to_pptx(
        self,
        pptx_stream: BytesIO,
        template_path: str
    ) -> BytesIO:
        """Apply master template to PPTX"""
        
    def validate_license(self) -> bool:
        """Validate Apryse license key"""
```

### 3. HTMLStyleParser

解析 HTML slides 中的样式信息。

```python
class HTMLStyleParser:
    """Parse HTML content and extract styling information"""
    
    def parse_slide_html(self, html: str) -> SlideContent:
        """Parse HTML and extract structured content"""
        
    def extract_styles(self, html: str) -> Dict[str, Any]:
        """Extract CSS styles from HTML"""
        
    def extract_background(self, html: str) -> Optional[Background]:
        """Extract background color or image"""
        
    def extract_text_formats(self, element) -> TextFormat:
        """Extract text formatting (bold, italic, color, size)"""
        
    def extract_images(self, html: str) -> List[ImageInfo]:
        """Extract images with position and size"""
```

### 4. TemplateManager

管理 Master Template 的加载和应用。

```python
class TemplateManager:
    """Manage master templates for PPTX export"""
    
    def load_template(self, template_id: str) -> Optional[MasterTemplate]:
        """Load master template by ID"""
        
    def get_default_template(self) -> MasterTemplate:
        """Get default template"""
        
    def apply_template_styles(
        self,
        slide: Any,
        template: MasterTemplate,
        slide_type: str
    ) -> None:
        """Apply template styles to a slide"""
```

## Data Models

### SlideContent

```python
@dataclass
class SlideContent:
    """Structured content extracted from HTML slide"""
    title: str
    subtitle: Optional[str]
    content_points: List[str]
    images: List[ImageInfo]
    background: Optional[Background]
    styles: Dict[str, Any]
    layout_type: str  # 'title', 'content', 'two-column', etc.
```

### Background

```python
@dataclass
class Background:
    """Background information for a slide"""
    type: str  # 'color', 'gradient', 'image'
    color: Optional[str]  # Hex color
    gradient: Optional[GradientInfo]
    image_url: Optional[str]
    image_data: Optional[bytes]
```

### TextFormat

```python
@dataclass
class TextFormat:
    """Text formatting information"""
    font_family: str
    font_size: int
    color: str
    bold: bool
    italic: bool
    underline: bool
    alignment: str  # 'left', 'center', 'right'
```

### ImageInfo

```python
@dataclass
class ImageInfo:
    """Image information with position and size"""
    src: str  # URL or base64
    data: Optional[bytes]
    left: float  # Position in inches
    top: float
    width: float
    height: float
    alt_text: Optional[str]
```

### MasterTemplate

```python
@dataclass
class MasterTemplate:
    """Master template definition"""
    template_id: str
    name: str
    file_path: Optional[str]  # Path to .pptx template file
    color_scheme: Dict[str, str]
    font_scheme: Dict[str, str]
    layouts: Dict[str, LayoutInfo]
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

在定义具体的属性之前，我们需要识别和消除冗余：

1. **样式保留属性的整合**: 属性 1.2（颜色和字体）、1.3（背景）、1.4（文本格式）都是关于样式保留的，可以整合为一个综合的"样式保留"属性。

2. **引擎选择逻辑的整合**: 属性 2.2（使用 Apryse）和 2.3（使用 python-pptx）是互斥的条件分支，可以整合为一个"引擎选择"属性。

3. **模板应用属性的整合**: 属性 3.2（布局）和 3.3（配色）都是模板应用的一部分，可以整合到属性 3.1 中。

4. **内容转换属性的整合**: 属性 4.1-4.4 都是关于内容类型转换的，可以整合为一个综合的"内容转换"属性。

经过反思，我们将保留以下核心属性：

### Property 1: 完整样式保留

*For any* HTML slide with styling (colors, fonts, backgrounds, text formats), exporting to PPTX should preserve all visual styling elements in the output file.

**Validates: Requirements 1.2, 1.3, 1.4**

### Property 2: 图片布局保留

*For any* HTML slide containing images, exporting to PPTX should preserve the position and size of all images.

**Validates: Requirements 1.5**

### Property 3: 引擎选择正确性

*For any* system configuration state, the export manager should use Apryse SDK when license key is valid, and fall back to python-pptx when license key is invalid or unavailable.

**Validates: Requirements 2.2, 2.3**

### Property 4: 错误降级处理

*For any* export attempt where Apryse SDK fails, the system should log the error and successfully fall back to python-pptx export.

**Validates: Requirements 2.4**

### Property 5: 模板应用完整性

*For any* project with an associated master template, exporting should apply the template's layouts and color scheme to all slides.

**Validates: Requirements 3.1, 3.2, 3.3**

### Property 6: 默认模板应用

*For any* project without an associated master template, exporting should apply a default clean design.

**Validates: Requirements 3.4**

### Property 7: 内容类型转换

*For any* HTML slide containing text, images, lists, or tables, the export should correctly convert each content type to its PPTX equivalent.

**Validates: Requirements 4.1, 4.2, 4.3, 4.4**

### Property 8: License Key 持久化 Round-trip

*For any* valid license key, saving it to configuration and restarting the system should result in the same license key being loaded.

**Validates: Requirements 5.5**

## Error Handling

### Error Categories

1. **Configuration Errors**
   - Missing or invalid Apryse license key
   - Corrupted configuration file
   - **Handling**: Log warning, fall back to python-pptx

2. **Apryse SDK Errors**
   - SDK initialization failure
   - License validation failure
   - Conversion errors
   - **Handling**: Log error with details, attempt fallback to python-pptx

3. **Content Processing Errors**
   - Invalid HTML structure
   - Unsupported content types
   - Image loading failures
   - **Handling**: Log warning, skip problematic content, continue with rest

4. **Template Errors**
   - Template file not found
   - Corrupted template file
   - **Handling**: Log warning, use default template

5. **Export Errors**
   - Insufficient memory
   - File system errors
   - **Handling**: Return HTTP 500 with descriptive error message

### Error Response Format

```python
{
    "success": false,
    "error": {
        "code": "EXPORT_FAILED",
        "message": "Failed to export PPTX",
        "details": "Apryse SDK initialization failed, fallback also failed",
        "fallback_used": true
    }
}
```

### Logging Strategy

- **INFO**: Successful exports, engine selection decisions
- **WARNING**: Fallback usage, skipped content, template issues
- **ERROR**: Export failures, SDK errors, configuration errors
- **DEBUG**: Detailed processing steps, style extraction details

## Testing Strategy

### Unit Testing

Unit tests will verify specific components and edge cases:

1. **Configuration Tests**
   - Test license key validation with valid/invalid formats
   - Test configuration loading and saving
   - Test environment variable override

2. **HTML Parser Tests**
   - Test style extraction from various HTML structures
   - Test background extraction (color, gradient, image)
   - Test image extraction with base64 and URLs
   - Test text format extraction

3. **Engine Selection Tests**
   - Test Apryse availability check
   - Test fallback logic when Apryse unavailable
   - Test error handling during export

4. **Template Manager Tests**
   - Test template loading
   - Test default template fallback
   - Test template style application

### Property-Based Testing

Property-based tests will verify universal properties across many inputs using **Hypothesis** (Python's property-based testing library). Each test will run a minimum of 100 iterations.

1. **Property Test 1: Style Preservation**
   - **Feature: pptx-export-enhancement, Property 1: 完整样式保留**
   - Generate random HTML slides with various styles
   - Export to PPTX
   - Parse PPTX and verify styles match

2. **Property Test 2: Image Layout Preservation**
   - **Feature: pptx-export-enhancement, Property 2: 图片布局保留**
   - Generate random HTML slides with images at various positions
   - Export to PPTX
   - Verify image positions and sizes match

3. **Property Test 3: Engine Selection**
   - **Feature: pptx-export-enhancement, Property 3: 引擎选择正确性**
   - Generate random configuration states (with/without license key)
   - Verify correct engine is selected

4. **Property Test 4: Error Fallback**
   - **Feature: pptx-export-enhancement, Property 4: 错误降级处理**
   - Simulate Apryse SDK failures
   - Verify fallback to python-pptx occurs and logs are created

5. **Property Test 5: Template Application**
   - **Feature: pptx-export-enhancement, Property 5: 模板应用完整性**
   - Generate random projects with templates
   - Verify template layouts and colors are applied

6. **Property Test 6: Default Template**
   - **Feature: pptx-export-enhancement, Property 6: 默认模板应用**
   - Generate random projects without templates
   - Verify default design is applied

7. **Property Test 7: Content Conversion**
   - **Feature: pptx-export-enhancement, Property 7: 内容类型转换**
   - Generate random HTML with various content types
   - Verify all content types are correctly converted

8. **Property Test 8: License Key Round-trip**
   - **Feature: pptx-export-enhancement, Property 8: License Key 持久化 Round-trip**
   - Generate random valid license keys
   - Save, restart (simulate), and load
   - Verify loaded key matches saved key

### Integration Testing

Integration tests will verify the complete export workflow:

1. **End-to-End Export Test**
   - Create a test project with various slide types
   - Export using both Apryse and python-pptx
   - Verify PPTX files are valid and openable

2. **Template Integration Test**
   - Create project with master template
   - Export and verify template is applied

3. **Fallback Integration Test**
   - Disable Apryse (invalid license)
   - Export and verify python-pptx is used
   - Verify export still succeeds

### Test Configuration

- **Minimum iterations for property tests**: 100
- **Test framework**: pytest + pytest-asyncio
- **Property testing library**: Hypothesis
- **Mocking library**: unittest.mock
- **Coverage target**: 80% for new code

## Implementation Notes

### Apryse SDK Integration

1. **License Initialization**
   ```python
   from apryse import PDFNet
   PDFNet.Initialize(license_key)
   ```

2. **HTML to PPTX Conversion**
   - Apryse SDK supports HTML to PDF conversion natively
   - For PPTX, we may need to:
     - Convert HTML to PDF first
     - Then convert PDF to PPTX
     - Or use Apryse's Office conversion features

3. **Alternative Approach**: If direct HTML to PPTX is not supported:
   - Use Apryse to manipulate existing PPTX files
   - Create PPTX with python-pptx
   - Use Apryse to enhance with advanced features

### Performance Considerations

1. **Caching**: Cache parsed templates to avoid repeated loading
2. **Async Processing**: Use async/await for I/O operations
3. **Memory Management**: Stream large PPTX files instead of loading entirely in memory
4. **Parallel Processing**: Consider parallel slide processing for large presentations

### Security Considerations

1. **License Key Storage**: Store license key encrypted in configuration
2. **Input Validation**: Validate HTML content to prevent injection attacks
3. **File Size Limits**: Enforce maximum PPTX file size
4. **Resource Limits**: Limit memory and CPU usage during export

## Migration Strategy

### Phase 1: Infrastructure Setup
- Add ApryseSDKWrapper class
- Add PPTXExportManager class
- Update configuration to support license key

### Phase 2: Core Implementation
- Implement HTML parsing with style extraction
- Implement Apryse-based export
- Implement fallback logic

### Phase 3: Template Support
- Implement template loading
- Implement template application
- Add default template

### Phase 4: Testing & Refinement
- Add unit tests
- Add property-based tests
- Add integration tests
- Performance optimization

### Phase 5: Deployment
- Update documentation
- Deploy to staging
- User acceptance testing
- Deploy to production

## Future Enhancements

1. **Advanced Animations**: Support slide transitions and animations
2. **Chart Support**: Convert HTML charts to native PPTX charts
3. **Video Embedding**: Support video content in slides
4. **Collaborative Editing**: Real-time collaborative PPTX editing
5. **Cloud Storage**: Direct export to cloud storage (Google Drive, OneDrive)
