"""Tests for YouTube optional behavior."""
import pytest
from recipe_agent.config import is_youtube_enabled


def test_youtube_disabled_no_api_key():
    """Test YouTube is disabled without API key."""
    config = {
        "youtube_api_key": ""
    }
    assert is_youtube_enabled(config) is False


def test_youtube_disabled_with_api_key():
    """Test YouTube is enabled with API key."""
    config = {
        "youtube_api_key": "test_key"
    }
    assert is_youtube_enabled(config) is True


def test_youtube_search_returns_none_without_key():
    """Test YouTube search returns None without API key."""
    from recipe_agent.tools.youtube_search import search_youtube_videos
    
    # This would need mocking of the config, but we can test the logic
    # In a real test, you'd mock load_config to return empty youtube_api_key
    pass
