"""Configuration loader for recipe agent."""
import os
from pathlib import Path
from dotenv import load_dotenv


def load_config():
    """Load configuration from .env file and environment variables."""
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    
    return {
        "llm_provider": os.getenv("LLM_PROVIDER", "google"),
        "llm_model": os.getenv("LLM_MODEL", "gemini-2.5-flash-lite"),
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "google_api_key": os.getenv("GOOGLE_API_KEY"),
        "gemini_api_key": os.getenv("GEMINI_API_KEY"),
        "youtube_api_key": os.getenv("YOUTUBE_API_KEY", ""),
        "default_language": os.getenv("DEFAULT_LANGUAGE", "auto"),
        "default_output_mode": os.getenv("DEFAULT_OUTPUT_MODE", "print"),
        "default_task_type": os.getenv("DEFAULT_TASK_TYPE", "recommend_then_recipe"),
        "default_recommendation_count": int(os.getenv("DEFAULT_RECOMMENDATION_COUNT", "10")),
        "default_max_revisions": int(os.getenv("DEFAULT_MAX_REVISIONS", "3")),
        "default_approval_threshold": float(os.getenv("DEFAULT_APPROVAL_THRESHOLD", "0.85")),
        "default_recommendation_threshold": float(os.getenv("DEFAULT_RECOMMENDATION_THRESHOLD", "0.80")),
        "default_include_video_urls": os.getenv("DEFAULT_INCLUDE_VIDEO_URLS", "false").lower() == "true",
        "default_max_video_urls": int(os.getenv("DEFAULT_MAX_VIDEO_URLS", "5")),
    }


def validate_config(config):
    """Validate required configuration based on LLM provider."""
    provider = (config.get("llm_provider") or "google").lower()
    
    if provider in ("google", "gemini"):
        api_key = config.get("google_api_key") or config.get("gemini_api_key")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY (or GEMINI_API_KEY) is required. "
                "Set it in .env file or environment."
            )
    elif provider == "openai":
        if not config.get("openai_api_key"):
            raise ValueError(
                "OPENAI_API_KEY is required when using OpenAI. "
                "Set it in .env file or environment."
            )
    else:
        raise ValueError(
            f"Unsupported LLM_PROVIDER: {provider}. Use 'google' or 'openai'."
        )
    
    return True


def is_youtube_enabled(config: dict) -> bool:
    """Check if YouTube integration is enabled."""
    return bool(config.get("youtube_api_key"))
