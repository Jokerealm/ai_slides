# Implementation Plan

- [x] 1. Prepare for simplification





  - Create database backup
  - Document current system state
  - Identify 3 templates to keep (besides default)
  - _Requirements: All_

- [x] 2. Simplify template system





  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 2.1 Identify and keep 4 templates


  - Review all templates in `template_examples/` directory
  - Select default template and 3 best alternatives
  - Document selected templates
  - _Requirements: 1.1_

- [x] 2.2 Remove unused template files


  - Delete unselected template JSON files from `template_examples/`
  - Keep only the 4 selected templates
  - _Requirements: 1.1, 1.3_


- [x] 2.3 Update template loading logic

  - Modify `src/ai_slides/database/create_default_template.py`
  - Ensure only selected templates are imported
  - Add error handling for missing templates
  - _Requirements: 1.1, 1.3, 1.4_

- [x] 2.4 Test template system


  - Verify exactly 4 templates load on startup
  - Test template selection UI displays 4 templates
  - Test system handles removed template references gracefully
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 3. Remove authentication system





  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [x] 3.1 Remove authentication middleware


  - Remove auth middleware from `src/ai_slides/main.py`
  - Remove auth router import and registration
  - Remove `get_current_admin_user` and related dependencies
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 3.2 Remove authentication routes and templates


  - Delete `src/ai_slides/auth/` directory
  - Delete `src/ai_slides/web/templates/login.html`
  - Delete `src/ai_slides/web/templates/profile.html`
  - _Requirements: 2.5_

- [x] 3.3 Update API routes to remove auth dependencies


  - Update `src/ai_slides/api/config_api.py` to remove `get_current_admin_user` dependency
  - Update other API routes that use auth dependencies
  - Ensure all routes are publicly accessible
  - _Requirements: 2.2, 2.3_

- [x] 3.4 Remove authentication database models


  - Remove `User` class from `src/ai_slides/database/models.py`
  - Remove `UserSession` class from `src/ai_slides/database/models.py`
  - _Requirements: 2.4_

- [x] 3.5 Create database migration script


  - Create migration to drop `users` table
  - Create migration to drop `user_sessions` table
  - Test migration on backup database
  - _Requirements: 2.4_

- [x] 3.6 Test authentication removal


  - Verify application starts without authentication
  - Test all routes are accessible without login
  - Verify no auth UI elements are displayed
  - _Requirements: 2.1, 2.2, 2.3, 2.5_

- [x] 4. Checkpoint - Verify system stability





  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Simplify AI provider configuration





  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 5.1 Remove unused AI provider classes


  - Remove `AnthropicProvider` class from `src/ai_slides/ai/providers.py`
  - Remove `OllamaProvider` class from `src/ai_slides/ai/providers.py`
  - Remove 302AI provider references
  - Update `AIProviderFactory._providers` dict to only include openai and gemini
  - _Requirements: 3.1, 3.3_

- [x] 5.2 Update configuration schema


  - Modify `src/ai_slides/services/config_service.py` to remove unused provider configs
  - Update configuration validation to only accept OpenAI and Gemini settings
  - _Requirements: 3.1, 3.4_

- [x] 5.3 Update AI configuration UI


  - Modify `src/ai_slides/web/templates/ai_config.html`
  - Remove UI elements for Anthropic, Ollama, and 302AI
  - Keep only OpenAI and Gemini configuration fields
  - _Requirements: 3.2_

- [x] 5.4 Clean up environment configuration


  - Update `.env` file to remove unused provider keys
  - Document required keys (OpenAI and Gemini only)
  - _Requirements: 3.4_

- [x] 5.5 Test AI provider simplification


  - Verify only OpenAI and Gemini providers are available
  - Test AI config UI shows only 2 providers
  - Test PPT generation with OpenAI
  - Test PPT generation with Gemini
  - _Requirements: 3.1, 3.2, 3.3, 3.5_

- [x] 6. Remove research functionality





  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 6.1 Remove research service files


  - Delete `src/ai_slides/services/deep_research_service.py`
  - Delete `src/ai_slides/services/research/` directory
  - Delete `src/ai_slides/services/research_report_generator.py`
  - _Requirements: 4.1, 4.4_

- [x] 6.2 Remove research API routes


  - Identify and remove research-related routes from API routers
  - Remove research route imports
  - _Requirements: 4.3_

- [x] 6.3 Remove research UI templates


  - Delete `src/ai_slides/web/templates/research_status.html`
  - Remove research-related UI elements from other templates
  - _Requirements: 4.2_

- [x] 6.4 Remove research dependencies


  - Remove Tavily API configuration
  - Remove research-related imports from service files
  - _Requirements: 4.4_

- [x] 6.5 Test research removal


  - Verify PPT generation works without research
  - Verify no research UI elements are visible
  - Verify no research routes are accessible
  - _Requirements: 4.1, 4.2, 4.3_

- [x] 7. Simplify export functionality




  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 7.1 Remove PDF conversion services


  - Delete `src/ai_slides/services/pdf_to_pptx_converter.py`
  - Delete `src/ai_slides/services/pyppeteer_pdf_converter.py`
  - Delete `src/ai_slides/services/pdf_to_pptx_worker.py`
  - _Requirements: 5.4_


- [x] 7.2 Remove speech script services

  - Delete `src/ai_slides/services/speech_script_exporter.py`
  - Delete `src/ai_slides/services/speech_script_service.py`
  - Delete `src/ai_slides/services/speech_script_repository.py`
  - _Requirements: 5.4_


- [x] 7.3 Remove SpeechScript database model

  - Remove `SpeechScript` class from `src/ai_slides/database/models.py`
  - Remove speech_scripts relationship from `Project` model
  - _Requirements: 5.4_


- [x] 7.4 Create database migration for speech scripts

  - Create migration to drop `speech_scripts` table
  - Test migration on backup database
  - _Requirements: 5.4_

- [x] 7.5 Simplify export UI


  - Update export-related templates to show only PPTX option
  - Remove PDF and speech script export buttons
  - Ensure PPTX export functionality works
  - _Requirements: 5.1, 5.3_

- [x] 7.6 Test export simplification


  - Verify only PPTX export option is visible
  - Test PPTX export generates valid file
  - Verify PDF and speech script exports are not accessible
  - _Requirements: 5.1, 5.2, 5.3, 5.5_

- [x] 8. Final cleanup and testing





  - _Requirements: All_

- [x] 8.1 Remove unused dependencies


  - Update `pyproject.toml` to remove anthropic, ollama, tavily-python, pyppeteer
  - Run dependency cleanup
  - _Requirements: All_

- [x] 8.2 Update documentation


  - Update README with simplified feature list
  - Document required environment variables
  - Update configuration examples
  - _Requirements: All_

- [x] 8.3 Clean up configuration files


  - Remove unused configuration sections
  - Simplify .env.example
  - _Requirements: All_

- [x] 8.4 Final integration testing


  - Test complete PPT generation workflow
  - Test all remaining features work correctly
  - Verify no broken links or errors
  - Test with both OpenAI and Gemini
  - _Requirements: All_

- [x] 9. Final Checkpoint - Complete verification





  - Ensure all tests pass, ask the user if questions arise.
  - Update simplification_progress.md with completion status
