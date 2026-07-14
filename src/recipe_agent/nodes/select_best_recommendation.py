"""Select best recommendation node."""
import json
from langchain_core.messages import HumanMessage, SystemMessage
from ..state import RecipeState
from ..config import load_config
from ..tools.llm import get_llm
from pathlib import Path


def load_prompt():
    """Load select_best_recommendation prompt template."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "select_best_recommendation.md"
    return prompt_path.read_text(encoding="utf-8")


def select_best_recommendation(state: RecipeState) -> RecipeState:
    """Select the best recommendation to turn into a recipe."""
    user_request = state["user_request"]
    constraints = state["constraints"]
    recommendations = state["recommendations"]
    config = load_config()
    
    # Load prompt
    prompt_template = load_prompt()
    prompt = prompt_template.format(
        user_request=user_request,
        constraints=json.dumps(constraints, indent=2),
        recommendations=json.dumps(recommendations, indent=2)
    )
    
    llm = get_llm(config, temperature=0.3)
    response = llm.invoke([
        SystemMessage(content="You are a helpful recipe selection assistant."),
        HumanMessage(content=prompt)
    ])
    
    # Parse selection
    try:
        content = response.content.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1])
        
        selection = json.loads(content)
        selected_index = selection.get("selected_index", 0)
        
        # Validate index
        if selected_index < 0 or selected_index >= len(recommendations):
            selected_index = 0
        
        selected_recommendation = recommendations[selected_index]
        selected_recommendation["reason_selected"] = selection.get("reason_selected", "")
        selected_recommendation["expected_recipe_direction"] = selection.get("expected_recipe_direction", "")
        
    except Exception as e:
        print(f"Warning: Failed to parse selection, using first recommendation: {e}")
        selected_recommendation = recommendations[0] if recommendations else {}
    
    return {
        **state,
        "selected_recommendation": selected_recommendation
    }
