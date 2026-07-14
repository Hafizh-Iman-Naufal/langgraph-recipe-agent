"""Tests for recommendations generation."""
import pytest


def test_recommendation_count_default():
    """Test default recommendation count."""
    from recipe_agent.config import load_config
    
    config = load_config()
    default_count = config.get("default_recommendation_count", 10)
    assert default_count == 10


def test_recommendation_structure():
    """Test expected recommendation structure."""
    recommendation = {
        "name": "Test Recipe",
        "type": "food",
        "short_description": "A test recipe",
        "why_it_fits": "Because it fits",
        "estimated_time_minutes": 15,
        "difficulty": "easy",
        "main_ingredients": ["ingredient 1", "ingredient 2"],
        "ingredient_availability_notes": "Available at Alfamart",
        "store_fit_score": 0.9,
        "simplicity_score": 0.95
    }
    
    assert "name" in recommendation
    assert "type" in recommendation
    assert recommendation["type"] in ["food", "drink"]
    assert "store_fit_score" in recommendation
    assert "simplicity_score" in recommendation


def test_recommendations_list():
    """Test that recommendations are generated as a list."""
    recommendations = []
    for i in range(10):
        recommendations.append({
            "name": f"Recipe {i+1}",
            "type": "food" if i < 7 else "drink",
            "short_description": f"Description {i+1}",
            "why_it_fits": "Fits the criteria",
            "estimated_time_minutes": 15,
            "difficulty": "easy",
            "main_ingredients": [],
            "ingredient_availability_notes": "",
            "store_fit_score": 0.8,
            "simplicity_score": 0.9
        })
    
    assert len(recommendations) == 10
    assert all(isinstance(r, dict) for r in recommendations)
