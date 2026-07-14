"""LangGraph workflow definition for recipe agent."""
from typing import Literal
from langgraph.graph import StateGraph, END
from .state import RecipeState
from .config import load_config, is_youtube_enabled
from .nodes.parse_input import parse_input
from .nodes.decide_task import decide_task
from .nodes.generate_recommendations import generate_recommendations
from .nodes.critique_recommendations import critique_recommendations
from .nodes.select_best_recommendation import select_best_recommendation
from .nodes.generate_recipe import generate_recipe
from .nodes.critique_recipe import critique_recipe
from .nodes.revise_recipe import revise_recipe
from .nodes.fetch_youtube_videos import fetch_youtube_videos
from .nodes.render_output import render_output


def route_after_decide_task(state: RecipeState) -> Literal["generate_recommendations", "generate_recipe", "render_output"]:
    """Route based on task_type decision."""
    task_type = state.get("task_type", "recommend_then_recipe")
    
    if task_type == "recommendations_only":
        return "generate_recommendations"
    elif task_type == "recipe_only":
        return "generate_recipe"
    elif task_type == "recommend_then_recipe":
        return "generate_recommendations"
    else:  # clarification_needed or unknown
        return "render_output"


def route_after_critique_recommendations(state: RecipeState) -> Literal["select_best_recommendation", "render_output"]:
    """Route after critique_recommendations based on task_type."""
    task_type = state.get("task_type", "recommend_then_recipe")
    
    if task_type == "recommendations_only":
        return "render_output"
    elif task_type == "recommend_then_recipe":
        return "select_best_recommendation"
    else:
        return "render_output"


def should_continue_revising(state: RecipeState) -> Literal["revise", "fetch_youtube"]:
    """Determine if we should revise or move to YouTube/output."""
    if state["critique_passed"]:
        return "fetch_youtube"
    
    if state["revision_count"] >= state["max_revisions"]:
        return "fetch_youtube"
    
    return "revise"


def create_recipe_graph():
    """Create and compile the recipe recommendation graph."""
    
    workflow = StateGraph(RecipeState)
    
    # Add nodes
    workflow.add_node("parse_input", parse_input)
    workflow.add_node("decide_task", decide_task)
    workflow.add_node("generate_recommendations", generate_recommendations)
    workflow.add_node("critique_recommendations", critique_recommendations)
    workflow.add_node("select_best_recommendation", select_best_recommendation)
    workflow.add_node("generate_recipe", generate_recipe)
    workflow.add_node("critique_recipe", critique_recipe)
    workflow.add_node("revise_recipe", revise_recipe)
    workflow.add_node("fetch_youtube_videos", fetch_youtube_videos)
    workflow.add_node("render_output", render_output)
    
    # Set entry point
    workflow.set_entry_point("parse_input")
    
    # parse_input -> decide_task
    workflow.add_edge("parse_input", "decide_task")
    
    # Route based on task_type
    workflow.add_conditional_edges(
        "decide_task",
        route_after_decide_task,
        {
            "generate_recommendations": "generate_recommendations",
            "generate_recipe": "generate_recipe",
            "render_output": "render_output"
        }
    )
    
    # After generating recommendations, critique them
    workflow.add_edge("generate_recommendations", "critique_recommendations")
    
    # Route after critique: select best (recommend_then_recipe) or render (recommendations_only)
    workflow.add_conditional_edges(
        "critique_recommendations",
        route_after_critique_recommendations,
        {
            "select_best_recommendation": "select_best_recommendation",
            "render_output": "render_output"
        }
    )
    
    # After selecting best recommendation, generate recipe
    workflow.add_edge("select_best_recommendation", "generate_recipe")
    
    # After generating recipe, critique it
    workflow.add_edge("generate_recipe", "critique_recipe")
    
    # Conditional edge for revision loop or proceed to YouTube/output
    workflow.add_conditional_edges(
        "critique_recipe",
        should_continue_revising,
        {
            "revise": "revise_recipe",
            "fetch_youtube": "fetch_youtube_videos"
        }
    )
    
    # revise -> critique (loop)
    workflow.add_edge("revise_recipe", "critique_recipe")
    
    # fetch_youtube_videos -> render_output (always proceeds)
    workflow.add_edge("fetch_youtube_videos", "render_output")
    
    # render_output -> END
    workflow.add_edge("render_output", END)
    
    # Compile graph
    return workflow.compile()
