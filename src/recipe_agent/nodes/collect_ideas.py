"""Collect recipe ideas node."""
import json
from langchain_core.messages import HumanMessage, SystemMessage
from ..state import RecipeState
from ..config import load_config
from ..tools.llm import get_llm
from ..tools.ingredient_store import load_ingredient_store


def collect_ideas(state: RecipeState) -> RecipeState:
    """Collect recipe candidates from LLM and local knowledge."""
    constraints = state["constraints"]
    search_queries = state["search_queries"]
    output_language = state["output_language"]
    config = load_config()
    
    # Load ingredient store
    ingredient_store = load_ingredient_store()
    
    # Build context from ingredient store
    available_ingredients = []
    for category, items in ingredient_store.items():
        available_ingredients.extend(items)
    
    # Generate recipe candidates using LLM
    prompt = f"""You are a recipe expert. Generate 3 recipe ideas based on these constraints.

Constraints:
{json.dumps(constraints, indent=2)}

Available ingredients (from local store):
{chr(10).join(f"- {item}" for item in available_ingredients[:50])}

Language: {output_language}

For each recipe idea, provide:
- name: Recipe name
- description: Brief 1-2 sentence description
- estimated_time_minutes: Estimated cooking time
- difficulty: easy/medium/hard
- key_ingredients: List of 5-8 main ingredients (prefer ingredients from available list)
- why_suitable: Why this matches the user's request
- source: "llm_generated"

Return as a JSON array of objects. Return ONLY valid JSON."""
    
    llm = get_llm(config, temperature=0.7)
    response = llm.invoke([
        SystemMessage(content="You are a helpful recipe assistant."),
        HumanMessage(content=prompt)
    ])
    
    # Parse JSON response
    try:
        ideas_text = response.content.strip()
        if ideas_text.startswith("```"):
            lines = ideas_text.split("\n")
            ideas_text = "\n".join(lines[1:-1])
        
        recipe_candidates = json.loads(ideas_text)
        
        # Ensure source is set
        for candidate in recipe_candidates:
            if "source" not in candidate:
                candidate["source"] = "llm_generated"
                
    except Exception as e:
        print(f"Warning: Failed to parse recipe ideas: {e}")
        recipe_candidates = [
            {
                "name": "Simple Recipe",
                "description": "A basic recipe option",
                "estimated_time_minutes": 30,
                "difficulty": "easy",
                "key_ingredients": ["ingredient 1", "ingredient 2"],
                "why_suitable": "Matches basic requirements",
                "source": "llm_generated"
            }
        ]
    
    return {
        **state,
        "recipe_candidates": recipe_candidates
    }
