"""State schema for recipe recommendation agent."""
from typing import Literal, TypedDict, Optional


TaskType = Literal[
    "recommendations_only",
    "recipe_only",
    "recommend_then_recipe",
    "clarification_needed",
]


class RecipeState(TypedDict):
    """State that flows through the recipe recommendation graph."""
    
    # User input
    user_request: str
    language: Literal["auto", "en", "id"]
    output_language: Optional[Literal["en", "id"]]
    output_mode: Literal["print", "markdown"]
    
    # Task routing
    task_type: Optional[TaskType]
    
    # Recommendations
    recommendation_count: int
    recommendations: list[dict]
    recommendation_critique_score: float
    recommendation_critique_notes: list[str]
    
    # YouTube integration
    include_video_urls: bool
    max_video_urls: int
    
    # Parsed constraints and search
    constraints: dict
    search_queries: list[str]
    
    # Recipe candidates
    recipe_candidates: list[dict]
    selected_recommendation: Optional[dict]
    selected_recipe: Optional[dict]
    draft_recipe: Optional[str]
    
    # Critique and revision
    critique_score: float
    critique_passed: bool
    critique_notes: list[str]
    revision_instructions: list[str]
    revision_count: int
    max_revisions: int
    approval_threshold: float
    
    # YouTube results
    video_urls: list[dict]
    
    # Output
    final_output: Optional[str]
    output_path: Optional[str]
    errors: list[str]
    warnings: list[str]
