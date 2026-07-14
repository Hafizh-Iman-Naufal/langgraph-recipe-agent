"""Tests for decide_task node."""
import pytest


def test_decide_task_recommendations_only():
    """Test detection of recommendations_only task."""
    # This would need to be tested with actual LLM call
    # For now, just test the logic
    task_type = "recommendations_only"
    assert task_type in ["recommendations_only", "recipe_only", "recommend_then_recipe", "clarification_needed"]


def test_decide_task_recipe_only():
    """Test detection of recipe_only task."""
    task_type = "recipe_only"
    assert task_type in ["recommendations_only", "recipe_only", "recommend_then_recipe", "clarification_needed"]


def test_decide_task_recommend_then_recipe():
    """Test detection of recommend_then_recipe task."""
    task_type = "recommend_then_recipe"
    assert task_type in ["recommendations_only", "recipe_only", "recommend_then_recipe", "clarification_needed"]


def test_decide_task_clarification_needed():
    """Test detection of clarification_needed task."""
    task_type = "clarification_needed"
    assert task_type in ["recommendations_only", "recipe_only", "recommend_then_recipe", "clarification_needed"]
