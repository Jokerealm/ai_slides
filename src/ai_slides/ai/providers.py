"""
AI provider implementations
"""

import asyncio
import json
import logging
import re
from typing import List, Dict, Any, Optional, AsyncGenerator, Union, Tuple

from .base import AIProvider, AIMessage, AIResponse, MessageRole, TextContent, ImageContent, MessageContentType
from ..core.config import ai_config

logger = logging.getLogger(__name__)


class OpenAIProvider(AIProvider):
    """OpenAI API provider"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        try:
            import openai
            self.client = openai.AsyncOpenAI(
                api_key=config.get("api_key"),
                base_url=config.get("base_url")
            )
        except ImportError:
            logger.warning("OpenAI library not installed. Install with: pip install openai")
            self.client = None

    def _convert_message_to_openai(self, message: AIMessage) -> Dict[str, Any]:
        """Convert AIMessage to OpenAI format, supporting multimodal content"""
        openai_message = {"role": message.role.value}

        if isinstance(message.content, str):
            # Simple text message
            openai_message["content"] = message.content
        elif isinstance(message.content, list):
            # Multimodal message
            content_parts = []
            for part in message.content:
                if isinstance(part, TextContent):
                    content_parts.append({
                        "type": "text",
                        "text": part.text
                    })
                elif isinstance(part, ImageContent):
                    content_parts.append({
                        "type": "image_url",
                        "image_url": part.image_url
                    })
            openai_message["content"] = content_parts
        else:
            # Fallback to string representation
            openai_message["content"] = str(message.content)

        if message.name:
            openai_message["name"] = message.name

        return openai_message

    def _filter_think_content(self, content: str) -> str:
        """
        Filter out content within think tags in all forms
        Supports: <think>, <think>, ＜think＞, 【think】 and their closing tags
        This prevents internal reasoning from being exposed in the output
        """
        if not content:
            return content

        import re

        # Pattern to match different forms of think tags (opening and closing)
        # Matches: <think>...</think>, <think>...</think>, ＜think＞...＜/think＞, 【think】...【/think】
        # Also handles self-closing and nested tags
        patterns = [
            r'<think[\s\S]*?></think>',           # <think>...</think>
        ]

        # Apply all patterns
        filtered_content = content
        for pattern in patterns:
            filtered_content = re.sub(pattern, '', filtered_content, flags=re.IGNORECASE)

        # # Clean up any extra whitespace that might be left behind
        # # Remove multiple consecutive empty lines
        # filtered_content = re.sub(r'\n\s*\n\s*\n\s*\n', '', filtered_content)

        # # Remove empty lines at the beginning and end
        # filtered_content = filtered_content.strip()

        # # Clean up extra spaces within lines
        # filtered_content = re.sub(r' +', ' ', filtered_content)

        return filtered_content
    
    async def chat_completion(self, messages: List[AIMessage], **kwargs) -> AIResponse:
        """Generate chat completion using OpenAI"""
        if not self.client:
            raise RuntimeError("OpenAI client not available")

        config = self._merge_config(**kwargs)

        # Convert messages to OpenAI format with multimodal support
        openai_messages = [
            self._convert_message_to_openai(msg)
            for msg in messages
        ]
        
        try:
            response = await self.client.chat.completions.create(
                model=config.get("model", self.model),
                messages=openai_messages,
                # max_tokens=config.get("max_tokens", 2000),
                temperature=config.get("temperature", 0.7),
                top_p=config.get("top_p", 1.0)
            )
            
            choice = response.choices[0]
            # Filter out think content from the response
            filtered_content = self._filter_think_content(choice.message.content)

            return AIResponse(
                content=filtered_content,
                model=response.model,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                finish_reason=choice.finish_reason,
                metadata={"provider": "openai"}
            )
            
        except Exception as e:
            # 提供更详细的错误信息
            error_msg = str(e)
            if "Expecting value" in error_msg:
                logger.error(f"OpenAI API JSON parsing error: {error_msg}. This usually indicates the API returned malformed JSON.")
            elif "timeout" in error_msg.lower():
                logger.error(f"OpenAI API timeout error: {error_msg}")
            elif "rate limit" in error_msg.lower():
                logger.error(f"OpenAI API rate limit error: {error_msg}")
            else:
                logger.error(f"OpenAI API error: {error_msg}")
            raise
    
    async def text_completion(self, prompt: str, **kwargs) -> AIResponse:
        """Generate text completion using OpenAI chat format"""
        messages = [AIMessage(role=MessageRole.USER, content=prompt)]
        return await self.chat_completion(messages, **kwargs)

    async def stream_chat_completion(self, messages: List[AIMessage], **kwargs) -> AsyncGenerator[str, None]:
        """Stream chat completion using OpenAI with think tag filtering"""
        if not self.client:
            raise RuntimeError("OpenAI client not available")

        config = self._merge_config(**kwargs)

        # Convert messages to OpenAI format with multimodal support
        openai_messages = [
            self._convert_message_to_openai(msg)
            for msg in messages
        ]

        try:
            stream = await self.client.chat.completions.create(
                model=config.get("model", self.model),
                messages=openai_messages,
                # max_tokens=config.get("max_tokens", 2000),
                temperature=config.get("temperature", 0.7),
                top_p=config.get("top_p", 1.0),
                stream=True
            )

            buffer = ""
            in_think_tag = False

            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    chunk_content = chunk.choices[0].delta.content
                    buffer += chunk_content

                    # Process the buffer to handle think tags
                    processed_content = ""
                    remaining_buffer = buffer

                    while remaining_buffer:
                        if not in_think_tag:
                            # Look for opening think tag
                            think_start = None
                            # Check for different forms of think tags (case-insensitive)
                            for tag in ['<think', '<think>', '＜think', '【think']:
                                pos = remaining_buffer.lower().find(tag.lower())
                                if pos != -1:
                                    think_start = pos
                                    break

                            if think_start is not None:
                                # Found opening tag, add content before it
                                processed_content += remaining_buffer[:think_start]
                                in_think_tag = True
                                # Remove everything up to and including the opening tag
                                remaining_buffer = remaining_buffer[think_start:]
                                # Find the end of the opening tag
                                tag_end = remaining_buffer.lower().find('>')
                                if tag_end != -1:
                                    remaining_buffer = remaining_buffer[tag_end + 1:]
                                else:
                                    remaining_buffer = ""
                                    break
                            else:
                                # No think tag found, add everything to processed content
                                processed_content += remaining_buffer
                                remaining_buffer = ""
                                break
                        else:
                            # We're inside a think tag, look for closing tag
                            think_end = None
                            # Check for different forms of closing tags (case-insensitive)
                            for tag in ['</think>', '</think>', '＜/think＞', '【/think】']:
                                pos = remaining_buffer.lower().find(tag.lower())
                                if pos != -1:
                                    think_end = pos
                                    break

                            if think_end is not None:
                                # Found closing tag, skip to after it
                                in_think_tag = False
                                remaining_buffer = remaining_buffer[think_end + len('</think>'):]
                            else:
                                # Haven't found closing tag yet, skip this chunk
                                remaining_buffer = ""

                    # Update buffer with remaining content
                    buffer = remaining_buffer

                    # Yield processed content if not in think tag
                    if not in_think_tag and processed_content:
                        yield processed_content

        except Exception as e:
            logger.error(f"OpenAI streaming error: {e}")
            raise

    async def stream_text_completion(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """Stream text completion using OpenAI chat format"""
        messages = [AIMessage(role=MessageRole.USER, content=prompt)]
        async for chunk in self.stream_chat_completion(messages, **kwargs):
            yield chunk



class GoogleProvider(AIProvider):
    """Google Gemini API provider"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        try:
            import google.generativeai as genai

            # Configure the API key
            genai.configure(api_key=config.get("api_key"))

            # Store base_url for potential future use or proxy configurations
            self.base_url = config.get("base_url", "https://generativelanguage.googleapis.com")

            self.client = genai
            self.model_instance = genai.GenerativeModel(config.get("model", "gemini-1.5-flash"))
        except ImportError:
            logger.warning("Google Generative AI library not installed. Install with: pip install google-generativeai")
            self.client = None
            self.model_instance = None

    def _convert_messages_to_gemini(self, messages: List[AIMessage]):
        """Convert AIMessage list to Gemini format, supporting multimodal content"""
        import google.generativeai as genai
        import base64

        # Try to import genai types for proper image handling
        try:
            from google.genai import types
            GENAI_TYPES_AVAILABLE = True
        except ImportError:
            try:
                # Fallback to older API structure
                from google.generativeai import types
                GENAI_TYPES_AVAILABLE = True
            except ImportError:
                logger.warning("Google GenAI types not available for proper image processing")
                GENAI_TYPES_AVAILABLE = False

        # Check if we have any images
        has_images = any(
            isinstance(msg.content, list) and
            any(isinstance(part, ImageContent) for part in msg.content)
            for msg in messages
        )

        if not has_images:
            # Text-only mode - return string
            parts = []
            for msg in messages:
                role_prefix = f"[{msg.role.value.upper()}]: "
                if isinstance(msg.content, str):
                    parts.append(role_prefix + msg.content)
                elif isinstance(msg.content, list):
                    message_parts = [role_prefix]
                    for part in msg.content:
                        if isinstance(part, TextContent):
                            message_parts.append(part.text)
                    parts.append(" ".join(message_parts))
                else:
                    parts.append(role_prefix + str(msg.content))
            return "\n\n".join(parts)
        else:
            # Multimodal mode - return list of parts for Gemini
            content_parts = []

            for msg in messages:
                role_prefix = f"[{msg.role.value.upper()}]: "

                if isinstance(msg.content, str):
                    content_parts.append(role_prefix + msg.content)
                elif isinstance(msg.content, list):
                    text_parts = [role_prefix]

                    for part in msg.content:
                        if isinstance(part, TextContent):
                            text_parts.append(part.text)
                        elif isinstance(part, ImageContent):
                            # Add accumulated text first
                            if len(text_parts) > 1 or text_parts[0]:
                                content_parts.append(" ".join(text_parts))
                                text_parts = []

                            # Process image for Gemini
                            image_url = part.image_url.get("url", "")
                            if image_url.startswith("data:image/") and GENAI_TYPES_AVAILABLE:
                                try:
                                    # Extract base64 data and mime type
                                    header, base64_data = image_url.split(",", 1)
                                    mime_type = header.split(":")[1].split(";")[0]  # Extract mime type like 'image/jpeg'
                                    image_data = base64.b64decode(base64_data)

                                    # Create Gemini-compatible part from base64 image data
                                    image_part = None
                                    if GENAI_TYPES_AVAILABLE:
                                        if hasattr(types, 'Part') and hasattr(types.Part, 'from_bytes'):
                                            image_part = types.Part.from_bytes(
                                                data=image_data,
                                                mime_type=mime_type
                                            )
                                        elif hasattr(types, 'to_part'):
                                            image_part = types.to_part({
                                                'inline_data': {
                                                    'mime_type': mime_type,
                                                    'data': image_data
                                                }
                                            })
                                    if image_part is None:
                                        image_part = {
                                            'inline_data': {
                                                'mime_type': mime_type,
                                                'data': image_data
                                            }
                                        }
                                    content_parts.append(image_part)
                                    logger.info(f"Successfully processed image for Gemini: {mime_type}, {len(image_data)} bytes")
                                except Exception as e:
                                    logger.error(f"Failed to process image for Gemini: {e}")
                                    content_parts.append("请参考上传的图片进行设计。图片包含了重要的设计参考信息，请根据图片的风格、色彩、布局等元素来生成模板。")
                            else:
                                # Fallback when genai types not available or not base64 image
                                if image_url.startswith("data:image/"):
                                    content_parts.append("请参考上传的图片进行设计。图片包含了重要的设计参考信息，请根据图片的风格、色彩、布局等元素来生成模板。")
                                else:
                                    content_parts.append(f"请参考图片 {image_url} 进行设计")

                    # Add remaining text
                    if len(text_parts) > 1 or (len(text_parts) == 1 and text_parts[0]):
                        content_parts.append(" ".join(text_parts))
                else:
                    content_parts.append(role_prefix + str(msg.content))

            return content_parts

    async def chat_completion(self, messages: List[AIMessage], **kwargs) -> AIResponse:
        """Generate chat completion using Google Gemini"""
        if not self.client or not self.model_instance:
            raise RuntimeError("Google Gemini client not available")

        config = self._merge_config(**kwargs)

        # Convert messages to Gemini format with multimodal support
        prompt = self._convert_messages_to_gemini(messages)

        try:
            # Configure generation parameters
            # 确保max_tokens不会太小，至少1000个token用于生成内容
            max_tokens = max(config.get("max_tokens", 16384), 1000)
            generation_config = {
                "temperature": config.get("temperature", 0.7),
                "top_p": config.get("top_p", 1.0),
                # "max_output_tokens": max_tokens,
            }

            # 配置安全设置 - 设置为较宽松的安全级别以减少误拦截
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_ONLY_HIGH"
                }
            ]


            response = await self._generate_async(prompt, generation_config, safety_settings)
            logger.debug(f"Google Gemini API response: {response}")

            # 检查响应状态和安全过滤
            finish_reason = "stop"
            content = ""

            if response.candidates:
                candidate = response.candidates[0]
                finish_reason = candidate.finish_reason.name if hasattr(candidate.finish_reason, 'name') else str(candidate.finish_reason)

                # 检查是否被安全过滤器阻止或其他问题
                if finish_reason == "SAFETY":
                    logger.warning("Content was blocked by safety filters")
                    content = "[内容被安全过滤器阻止]"
                elif finish_reason == "RECITATION":
                    logger.warning("Content was blocked due to recitation")
                    content = "[内容因重复而被阻止]"
                elif finish_reason == "MAX_TOKENS":
                    logger.warning("Response was truncated due to max tokens limit")
                    # 尝试获取部分内容
                    try:
                        if hasattr(candidate, 'content') and candidate.content and hasattr(candidate.content, 'parts') and candidate.content.parts:
                            content = candidate.content.parts[0].text if candidate.content.parts[0].text else "[响应因token限制被截断，无内容]"
                        else:
                            content = "[响应因token限制被截断，无内容]"
                    except Exception as text_error:
                        logger.warning(f"Failed to get truncated response text: {text_error}")
                        content = "[响应因token限制被截断，无法获取内容]"
                elif finish_reason == "OTHER":
                    logger.warning("Content was blocked for other reasons")
                    content = "[内容被其他原因阻止]"
                else:
                    # 正常情况下获取文本
                    try:
                        if hasattr(candidate, 'content') and candidate.content and hasattr(candidate.content, 'parts') and candidate.content.parts:
                            content = candidate.content.parts[0].text if candidate.content.parts[0].text else ""
                        else:
                            # 回退到response.text
                            content = response.text if hasattr(response, 'text') and response.text else ""
                    except Exception as text_error:
                        logger.warning(f"Failed to get response text: {text_error}")
                        content = "[无法获取响应内容]"
            else:
                logger.warning("No candidates in response")
                content = "[响应中没有候选内容]"

            return AIResponse(
                content=content,
                model=self.model,
                usage={
                    "prompt_tokens": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else 0,
                    "completion_tokens": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else 0,
                    "total_tokens": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0
                },
                finish_reason=finish_reason,
                metadata={"provider": "google"}
            )

        except Exception as e:
            logger.error(f"Google Gemini API error: {e}")
            raise

    async def _generate_async(self, prompt, generation_config: Dict[str, Any], safety_settings=None):
        """Async wrapper for Gemini generation - supports both text and multimodal content"""
        import asyncio
        loop = asyncio.get_event_loop()

        def _generate_sync():
            kwargs = {
                "generation_config": generation_config
            }
            if safety_settings:
                kwargs["safety_settings"] = safety_settings

            return self.model_instance.generate_content(
                prompt,  # Can be string or list of parts
                **kwargs
            )

        return await loop.run_in_executor(None, _generate_sync)

    async def text_completion(self, prompt: str, **kwargs) -> AIResponse:
        """Generate text completion using Google Gemini"""
        messages = [AIMessage(role=MessageRole.USER, content=prompt)]
        return await self.chat_completion(messages, **kwargs)



