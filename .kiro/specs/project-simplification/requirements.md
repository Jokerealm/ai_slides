# Requirements Document

## Introduction

This document outlines the requirements for simplifying the AI Slides project by removing unnecessary features and configurations. The goal is to create a more maintainable, focused application that retains core PPT generation functionality while eliminating complex features that are not essential for basic usage.

## Glossary

- **System**: The AI Slides application
- **Template**: A PowerPoint design template with predefined styles and layouts
- **AI Provider**: An external AI service (OpenAI, Gemini, etc.) used for content generation
- **Authentication Module**: The login/user management system
- **Research Module**: The deep research and web search functionality
- **Export Function**: The capability to save generated presentations in various formats

## Requirements

### Requirement 1: Template Simplification

**User Story:** As a maintainer, I want to reduce the number of available templates, so that the application is easier to maintain and users are not overwhelmed with choices.

#### Acceptance Criteria

1. WHEN the System starts THEN the System SHALL load only the default template and 3 additional templates
2. WHEN a user accesses the template selection interface THEN the System SHALL display exactly 4 templates (default plus 3 others)
3. WHEN template files are removed from the filesystem THEN the System SHALL continue to function without errors
4. WHEN the database contains references to removed templates THEN the System SHALL handle these gracefully without crashes

### Requirement 2: Authentication Removal

**User Story:** As a maintainer, I want to remove all login and authentication functionality, so that the application runs as a single-user tool without access control overhead.

#### Acceptance Criteria

1. WHEN the System starts THEN the System SHALL not require user login
2. WHEN a user accesses any route THEN the System SHALL not perform authentication checks
3. WHEN authentication middleware is removed THEN all application routes SHALL remain accessible
4. WHEN the database schema is updated THEN the System SHALL remove all user authentication tables
5. WHEN the frontend loads THEN the System SHALL not display login, logout, or profile management interfaces

### Requirement 3: AI Configuration Simplification

**User Story:** As a user, I want to configure only OpenAI and Gemini API keys, so that I can focus on the AI providers I actually use without unnecessary configuration complexity.

#### Acceptance Criteria

1. WHEN the System loads AI configuration THEN the System SHALL support only OpenAI and Gemini providers
2. WHEN a user accesses the AI configuration interface THEN the System SHALL display only OpenAI API Key and Gemini configuration fields
3. WHEN the System initializes AI providers THEN the System SHALL not attempt to load other provider implementations
4. WHEN configuration files are read THEN the System SHALL ignore settings for removed AI providers
5. WHEN API calls are made THEN the System SHALL route requests only to OpenAI or Gemini endpoints

### Requirement 4: Research Functionality Removal

**User Story:** As a maintainer, I want to remove all research and web search features, so that the application focuses solely on PPT generation from user-provided content.

#### Acceptance Criteria

1. WHEN the System processes a PPT generation request THEN the System SHALL not invoke research services
2. WHEN a user accesses the web interface THEN the System SHALL not display research-related UI elements
3. WHEN API endpoints are registered THEN the System SHALL not expose research-related routes
4. WHEN the System imports modules THEN the System SHALL not load research service dependencies
5. WHEN background tasks execute THEN the System SHALL not schedule or run research-related jobs

### Requirement 5: Export Functionality Simplification

**User Story:** As a user, I want a simple PPTX export function, so that I can save my presentations without confusion from multiple export options.

#### Acceptance Criteria

1. WHEN a user requests to export a presentation THEN the System SHALL provide only PPTX format as an option
2. WHEN the export function executes THEN the System SHALL generate a standard PPTX file without additional format conversions
3. WHEN the export interface is displayed THEN the System SHALL show only a single "Export PPTX" action
4. WHEN PDF or other format export code exists THEN the System SHALL remove these implementations
5. WHEN the System completes an export THEN the System SHALL return the PPTX file to the user
