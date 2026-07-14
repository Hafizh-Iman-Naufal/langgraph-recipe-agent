"""Tests for recipe agent graph."""
import pytest
from recipe_agent.graph import create_recipe_graph, route_after_decide_task, route_after_critique_recommendations, should_continue_revising
from recipe_agent.state import RecipeState


def test_graph_creation():
    """Test that the graph can be created."""
    graph = create_recipe_graph()
    assert graph is not None
    
    # Check nodes exist
    nodes = list(graph.get_graph().nodes)
    assert "parse_input" in nodes
    assert "decide_task" in nodes
    assert "generate_recommendations" in nodes
    assert "critique_recommendations" in nodes
    assert "select_best_recommendation" in nodes
    assert "generate_recipe" in nodes
    assert "critique_recipe" in nodes
    assert "revise_recipe" in nodes
    assert "fetch_youtube_videos" in nodes
    assert "render_output" in nodes


def test_route_after_decide_task():
    """Test routing after decide_task."""
    # Test recommendations_only
    state = {"task_type": "recommendations_only"}
    assert route_after_decide_task(state) == "generate_recommendations"
    
    # Test recipe_only
    state = {"task_type": "recipe_only"}
    assert route_after_decide_task(state) == "generate_recipe"
    
    # Test recommend_then_recipe
    state = {"task_type": "recommend_then_recipe"}
    assert route_after_decide_task(state) == "generate_recommendations"
    
    # Test clarification_needed
    state = {"task_type": "clarification_needed"}
    assert route_after_decide_task(state) == "render_output"


def test_route_after_critique_recommendations():
    """Test routing after critique_recommendations."""
    # Test recommendations_only -> render
    state = {"task_type": "recommendations_only"}
    assert route_after_critique_recommendations(state) == "render_output"
    
    # Test recommend_then_recipe -> select_best
    state = {"task_type": "recommend_then_recipe"}
    assert route_after_critique_recommendations(state) == "select_best_recommendation"


def test_should_continue_revising():
    """Test revision logic."""
    # Test passed critique
    state = {
        "critique_passed": True,
        "revision_count": 0,
        "max_revisions": 3
    }
    assert should_continue_revising(state) == "fetch_youtube"
    
    # Test max revisions reached
    state = {
        "critique_passed": False,
        "revision_count": 3,
        "max_revisions": 3
    }
    assert should_continue_revising(state) == "fetch_youtube"
    
    # Test should revise
    state = {
        "critique_passed": False,
        "revision_count": 1,
        "max_revisions": 3
    }
    assert should_continue_revising(state) == "revise"


def test_language_detection():
    """Test language detection."""
    from recipe_agent.tools.language import detect_language
    
    assert detect_language("I want a simple recipe") == "en"
    assert detect_language("Saya mau makanan simple") == "id"
    assert detect_language("Quick dinner ideas") == "en"
    assert detect_language("Resep sarapan yang cepat") == "id"


def test_ingredient_store():
    """Test ingredient store loading."""
    from recipe_agent.tools.ingredient_store import load_ingredient_store, get_all_ingredients
    
    store = load_ingredient_store()
    assert isinstance(store, dict)
    assert "carbs" in store
    assert "protein" in store
    
    ingredients = get_all_ingredients()
    assert isinstance(ingredients, list)
    assert len(ingredients) > 0
    assert "telur" in ingredients
    assert "mie instan" in ingredients