class AIProviderFactory:
    """Factory for creating AI providers"""

    _providers = {
        "openai": OpenAIProvider,
        "google": GoogleProvider,
        "gemini": GoogleProvider,  # Alias for google
    }

    @classmethod
    def create_provider(cls, provider_name: str, config: Optional[Dict[str, Any]] = None) -> AIProvider:
        """Create an AI provider instance"""
        if config is None:
            config = ai_config.get_provider_config(provider_name)

        # Built-in providers
        if provider_name not in cls._providers:
            raise ValueError(f"Unknown provider: {provider_name}")

        provider_class = cls._providers[provider_name]
        return provider_class(config)
    
    @classmethod
    def get_available_providers(cls) -> List[str]:
        """Get list of available providers"""
        return list(cls._providers.keys())

class AIProviderManager:
    """Manager for AI provider instances with caching and reloading"""

    def __init__(self):
        self._provider_cache = {}
        self._config_cache = {}

    def get_provider(self, provider_name: Optional[str] = None) -> AIProvider:
        """Get AI provider instance with caching"""
        if provider_name is None:
            provider_name = ai_config.default_ai_provider

        # Get current config for the provider
        current_config = ai_config.get_provider_config(provider_name)

        # Check if we have a cached provider and if config has changed
        cache_key = provider_name
        if (cache_key in self._provider_cache and
            cache_key in self._config_cache and
            self._config_cache[cache_key] == current_config):
            return self._provider_cache[cache_key]

        # Create new provider instance
        provider = AIProviderFactory.create_provider(provider_name, current_config)

        # Cache the provider and config
        self._provider_cache[cache_key] = provider
        self._config_cache[cache_key] = current_config

        return provider

    def clear_cache(self):
        """Clear provider cache to force reload"""
        self._provider_cache.clear()
        self._config_cache.clear()

    def reload_provider(self, provider_name: str):
        """Reload a specific provider"""
        cache_key = provider_name
        if cache_key in self._provider_cache:
            del self._provider_cache[cache_key]
        if cache_key in self._config_cache:
            del self._config_cache[cache_key]

# Global provider manager
_provider_manager = AIProviderManager()

def get_ai_provider(provider_name: Optional[str] = None) -> AIProvider:
    """Get AI provider instance"""
    return _provider_manager.get_provider(provider_name)


def get_role_provider(role: str, provider_override: Optional[str] = None) -> Tuple[AIProvider, Dict[str, Optional[str]]]:
    """Get provider and settings for a specific task role"""
    settings = ai_config.get_model_config_for_role(role, provider_override=provider_override)
    provider = get_ai_provider(settings["provider"])
    return provider, settings

def reload_ai_providers():
    """Reload all AI providers (clear cache)"""
    _provider_manager.clear_cache()
