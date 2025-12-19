# Design Document

## Overview

This design document outlines the technical approach for simplifying the AI Slides application by removing unnecessary features while maintaining core PPT generation functionality. The simplification will involve code removal, database schema updates, configuration changes, and UI modifications across multiple layers of the application.

## Architecture

The AI Slides application follows a layered architecture:

- **Web Layer**: FastAPI routes and Jinja2 templates
- **Service Layer**: Business logic and AI integration
- **Data Layer**: SQLAlchemy models and database operations
- **Configuration Layer**: Environment variables and AI provider settings

The simplification will affect all layers, with the primary goal of reducing complexity while maintaining system stability.

## Components and Interfaces

### 1. Template Management System

**Current State:**
- Multiple template files in `template_examples/` directory (20+ templates)
- Database table `global_master_templates` storing template metadata
- Template loading logic in `create_default_template.py`

**Target State:**
- Keep only 4 templates: default + 3 selected templates
- Remove unused template files from filesystem
- Update template loading logic to skip removed templates
- Maintain database integrity for existing projects using removed templates

**Affected Files:**
- `template_examples/*.json` (remove most files)
- `src/ai_slides/database/create_default_template.py` (update loading logic)
- `src/ai_slides/web/templates/template_selection.html` (UI updates)

### 2. Authentication System

**Current State:**
- Full authentication module in `src/ai_slides/auth/`
- Database tables: `users`, `user_sessions`
- Authentication middleware protecting routes
- Login/logout/profile UI pages

**Target State:**
- Remove all authentication code
- Remove authentication middleware
- Remove user-related database tables
- Remove login/profile UI pages
- Make all routes publicly accessible

**Affected Files:**
- `src/ai_slides/auth/` (entire directory removal)
- `src/ai_slides/main.py` (remove auth middleware and router)
- `src/ai_slides/database/models.py` (remove User, UserSession models)
- `src/ai_slides/web/templates/login.html` (remove)
- `src/ai_slides/web/templates/profile.html` (remove)
- `src/ai_slides/api/config_api.py` (remove auth dependencies)

### 3. AI Provider Configuration

**Current State:**
- Support for multiple providers: OpenAI, Anthropic, Google/Gemini, Ollama, 302AI
- Provider factory pattern in `src/ai_slides/ai/providers.py`
- Configuration schema supporting all providers

**Target State:**
- Keep only OpenAI and Gemini providers
- Remove Anthropic, Ollama, and 302AI provider classes
- Simplify configuration schema
- Update UI to show only OpenAI and Gemini options

**Affected Files:**
- `src/ai_slides/ai/providers.py` (remove unused provider classes)
- `src/ai_slides/services/config_service.py` (update schema)
- `src/ai_slides/web/templates/ai_config.html` (UI updates)
- `.env` (remove unused provider keys)

### 4. Research Functionality

**Current State:**
- Deep research service using Tavily API
- Research report generation
- Web search integration
- Research-related UI components

**Target State:**
- Remove all research-related code
- Remove Tavily API integration
- Remove research service dependencies
- Remove research UI components

**Affected Files:**
- `src/ai_slides/services/deep_research_service.py` (remove)
- `src/ai_slides/services/research/` (entire directory removal)
- `src/ai_slides/services/research_report_generator.py` (remove)
- `src/ai_slides/web/templates/research_status.html` (remove)
- API routes related to research (identify and remove)

### 5. Export Functionality

**Current State:**
- Multiple export formats (PPTX, PDF, speech scripts)
- PDF conversion services
- Speech script generation and export
- Complex export UI with multiple options

**Target State:**
- Keep only PPTX export
- Remove PDF conversion code
- Remove speech script export
- Simplify export UI to single PPTX button

**Affected Files:**
- `src/ai_slides/services/pdf_to_pptx_converter.py` (remove)
- `src/ai_slides/services/pyppeteer_pdf_converter.py` (remove)
- `src/ai_slides/services/speech_script_exporter.py` (remove)
- `src/ai_slides/services/speech_script_service.py` (remove)
- `src/ai_slides/database/models.py` (remove SpeechScript model)
- Export UI components (simplify)

