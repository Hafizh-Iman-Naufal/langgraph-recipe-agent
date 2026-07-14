"""Generate recommendations node."""
import json
from langchain_core.messages import HumanMessage, SystemMessage
from ..state import RecipeState
from ..config import load_config
from ..tools.llm import get_llm
from ..tools.ingredient_store import load_ingredient_store
from pathlib import Path


def load_prompt():
    """Load generate_recommendations prompt template."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "generate_recommendations.md"
    return prompt_path.read_text(encoding="utf-8")


def generate_recommendations(state: RecipeState) -> RecipeState:
    """Generate food/drink recommendations based on constraints."""
    user_request = state["user_request"]
    constraints = state["constraints"]
    output_language = state["output_language"]
    recommendation_count = state.get("recommendation_count", 10)
    config = load_config()
    
    # Load ingredient store
    ingredient_store = load_ingredient_store()
    available_ingredients = []
    for category, items in ingredient_store.items():
        available_ingredients.extend(items)
    
    # Load prompt
    prompt_template = load_prompt()
    prompt = prompt_template.format(
        user_request=user_request,
        constraints=json.dumps(constraints, indent=2),
        available_ingredients="\n".join(f"- {item}" for item in available_ingredients[:50]),
        output_language=output_language,
        recommendation_count=recommendation_count
    )
    
    llm = get_llm(config, temperature=0.7)
    response = llm.invoke([
        SystemMessage(content="You are a helpful recipe assistant."),
        HumanMessage(content=prompt)
    ])
    
    # Parse JSON response
    try:
        content = response.content.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1])
        
        recommendations = json.loads(content)
        
        # Ensure we have a list
        if not isinstance(recommendations, list):
            recommendations = [recommendations]
            
        # Ensure minimum count (fill with generic if needed)
        while len(recommendations) < recommendation_count:
            recommendations.append({
                "name": f"Simple Recipe {len(recommendations) + 1}",
                "type": "food",
                "short_description": "A simple option",
                "why_it_fits": "Matches basic requirements",
                "estimated_time_minutes": 15,
                "difficulty": "easy",
                "main_ingredients": [],
                "ingredient_availability_notes": "",
                "store_fit_score": 0.5,
                "simplicity_score": 0.8
            })
        
        # Limit to requested count
        recommendations = recommendations[:recommendation_count]
        
    except Exception as e:
        print(f"Warning: Failed to parse recommendations: {e}")
        recommendations = [
            {
                "name": "Simple Recipe",
                "type": "food",
                "short_description": "A basic recipe option",
                "why_it_fits": "Matches basic requirements",
                "estimated_time_minutes": 15,
                "difficulty": "easy",
                "main_ingredients": ["ingredient 1", "ingredient 2"],
                "ingredient_availability_notes": "",
                "store_fit_score": 0.5,
                "simplicity_score": 0.8
            }
        ]
    
    return {
        **state,
        "recommendations": recommendations
    }
