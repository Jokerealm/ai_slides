# System State Before Simplification

**Date:** December 18, 2024  
**Database Backup:** `ai_slides.db.backup` created

## Current System Overview

This document captures the state of the AI Slides system before simplification begins.

## 1. Template System

### Current Templates (25 total)
Located in `template_examples/` directory:

1. Toy风.json
2. 中国风.json
3. 中式书卷风.json
4. 五彩斑斓的黑.json
5. 吉卜力风.json
6. 商务.json
7. 大气红.json
8. 宣纸风.json
9. 拟态风.json
10. 日落大道.json
11. 星月夜风.json
12. 星月蓝.json
13. 森林绿.json
14. 模糊玻璃.json
15. 清新笔记.json
16. 清新风.json
17. 科技风.json
18. 竹简风.json
19. 简约答辩风.json
20. 素白风.json
21. 终端风.json
22. 莫奈风.json
23. 赛博朋克风.json
24. 速度黄.json
25. 饺子风.json

### Template Loading
- Templates loaded via `src/ai_slides/database/create_default_template.py`
- Stored in `global_master_templates` database table
- UI selection in `src/ai_slides/web/templates/template_selection.html`

## 2. Authentication System

### Components
- **Module Location:** `src/ai_slides/auth/`
- **Files:**
  - `auth_service.py` - Core authentication logic
  - `middleware.py` - Authentication middleware
  - `routes.py` - Auth API routes
  - `__init__.py`

### Database Models
- `User` - User accounts with password hashing
- `UserSession` - Session management with expiration

### Features
- User registration and login
- Password hashing (SHA256)
- Session management with configurable expiration
- Admin user support
- Default admin account: admin/admin123

### UI Templates
- `login.html` - Login page
- `profile.html` - User profile management

## 3. AI Provider Configuration

### Supported Providers (6 total)
1. **OpenAI** - `OpenAIProvider`
2. **Anthropic** - `AnthropicProvider` (Claude)
3. **Google/Gemini** - `GoogleProvider`
4. **Ollama** - `OllamaProvider` (local models)
5. **302AI** - Uses OpenAI-compatible API

### Provider Implementation
- **Location:** `src/ai_slides/ai/providers.py`
- **Factory Pattern:** `AIProviderFactory` with provider registry
- **Manager:** `AIProviderManager` with caching
- **Base Class:** `AIProvider` in `src/ai_slides/ai/base.py`

### Features
- Multimodal support (text + images)
- Streaming responses
- Role-based model configuration
- Provider-specific configuration
- Think tag filtering (OpenAI)

### Configuration
- **Service:** `src/ai_slides/services/config_service.py`
- **UI:** `src/ai_slides/web/templates/ai_config.html`
- **Environment:** `.env` file with provider-specific keys

## 4. Research Functionality

### Components
- **Deep Research Service:** `src/ai_slides/services/deep_research_service.py`
- **Research Module:** `src/ai_slides/services/research/` directory
  - `content_extractor.py`
  - `enhanced_report_generator.py`
  - `enhanced_research_service.py`
  - `searxng_provider.py`
- **Report Generator:** `src/ai_slides/services/research_report_generator.py`

### Features
- Web search integration (Tavily API)
- Content extraction from URLs
- Research report generation
- Deep research workflows

### UI
- `research_status.html` - Research progress tracking
- Research-related UI elements in other templates

## 5. Export Functionality

### Current Export Options
1. **PPTX Export** - Standard PowerPoint format (KEEP)
2. **PDF Export** - PDF conversion services (REMOVE)
3. **Speech Script Export** - Presentation scripts (REMOVE)

### PDF Conversion Services
- `pdf_to_pptx_converter.py` - PDF to PPTX conversion
- `pyppeteer_pdf_converter.py` - Browser-based PDF generation
- `pdf_to_pptx_worker.py` - Background worker for PDF tasks

### Speech Script Services
- `speech_script_exporter.py` - Export speech scripts
- `speech_script_service.py` - Speech script generation
- `speech_script_repository.py` - Database operations

### Database Model
- `SpeechScript` - Stores generated speech scripts
- Relationship with `Project` model

## 6. Database Schema

### Current Tables
- `users` - User accounts (TO REMOVE)
- `user_sessions` - Session data (TO REMOVE)
- `speech_scripts` - Speech scripts (TO REMOVE)
- `projects` - Core project data (KEEP)
- `todo_boards` - Workflow management (KEEP)
- `todo_stages` - Stage tracking (KEEP)
- `project_versions` - Version control (KEEP)
- `slide_data` - Slide content (KEEP)
- `ppt_templates` - Template data (KEEP)
- `global_master_templates` - Master templates (KEEP)

### Migration Files
- `src/ai_slides/database/migrations/add_project_share_fields.py`
- `src/ai_slides/database/migrations/add_speech_scripts_table.py`

## 7. Dependencies

### External Libraries (to be reviewed)
- `openai` - OpenAI API (KEEP)
- `google-generativeai` - Gemini API (KEEP)
- `anthropic` - Anthropic API (REMOVE)
- `ollama` - Ollama local models (REMOVE)
- `tavily-python` - Research/search API (REMOVE)
- `pyppeteer` - PDF conversion (REMOVE)
- `fastapi` - Web framework (KEEP)
- `sqlalchemy` - Database ORM (KEEP)
- `python-pptx` - PPTX generation (KEEP)

## 8. Application Structure

### Main Entry Point
- `src/ai_slides/main.py` - FastAPI application setup

### Web Layer
- Routes: `src/ai_slides/web/routes.py`
- Templates: `src/ai_slides/web/templates/`
- Static files: `src/ai_slides/web/static/`

### API Layer
- `src/ai_slides/api/ai_slides_api.py` - Main API endpoints
- `src/ai_slides/api/config_api.py` - Configuration API
- `src/ai_slides/api/database_api.py` - Database operations
- `src/ai_slides/api/image_api.py` - Image handling
- `src/ai_slides/api/global_master_template_api.py` - Template API
- `src/ai_slides/api/openai_compat.py` - OpenAI compatibility

### Service Layer
- AI services: `src/ai_slides/services/ai_service.py`
- PPT generation: `src/ai_slides/services/ppt_service.py`
- Enhanced PPT: `src/ai_slides/services/enhanced_ppt_service.py`
- Image services: `src/ai_slides/services/image/`
- Project management: `src/ai_slides/services/project_manager.py`
- Background tasks: `src/ai_slides/services/background_tasks.py`

## 9. Configuration Files

### Environment Configuration
- `.env` - Environment variables
- `.env.example` - Example configuration (if exists)

### Project Configuration
- `pyproject.toml` - Python project metadata and dependencies
- `docker-compose.yml` - Docker configuration
- `Dockerfile` - Container image definition

## 10. Backup Information

### Database Backup
- **Original:** `ai_slides.db`
- **Backup:** `ai_slides.db.backup`
- **Created:** December 18, 2024
- **Size:** [Database file size]

### Restoration Instructions
If rollback is needed:
```powershell
# Stop the application
# Restore database
Copy-Item ai_slides.db.backup ai_slides.db -Force
# Restart the application
```

## Next Steps

After documenting the current state, the simplification will proceed with:
1. Template reduction (25 → 4 templates)
2. Authentication removal
3. AI provider simplification (6 → 2 providers)
4. Research functionality removal
5. Export simplification (3 → 1 format)

---

**Document Status:** Complete  
**Ready for Simplification:** Yes
