"""Tests for markdown writer."""
import pytest
from recipe_agent.tools.markdown_writer import (
    render_recommendations_markdown,
    render_recommend_then_recipe_markdown,
    render_recipe_only_markdown,
    render_markdown
)


def test_render_english_recommendations():
    """Test rendering English recommendations."""
    recommendations = [
        {
            "name": "Simple Egg Noodles",
            "type": "food",
            "why_it_fits": "Quick and easy",
            "estimated_time_minutes": 15
        }
    ]
    
    state = {"output_language": "en", "task_type": "recommendations_only"}
    output = render_recommendations_markdown(recommendations, state)
    
    assert "# Food and Drink Recommendations" in output
    assert "Simple Egg Noodles" in output
    assert "15 minutes" in output


def test_render_indonesian_recommendations():
    """Test rendering Indonesian recommendations."""
    recommendations = [
        {
            "name": "Mie Telur Simple",
            "type": "food",
            "why_it_fits": "Cepat dan mudah",
            "estimated_time_minutes": 15
        }
    ]
    
    state = {"output_language": "id", "task_type": "recommendations_only"}
    output = render_recommendations_markdown(recommendations, state)
    
    assert "# Rekomendasi Makanan dan Minuman" in output
    assert "Mie Telur Simple" in output
    assert "15 menit" in output


def test_render_recommend_then_recipe():
    """Test rendering recommendations + recipe."""
    recommendations = [
        {"name": "Recipe 1"},
        {"name": "Recipe 2"}
    ]
    
    selected_recommendation = {
        "name": "Recipe 1",
        "reason_selected": "Best match"
    }
    
    recipe = {
        "title": "Full Recipe",
        "description": "A complete recipe",
        "ingredients": [{"item": "egg", "amount": "1", "unit": ""}],
        "steps": ["Step 1", "Step 2"],
        "prep_time_minutes": 5,
        "cook_time_minutes": 10,
        "total_time_minutes": 15,
        "difficulty": "easy",
        "substitutions": [],
        "tips": []
    }
    
    state = {"output_language": "en", "task_type": "recommend_then_recipe"}
    output = render_recommend_then_recipe_markdown(
        recommendations, selected_recommendation, recipe, [], state
    )
    
    assert "# Best Recommendation: Recipe 1" in output
    assert "## Why This Was Selected" in output
    assert "## Recommendation Shortlist" in output
    assert "## Full Recipe" in output


def test_render_recipe_only():
    """Test rendering single recipe."""
    recipe = {
        "title": "Simple Recipe",
        "description": "A simple recipe",
        "ingredients": [],
        "steps": [],
        "prep_time_minutes": 5,
        "cook_time_minutes": 10,
        "total_time_minutes": 15,
        "difficulty": "easy",
        "substitutions": [],
        "tips": []
    }
    
    state = {"output_language": "en", "task_type": "recipe_only"}
    output = render_recipe_only_markdown(recipe, [], state)
    
    assert "# Simple Recipe" in output
    assert "## Why This Recipe Fits" in output


def test_render_markdown_routing():
    """Test that render_markdown routes correctly."""
    recipe = {"title": "Test"}
    videos = []
    
    # Test recommendations_only
    state = {
        "task_type": "recommendations_only",
        "output_language": "en",
        "recommendations": [{"name": "Rec 1", "type": "food", "estimated_time_minutes": 10}]
    }
    output = render_markdown(recipe, videos, state)
    assert "Recommendations" in output
    
    # Test recipe_only
    state = {
        "task_type": "recipe_only",
        "output_language": "en",
        "recommendations": []
    }
    recipe = {
        "title": "Recipe",
        "description": "Test",
        "ingredients": [],
        "steps": [],
        "prep_time_minutes": 5,
        "cook_time_minutes": 10,
        "total_time_minutes": 15,
        "difficulty": "easy"
    }
    output = render_markdown(recipe, videos, state)
    assert "# Recipe" in output
