"""Generate recipe draft node."""
import json
from langchain_core.messages import HumanMessage, SystemMessage
from ..state import RecipeState
from ..config import load_config
from ..tools.llm import get_llm
from pathlib import Path


def load_prompt():
    """Load generate_recipe prompt template."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "generate_recipe.md"
    return prompt_path.read_text(encoding="utf-8")


def generate_recipe(state: RecipeState) -> RecipeState:
    """Generate a complete recipe draft."""
    user_request = state["user_request"]
    constraints = state["constraints"]
    output_language = state["output_language"]
    config = load_config()
    
    # Get the source for recipe (either selected_recommendation or direct request)
    task_type = state.get("task_type", "recommend_then_recipe")
    
    if task_type == "recommend_then_recipe" and state.get("selected_recommendation"):
        recipe_concept = json.dumps(state["selected_recommendation"], indent=2)
        context_info = f"\n\nSelected from recommendations based on user request."
    elif task_type == "recipe_only":
        recipe_concept = json.dumps({"concept": "Direct recipe request"}, indent=2)
        context_info = f"\n\nUser requested a specific recipe directly."
    else:
        recipe_concept = json.dumps({"concept": "Generic recipe"}, indent=2)
        context_info = ""
    
    # Load prompt
    prompt_template = load_prompt()
    prompt = prompt_template.format(
        user_request=user_request,
        recipe_concept=recipe_concept,
        constraints=json.dumps(constraints, indent=2),
        output_language=output_language
    ) + context_info
    
    llm = get_llm(config, temperature=0.6)
    response = llm.invoke([
        SystemMessage(content="You are a professional chef and recipe writer."),
        HumanMessage(content=prompt)
    ])
    
    # Parse recipe draft
    try:
        draft_text = response.content.strip()
        if draft_text.startswith("```"):
            lines = draft_text.split("\n")
            draft_text = "\n".join(lines[1:-1])
        
        recipe_draft = json.loads(draft_text)
    except Exception as e:
        print(f"Warning: Failed to parse recipe draft: {e}")
        recipe_draft = {
            "title": "Recipe",
            "description": "A recipe",
            "prep_time_minutes": 10,
            "cook_time_minutes": 20,
            "total_time_minutes": 30,
            "servings": 2,
            "difficulty": "easy",
            "ingredients": [],
            "steps": [],
            "tips": [],
            "substitutions": []
        }
    
    return {
        **state,
        "draft_recipe": recipe_draft
    }