## Data Models

### Models to Remove

```python
# From src/ai_slides/database/models.py

class User(Base):
    # Remove entire model
    pass

class UserSession(Base):
    # Remove entire model
    pass

class SpeechScript(Base):
    # Remove entire model
    pass
```

### Models to Keep (No Changes)

- `Project` - Core project data
- `TodoBoard` - Workflow management
- `TodoStage` - Stage tracking
- `ProjectVersion` - Version control
- `SlideData` - Slide content
- `PPTTemplate` - Template data
- `GlobalMasterTemplate` - Master templates

### Database Migration Strategy

1. Create backup of existing database
2. Remove authentication tables (users, user_sessions)
3. Remove speech_scripts table
4. Keep all other tables intact
5. Update foreign key constraints if needed



## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

After analyzing all acceptance criteria, most of them are specific examples or edge cases rather than universal properties. The testable items are primarily:
- Specific configuration checks (template count, provider list)
- UI element presence/absence verification
- Database schema validation
- Route accessibility checks

These are best validated through example-based tests rather than property-based tests, as they test specific states rather than universal rules across all inputs.

### Example-Based Verification

Since most acceptance criteria involve checking specific system states or configurations, we will use example-based tests:

**Example 1: Template Count Verification**
*Given* the system has started, *when* we query the loaded templates, *then* exactly 4 templates should be present (1 default + 3 others)
**Validates: Requirements 1.1, 1.2**

**Example 2: Authentication Removal Verification**
*Given* the system is running, *when* we access any application route, *then* no authentication check should be performed and the route should be accessible
**Validates: Requirements 2.1, 2.2, 2.3**

**Example 3: AI Provider Restriction**
*Given* the system configuration, *when* we query available AI providers, *then* only "openai" and "gemini" should be in the list
**Validates: Requirements 3.1, 3.3**

**Example 4: Research Service Removal**
*Given* a PPT generation request, *when* the system processes it, *then* no research service methods should be invoked
**Validates: Requirements 4.1**

**Example 5: Export Format Restriction**
*Given* the export interface, *when* a user views export options, *then* only "Export PPTX" option should be visible
**Validates: Requirements 5.1, 5.3**

## Error Handling

### Template Loading Errors

**Scenario**: Missing template files or corrupted template data

**Handling Strategy**:
- Log warnings for missing templates
- Continue loading remaining valid templates
- Ensure at least one default template is available
- Gracefully handle projects referencing removed templates by falling back to default template

### Database Migration Errors

**Scenario**: Failed table removal or constraint violations

**Handling Strategy**:
- Create database backup before migration
- Use transactional migrations
- Rollback on failure
- Provide clear error messages for manual intervention

### Configuration Errors

**Scenario**: Invalid or missing AI provider configuration

**Handling Strategy**:
- Validate configuration on startup
- Provide clear error messages for missing API keys
- Fall back to available provider if one is misconfigured
- Log configuration issues prominently

### Route Access Errors

**Scenario**: Broken routes after authentication removal

**Handling Strategy**:
- Test all routes after auth removal
- Ensure no orphaned auth checks remain
- Update route dependencies
- Maintain backward compatibility where possible

## Testing Strategy

### Unit Testing

Unit tests will verify specific functionality:

1. **Template Loading Tests**
   - Test that exactly 4 templates are loaded
   - Test template file parsing
   - Test handling of missing template files

2. **Configuration Tests**
   - Test AI provider filtering
   - Test configuration validation
   - Test provider initialization

3. **Database Tests**
   - Test model removal
   - Test migration scripts
   - Test data integrity after changes

4. **Route Tests**
   - Test route accessibility without auth
   - Test that auth routes are removed
   - Test that all functional routes still work

### Integration Testing

Integration tests will verify system-wide behavior:

