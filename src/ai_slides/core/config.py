"""
Configuration management for AI Slides AI features
"""

import os
from typing import Optional, Dict, Any, ClassVar
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables with error handling
try:
    load_dotenv()
except (PermissionError, FileNotFoundError) as e:
    # Silently continue if .env file is not accessible
    # This allows the application to work with system environment variables
    pass
except Exception as e:
    # Log other errors but continue
    import logging
    logging.getLogger(__name__).warning(f"Could not load .env file: {e}")

class AIConfig(BaseSettings):
    """AI configuration settings"""
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_base_url: str = Field(default="https://api.openai.com/v1", env="OPENAI_BASE_URL")
    openai_model: str = Field(default="gpt-3.5-turbo", env="OPENAI_MODEL")
    
    # Anthropic Configuration
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    anthropic_model: str = Field(default="claude-3-haiku-20240307", env="ANTHROPIC_MODEL")

    # Google Gemini Configuration
    google_api_key: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    google_base_url: str = Field(default="https://generativelanguage.googleapis.com", env="GOOGLE_BASE_URL")
    google_model: str = Field(default="gemini-1.5-flash", env="GOOGLE_MODEL")
    
    # Azure OpenAI Configuration
    azure_openai_api_key: Optional[str] = Field(default=None, env="AZURE_OPENAI_API_KEY")
    azure_openai_endpoint: Optional[str] = Field(default=None, env="AZURE_OPENAI_ENDPOINT")
    azure_openai_api_version: str = Field(default="2024-02-15-preview", env="AZURE_OPENAI_API_VERSION")
    azure_openai_deployment_name: Optional[str] = Field(default=None, env="AZURE_OPENAI_DEPLOYMENT_NAME")
    
    # Ollama Configuration
    ollama_base_url: str = Field(default="http://localhost:11434", env="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="llama2", env="OLLAMA_MODEL")
    
    # 302.AI Configuration
    ai_302ai_api_key: Optional[str] = Field(default=None, env="302AI_API_KEY", alias="302ai_api_key")
    ai_302ai_base_url: str = Field(default="https://api.302.ai/v1", env="302AI_BASE_URL", alias="302ai_base_url")
    ai_302ai_model: str = Field(default="gpt-4o", env="302AI_MODEL", alias="302ai_model")
    
    # Hugging Face Configuration
    huggingface_api_token: Optional[str] = Field(default=None, env="HUGGINGFACE_API_TOKEN")

    # Apryse SDK Configuration (for PPTX export functionality)
    apryse_license_key: Optional[str] = Field(default=None, env="APRYSE_LICENSE_KEY")

    # Provider Selection
    default_ai_provider: str = Field(default="openai", env="DEFAULT_AI_PROVIDER")
    
    # Model Role Configuration
    default_model_provider: Optional[str] = Field(default=None, env="DEFAULT_MODEL_PROVIDER")
    default_model_name: Optional[str] = Field(default=None, env="DEFAULT_MODEL_NAME")
    outline_model_provider: Optional[str] = Field(default=None, env="OUTLINE_MODEL_PROVIDER")
    outline_model_name: Optional[str] = Field(default=None, env="OUTLINE_MODEL_NAME")
    creative_model_provider: Optional[str] = Field(default=None, env="CREATIVE_MODEL_PROVIDER")
    creative_model_name: Optional[str] = Field(default=None, env="CREATIVE_MODEL_NAME")
    image_prompt_model_provider: Optional[str] = Field(default=None, env="IMAGE_PROMPT_MODEL_PROVIDER")
    image_prompt_model_name: Optional[str] = Field(default=None, env="IMAGE_PROMPT_MODEL_NAME")
    slide_generation_model_provider: Optional[str] = Field(default=None, env="SLIDE_GENERATION_MODEL_PROVIDER")
    slide_generation_model_name: Optional[str] = Field(default=None, env="SLIDE_GENERATION_MODEL_NAME")
    editor_assistant_model_provider: Optional[str] = Field(default=None, env="EDITOR_ASSISTANT_MODEL_PROVIDER")
    editor_assistant_model_name: Optional[str] = Field(default=None, env="EDITOR_ASSISTANT_MODEL_NAME")
    template_generation_model_provider: Optional[str] = Field(default=None, env="TEMPLATE_GENERATION_MODEL_PROVIDER")
    template_generation_model_name: Optional[str] = Field(default=None, env="TEMPLATE_GENERATION_MODEL_NAME")
    speech_script_model_provider: Optional[str] = Field(default=None, env="SPEECH_SCRIPT_MODEL_PROVIDER")
    speech_script_model_name: Optional[str] = Field(default=None, env="SPEECH_SCRIPT_MODEL_NAME")
    vision_analysis_model_provider: Optional[str] = Field(default=None, env="VISION_ANALYSIS_MODEL_PROVIDER")
    vision_analysis_model_name: Optional[str] = Field(default=None, env="VISION_ANALYSIS_MODEL_NAME")

    # Generation Parameters
    max_tokens: int = Field(default=16384, env="MAX_TOKENS")
    temperature: float = Field(default=0.7, env="TEMPERATURE")
    top_p: float = Field(default=1.0, env="TOP_P")
    
    # Parallel Generation Configuration
    enable_parallel_generation: bool = Field(default=False, env="ENABLE_PARALLEL_GENERATION")
    parallel_slides_count: int = Field(default=3, env="PARALLEL_SLIDES_COUNT")
    
    # Feature Flags
    enable_network_mode: bool = Field(default=True, env="ENABLE_NETWORK_MODE")
    enable_local_models: bool = Field(default=False, env="ENABLE_LOCAL_MODELS")
    enable_streaming: bool = Field(default=True, env="ENABLE_STREAMING")
    enable_auto_layout_repair: bool = Field(default=False, env="ENABLE_AUTO_LAYOUT_REPAIR")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_ai_requests: bool = Field(default=False, env="LOG_AI_REQUESTS")
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"
    }



    MODEL_ROLE_FIELDS: ClassVar[dict[str, tuple[str, str]]] = {
        "default": ("default_model_provider", "default_model_name"),
        "outline": ("outline_model_provider", "outline_model_name"),
        "creative": ("creative_model_provider", "creative_model_name"),
        "image_prompt": ("image_prompt_model_provider", "image_prompt_model_name"),
        "slide_generation": ("slide_generation_model_provider", "slide_generation_model_name"),
        "editor": ("editor_assistant_model_provider", "editor_assistant_model_name"),
        "template": ("template_generation_model_provider", "template_generation_model_name"),
        "speech_script": ("speech_script_model_provider", "speech_script_model_name"),
        "vision_analysis": ("vision_analysis_model_provider", "vision_analysis_model_name"),
    }

    MODEL_ROLE_LABELS: ClassVar[dict[str, str]] = {
        "default": "默认模型",
        "outline": "大纲生成 / 要点增强模型",
        "creative": "创意指导模型",
        "image_prompt": "配图与提示词模型",
        "slide_generation": "幻灯片生成模型",
        "editor": "AI编辑助手模型",
        "template": "AI模板生成模型",
        "speech_script": "演讲稿生成模型",
        "vision_analysis": "多模态视觉分析模型",
    }



    @staticmethod
    def _normalize_optional_str(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        if not isinstance(value, str):
            value = str(value)
        value = value.strip()
        return value or None

    def _normalize_provider(self, provider: Optional[str]) -> Optional[str]:
        normalized = self._normalize_optional_str(provider)
        return normalized.lower() if normalized else None

    def _get_default_model_for_provider(self, provider: Optional[str]) -> Optional[str]:
        provider_key = self._normalize_provider(provider)
        if provider_key == "openai":
            return self._normalize_optional_str(self.openai_model)
        if provider_key == "anthropic":
            return self._normalize_optional_str(self.anthropic_model)
        if provider_key in ("google", "gemini"):
            return self._normalize_optional_str(self.google_model)
        if provider_key == "302ai":
            return self._normalize_optional_str(self.ai_302ai_model)
        if provider_key == "ollama":
            return self._normalize_optional_str(self.ollama_model)
        if provider_key == "azure_openai":
            return self._normalize_optional_str(getattr(self, "azure_openai_deployment_name", None))
        return self._normalize_optional_str(self.openai_model)

    def get_model_config_for_role(self, role: str, provider_override: Optional[str] = None) -> Dict[str, Optional[str]]:
        role_key = (role or "default").lower()
        if role_key not in self.MODEL_ROLE_FIELDS:
            raise ValueError(f"Unknown model role: {role}")

        provider_field, model_field = self.MODEL_ROLE_FIELDS[role_key]
        configured_provider = self._normalize_provider(getattr(self, provider_field, None))
        configured_model = self._normalize_optional_str(getattr(self, model_field, None))
        override_provider = self._normalize_provider(provider_override)

        effective_provider = override_provider or configured_provider or self._normalize_provider(self.default_ai_provider) or "openai"

        if override_provider:
            if override_provider == configured_provider and configured_model:
                effective_model = configured_model
            else:
                effective_model = self._get_default_model_for_provider(override_provider)
        else:
            effective_model = configured_model or self._get_default_model_for_provider(effective_provider)

        return {
            "role": role_key,
            "provider": effective_provider,
            "model": effective_model
        }

    def get_all_model_roles(self) -> Dict[str, Dict[str, Optional[str]]]:
        roles = {}
        for role_key, (provider_field, model_field) in self.MODEL_ROLE_FIELDS.items():
            roles[role_key] = {
                "provider": self._normalize_optional_str(getattr(self, provider_field, None)),
                "model": self._normalize_optional_str(getattr(self, model_field, None)),
                "label": self.MODEL_ROLE_LABELS.get(role_key)
            }
        return roles


    def get_provider_config(self, provider: Optional[str] = None) -> Dict[str, Any]:
        """Get configuration for a specific AI provider"""
        provider = provider or self.default_ai_provider

        # Built-in providers
        configs = {
            "openai": {
                "api_key": self.openai_api_key,
                "base_url": self.openai_base_url,
                "model": self.openai_model,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
            },
            "anthropic": {
                "api_key": self.anthropic_api_key,
                "model": self.anthropic_model,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
            },
            "google": {
                "api_key": self.google_api_key,
                "base_url": self.google_base_url,
                "model": self.google_model,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
            },
            "gemini": {  # Alias for google
                "api_key": self.google_api_key,
                "base_url": self.google_base_url,
                "model": self.google_model,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
            },
            "azure_openai": {
                "api_key": self.azure_openai_api_key,
                "endpoint": self.azure_openai_endpoint,
                "api_version": self.azure_openai_api_version,
                "deployment_name": self.azure_openai_deployment_name,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
            },
            "ollama": {
                "base_url": self.ollama_base_url,
                "model": self.ollama_model,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
            },
            "302ai": {
                "api_key": self.ai_302ai_api_key,
                "base_url": self.ai_302ai_base_url,
                "model": self.ai_302ai_model,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
            }
        }

        return configs.get(provider, configs.get("openai", {}))
    
    def is_provider_available(self, provider: str) -> bool:
        """Check if a provider is properly configured"""
        config = self.get_provider_config(provider)

        # Built-in providers
        if provider == "openai":
            return bool(config.get("api_key"))
        elif provider == "anthropic":
            return bool(config.get("api_key"))
        elif provider == "google" or provider == "gemini":
            return bool(config.get("api_key"))
        elif provider == "azure_openai":
            return bool(config.get("api_key") and config.get("endpoint"))
        elif provider == "ollama":
            return self.enable_local_models
        elif provider == "302ai":
            return bool(config.get("api_key"))

        return False
    
    def get_available_providers(self) -> list[str]:
        """Get list of available AI providers"""
        providers = []

        # Add built-in providers
        for provider in ["openai", "anthropic", "google", "gemini", "azure_openai", "ollama", "302ai"]:
            if self.is_provider_available(provider):
                providers.append(provider)

        return providers

# Global configuration instance
ai_config = AIConfig()

def reload_ai_config():
    """Reload AI configuration from environment variables"""
    global ai_config
    # Force reload environment variables with error handling
    from dotenv import load_dotenv
    import os
    env_file = os.path.join(os.getcwd(), '.env')
    try:
        load_dotenv(env_file, override=True)
    except (PermissionError, FileNotFoundError) as e:
        # Silently continue if .env file is not accessible
        pass
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"Could not reload .env file: {e}")

    # Force update the existing instance with new values from environment
    ai_config.openai_model = os.environ.get('OPENAI_MODEL', ai_config.openai_model)
    ai_config.openai_base_url = os.environ.get('OPENAI_BASE_URL', ai_config.openai_base_url)
    ai_config.openai_api_key = os.environ.get('OPENAI_API_KEY', ai_config.openai_api_key)
    ai_config.anthropic_api_key = os.environ.get('ANTHROPIC_API_KEY', ai_config.anthropic_api_key)
    ai_config.anthropic_model = os.environ.get('ANTHROPIC_MODEL', ai_config.anthropic_model)
    ai_config.google_api_key = os.environ.get('GOOGLE_API_KEY', ai_config.google_api_key)
    ai_config.google_base_url = os.environ.get('GOOGLE_BASE_URL', ai_config.google_base_url)
    ai_config.google_model = os.environ.get('GOOGLE_MODEL', ai_config.google_model)
    ai_config.ai_302ai_api_key = os.environ.get('302AI_API_KEY', ai_config.ai_302ai_api_key)
    ai_config.ai_302ai_base_url = os.environ.get('302AI_BASE_URL', ai_config.ai_302ai_base_url)
    ai_config.ai_302ai_model = os.environ.get('302AI_MODEL', ai_config.ai_302ai_model)
    ai_config.default_ai_provider = os.environ.get('DEFAULT_AI_PROVIDER', ai_config.default_ai_provider)
    model_provider_env = os.environ.get('DEFAULT_MODEL_PROVIDER')
    ai_config.default_model_provider = (ai_config._normalize_optional_str(model_provider_env)
                                        if model_provider_env is not None else ai_config.default_model_provider)
    model_name_env = os.environ.get('DEFAULT_MODEL_NAME')
    ai_config.default_model_name = (ai_config._normalize_optional_str(model_name_env)
                                    if model_name_env is not None else ai_config.default_model_name)

    outline_provider_env = os.environ.get('OUTLINE_MODEL_PROVIDER')
    ai_config.outline_model_provider = (ai_config._normalize_optional_str(outline_provider_env)
                                        if outline_provider_env is not None else ai_config.outline_model_provider)
    outline_model_env = os.environ.get('OUTLINE_MODEL_NAME')
    ai_config.outline_model_name = (ai_config._normalize_optional_str(outline_model_env)
                                    if outline_model_env is not None else ai_config.outline_model_name)

    creative_provider_env = os.environ.get('CREATIVE_MODEL_PROVIDER')
    ai_config.creative_model_provider = (ai_config._normalize_optional_str(creative_provider_env)
                                         if creative_provider_env is not None else ai_config.creative_model_provider)
    creative_model_env = os.environ.get('CREATIVE_MODEL_NAME')
    ai_config.creative_model_name = (ai_config._normalize_optional_str(creative_model_env)
                                     if creative_model_env is not None else ai_config.creative_model_name)

    image_prompt_provider_env = os.environ.get('IMAGE_PROMPT_MODEL_PROVIDER')
    ai_config.image_prompt_model_provider = (ai_config._normalize_optional_str(image_prompt_provider_env)
                                             if image_prompt_provider_env is not None else ai_config.image_prompt_model_provider)
    image_prompt_model_env = os.environ.get('IMAGE_PROMPT_MODEL_NAME')
    ai_config.image_prompt_model_name = (ai_config._normalize_optional_str(image_prompt_model_env)
                                         if image_prompt_model_env is not None else ai_config.image_prompt_model_name)

    slide_provider_env = os.environ.get('SLIDE_GENERATION_MODEL_PROVIDER')
    ai_config.slide_generation_model_provider = (ai_config._normalize_optional_str(slide_provider_env)
                                                 if slide_provider_env is not None else ai_config.slide_generation_model_provider)
    slide_model_env = os.environ.get('SLIDE_GENERATION_MODEL_NAME')
    ai_config.slide_generation_model_name = (ai_config._normalize_optional_str(slide_model_env)
                                             if slide_model_env is not None else ai_config.slide_generation_model_name)

    editor_provider_env = os.environ.get('EDITOR_ASSISTANT_MODEL_PROVIDER')
    ai_config.editor_assistant_model_provider = (ai_config._normalize_optional_str(editor_provider_env)
                                                 if editor_provider_env is not None else ai_config.editor_assistant_model_provider)
    editor_model_env = os.environ.get('EDITOR_ASSISTANT_MODEL_NAME')
    ai_config.editor_assistant_model_name = (ai_config._normalize_optional_str(editor_model_env)
                                             if editor_model_env is not None else ai_config.editor_assistant_model_name)

    template_provider_env = os.environ.get('TEMPLATE_GENERATION_MODEL_PROVIDER')
    ai_config.template_generation_model_provider = (ai_config._normalize_optional_str(template_provider_env)
                                                   if template_provider_env is not None else ai_config.template_generation_model_provider)
    template_model_env = os.environ.get('TEMPLATE_GENERATION_MODEL_NAME')
    ai_config.template_generation_model_name = (ai_config._normalize_optional_str(template_model_env)
                                               if template_model_env is not None else ai_config.template_generation_model_name)

    speech_provider_env = os.environ.get('SPEECH_SCRIPT_MODEL_PROVIDER')
    ai_config.speech_script_model_provider = (ai_config._normalize_optional_str(speech_provider_env)
                                              if speech_provider_env is not None else ai_config.speech_script_model_provider)
    speech_model_env = os.environ.get('SPEECH_SCRIPT_MODEL_NAME')
    ai_config.speech_script_model_name = (ai_config._normalize_optional_str(speech_model_env)
                                         if speech_model_env is not None else ai_config.speech_script_model_name)

    vision_provider_env = os.environ.get('VISION_ANALYSIS_MODEL_PROVIDER')
    ai_config.vision_analysis_model_provider = (ai_config._normalize_optional_str(vision_provider_env)
                                               if vision_provider_env is not None else ai_config.vision_analysis_model_provider)
    vision_model_env = os.environ.get('VISION_ANALYSIS_MODEL_NAME')
    ai_config.vision_analysis_model_name = (ai_config._normalize_optional_str(vision_model_env)
                                            if vision_model_env is not None else ai_config.vision_analysis_model_name)

    ai_config.max_tokens = int(os.environ.get('MAX_TOKENS', str(ai_config.max_tokens)))
    ai_config.temperature = float(os.environ.get('TEMPERATURE', str(ai_config.temperature)))
    ai_config.top_p = float(os.environ.get('TOP_P', str(ai_config.top_p)))
    
    # Update parallel generation configuration
    ai_config.enable_parallel_generation = os.environ.get('ENABLE_PARALLEL_GENERATION', str(ai_config.enable_parallel_generation)).lower() == 'true'
    ai_config.parallel_slides_count = int(os.environ.get('PARALLEL_SLIDES_COUNT', str(ai_config.parallel_slides_count)))
    ai_config.enable_auto_layout_repair = os.environ.get('ENABLE_AUTO_LAYOUT_REPAIR', str(ai_config.enable_auto_layout_repair)).lower() == 'true'

    ai_config.apryse_license_key = os.environ.get('APRYSE_LICENSE_KEY', ai_config.apryse_license_key)

class AppConfig(BaseSettings):
    """Application configuration"""
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    debug: bool = Field(default=True, env="DEBUG")
    reload: bool = Field(default=True, env="RELOAD")
    
    # Database Configuration (for future use)
    database_url: str = Field(default="sqlite:///./ai_slides.db", env="DATABASE_URL")
    
    # Security Configuration
    secret_key: str = Field(default="your-secret-key-here", env="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # File Upload Configuration
    max_file_size: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    upload_dir: str = Field(default="uploads", env="UPLOAD_DIR")
    
    # Cache Configuration
    cache_ttl: int = Field(default=3600, env="CACHE_TTL")  # 1 hour
    
    model_config = {
        "case_sensitive": False,
        "extra": "ignore"
    }

# Global app configuration instance
app_config = AppConfig()
