"""LLM wrapper for consistent model access.

Supports OpenAI (gpt-4o-mini) and Google Gemini (gemini-2.5-flash-lite).
Both return a LangChain BaseChatModel, so all nodes work identically.
"""
from typing import Union
from langchain_core.language_models.chat_models import BaseChatModel
from ..config import load_config


def get_llm(config: dict, temperature: float = 0.7) -> BaseChatModel:
    """Get configured LLM instance based on LLM_PROVIDER in config.

    Supported providers:
      - "google" / "gemini" -> Google Gemini (default: gemini-2.5-flash-lite)
      - "openai"            -> OpenAI ChatGPT
    """
    provider = (config.get("llm_provider") or "google").lower()

    if provider in ("google", "gemini"):
        from langchain_google_genai import ChatGoogleGenerativeAI

        model = config.get("llm_model", "gemini-2.5-flash-lite")
        api_key = config.get("google_api_key") or config.get("gemini_api_key")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY (or GEMINI_API_KEY) is required when LLM_PROVIDER=google. "
                "Set it in .env or export it in your shell."
            )
        return ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            google_api_key=api_key,
        )

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        model = config.get("llm_model", "gpt-4o-mini")
        api_key = config.get("openai_api_key")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is required when LLM_PROVIDER=openai. "
                "Set it in .env or export it in your shell."
            )
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            openai_api_key=api_key,
        )

    raise ValueError(
        f"Unsupported LLM_PROVIDER: {provider!r}. "
        "Use 'google'/'gemini' or 'openai'."
    )
