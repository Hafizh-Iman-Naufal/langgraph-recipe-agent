"""YouTube Data API v3 client for video recommendations."""
import requests
from typing import List, Dict, Optional
from ..config import load_config, is_youtube_enabled


def search_youtube_videos(recipe_title: str, language: str = "en", max_results: int = 5) -> Optional[List[Dict[str, str]]]:
    """
    Search YouTube for recipe videos.
    
    Returns None if API key is missing or request fails.
    """
    config = load_config()
    api_key = config.get("youtube_api_key")
    
    if not api_key:
        return None
    
    # Build search query based on language
    if language == "id":
        queries = [
            f"resep {recipe_title} simple shorts",
            f"resep {recipe_title} mudah",
            f"{recipe_title} recipe shorts"
        ]
    else:
        queries = [
            f"{recipe_title} recipe shorts",
            f"{recipe_title} easy recipe",
            f"{recipe_title} simple recipe"
        ]
    
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": queries[0],
            "type": "video",
            "videoDuration": "short",
            "maxResults": max_results,
            "key": api_key,
            "order": "relevance"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        videos = []
        
        for item in data.get("items", []):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            channel = item["snippet"]["channelTitle"]
            
            videos.append({
                "title": title,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "shorts_url": f"https://www.youtube.com/shorts/{video_id}",
                "channel": channel
            })
        
        return videos if videos else None
        
    except Exception as e:
        print(f"Warning: YouTube API request failed: {e}")
        return None