1. **End-to-End PPT Generation**
   - Test complete PPT generation workflow
   - Verify no research services are called
   - Verify export produces valid PPTX

2. **Template Selection Flow**
   - Test template selection UI
   - Test template application to projects
   - Test handling of legacy template references

3. **Configuration Management**
   - Test AI provider configuration
   - Test configuration persistence
   - Test provider switching

### Manual Testing Checklist

1. **UI Verification**
   - [ ] Login page is removed/inaccessible
   - [ ] Profile page is removed/inaccessible
   - [ ] Template selection shows exactly 4 templates
   - [ ] AI config shows only OpenAI and Gemini
   - [ ] Research UI elements are removed
   - [ ] Export shows only PPTX option

2. **Functionality Verification**
   - [ ] Can create new project without login
   - [ ] Can generate PPT with OpenAI
   - [ ] Can generate PPT with Gemini
   - [ ] Can export project as PPTX
   - [ ] Cannot access research features
   - [ ] Cannot access PDF export

3. **Database Verification**
   - [ ] Users table is removed
   - [ ] User_sessions table is removed
   - [ ] Speech_scripts table is removed
   - [ ] All other tables intact
   - [ ] Existing projects still accessible

## Implementation Phases

### Phase 1: Template Simplification
- Identify 3 templates to keep (in addition to default)
- Remove unused template files
- Update template loading logic
- Test template selection UI

### Phase 2: Authentication Removal
- Remove auth middleware from main.py
- Remove auth routes
- Remove auth templates
- Remove User and UserSession models
- Create database migration
- Test all routes are accessible

### Phase 3: AI Provider Simplification
- Remove unused provider classes
- Update provider factory
- Update configuration schema
- Update AI config UI
- Test with OpenAI and Gemini

### Phase 4: Research Removal
- Remove research service files
- Remove research routes
- Remove research UI templates
- Remove Tavily dependencies
- Test PPT generation without research

### Phase 5: Export Simplification
- Remove PDF conversion services
- Remove speech script services
- Remove SpeechScript model
- Update export UI
- Test PPTX export functionality

### Phase 6: Final Cleanup
- Remove unused dependencies from requirements
- Update documentation
- Clean up configuration files
- Final integration testing

## Dependencies

### External Dependencies to Remove

```
# From pyproject.toml or requirements.txt
- anthropic (Anthropic provider)
- ollama (Ollama provider)
- tavily-python (Research service)
- pyppeteer (PDF conversion)
```

### External Dependencies to Keep

```
- openai (OpenAI provider)
- google-generativeai (Gemini provider)
- fastapi (Web framework)
- sqlalchemy (Database ORM)
- python-pptx (PPTX generation)
```

## Rollback Strategy

In case of issues during simplification:

1. **Database Rollback**
   - Restore from backup created before migration
   - Revert migration scripts

2. **Code Rollback**
   - Use git to revert to previous commit
   - Restore removed files from backup

3. **Configuration Rollback**
   - Restore original .env file
   - Restore original configuration files

## Performance Considerations

### Expected Improvements

1. **Startup Time**: Faster due to fewer modules to load
2. **Memory Usage**: Lower due to fewer services running
3. **Code Complexity**: Reduced, easier to maintain
4. **Configuration Complexity**: Simplified, fewer options to manage

### Potential Risks

1. **Breaking Changes**: Existing projects may reference removed features
2. **Data Loss**: User accounts will be removed (acceptable for single-user tool)
3. **Feature Regression**: Ensure core PPT generation still works correctly

## Security Considerations

### Changes in Security Posture

1. **Authentication Removal**: Application becomes single-user, no access control
2. **Reduced Attack Surface**: Fewer features means fewer potential vulnerabilities
3. **Simplified Configuration**: Fewer API keys to manage

### Recommendations

1. Run application on localhost only or behind firewall
2. Use environment variables for API keys
3. Regular backups of project database
4. Monitor API key usage for cost control
