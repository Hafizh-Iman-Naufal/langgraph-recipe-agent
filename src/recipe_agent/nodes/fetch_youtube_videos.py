"""Fetch YouTube videos node."""
from ..state import RecipeState
from ..config import load_config, is_youtube_enabled
from ..tools.youtube_search import search_youtube_videos


def fetch_youtube_videos(state: RecipeState) -> RecipeState:
    """Fetch YouTube video recommendations if enabled."""
    config = load_config()
    
    # Check if YouTube is enabled
    if not state.get("include_video_urls"):
        return {
            **state,
            "video_urls": []
        }
    
    if not is_youtube_enabled(config):
        state["warnings"].append("YouTube API key not configured. Skipping video recommendations.")
        return {
            **state,
            "video_urls": []
        }
    
    # Get recipe title for search
    draft_recipe = state.get("draft_recipe", {})
    recipe_title = draft_recipe.get("title", "recipe")
    output_language = state.get("output_language", "en")
    
    # Search YouTube
    max_videos = state.get("max_video_urls", 5)
    videos = search_youtube_videos(recipe_title, output_language, max_videos)
    
    return {
        **state,
        "video_urls": videos if videos else []
    }
