"""Select best recipe node."""
import json
from langchain_core.messages import HumanMessage, SystemMessage
from ..state import RecipeState
from ..config import load_config
from ..tools.llm import get_llm


def select_recipe(state: RecipeState) -> RecipeState:
    """Select the best recipe from candidates."""
    user_request = state["user_request"]
    constraints = state["constraints"]
    candidates = state["recipe_candidates"]
    output_language = state["output_language"]
    config = load_config()
    
    prompt = f"""You are a recipe selection expert. Given these recipe ideas and user constraints, select the BEST recipe.

User request: {user_request}

User constraints:
{json.dumps(constraints, indent=2)}

Recipe candidates:
{json.dumps(candidates, indent=2)}

Select the recipe that best matches ALL constraints. Consider:
- Matches user intent (highest priority)
- Uses available ingredients (high priority)
- Simple to prepare (high priority)
- Low cost (medium priority)
- Fast cooking time (medium priority)
- Interesting taste (medium priority)

Return a JSON object with:
{{
  "selected_index": number (0-based index of selected recipe),
  "reasoning": "Why this recipe is the best choice"
}}

Return ONLY valid JSON."""
    
    llm = get_llm(config, temperature=0.3)
    response = llm.invoke([
        SystemMessage(content="You are a helpful recipe selection assistant."),
        HumanMessage(content=prompt)
    ])
    
    # Parse selection
    try:
        selection_text = response.content.strip()
        if selection_text.startswith("```"):
            lines = selection_text.split("\n")
            selection_text = "\n".join(lines[1:-1])
        
        selection = json.loads(selection_text)
        selected_index = selection.get("selected_index", 0)
        
        # Validate index
        if selected_index < 0 or selected_index >= len(candidates):
            selected_index = 0
            
    except Exception as e:
        print(f"Warning: Failed to parse selection, using first recipe: {e}")
        selected_index = 0
    
    selected_recipe = candidates[selected_index]
    
    return {
        **state,
        "selected_recipe": selected_recipe
    }
