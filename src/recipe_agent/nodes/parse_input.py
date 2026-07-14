"""Parse user input node."""
import json
from pathlib import Path
from langchain_core.messages import HumanMessage, SystemMessage
from ..state import RecipeState
from ..config import load_config
from ..tools.ingredient_store import load_ingredient_store
from ..tools.language import detect_language


def load_parse_prompt():
    """Load parse input prompt template."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "parse_input.md"
    return prompt_path.read_text(encoding="utf-8")


def parse_input(state: RecipeState) -> RecipeState:
    """Parse user input and extract constraints."""
    from ..tools.llm import get_llm
    
    user_request = state["user_request"]
    config = load_config()
    
    # Detect language
    if state["language"] == "auto":
        detected = detect_language(user_request)
        output_language = detected
    else:
        output_language = state["language"]
    
    # Load prompt
    prompt_template = load_parse_prompt()
    
    # Load ingredient store for context
    ingredient_store = load_ingredient_store()
    available_ingredients = []
    for category, items in ingredient_store.items():
        available_ingredients.extend(items)
    
    # Format prompt
    prompt = prompt_template.format(
        user_request=user_request,
        available_ingredients="\n".join(f"- {item}" for item in available_ingredients[:50])
    )
    
    # Parse constraints using LLM
    llm = get_llm(config, temperature=0.3)
    response = llm.invoke([
        SystemMessage(content="You are a helpful assistant that extracts structured information from text. Return only valid JSON."),
        HumanMessage(content=prompt)
    ])
    
    # Parse JSON response
    try:
        constraints_text = response.content.strip()
        if constraints_text.startswith("```"):
            lines = constraints_text.split("\n")
            constraints_text = "\n".join(lines[1:-1])
        
        constraints = json.loads(constraints_text)
    except Exception as e:
        print(f"Warning: Failed to parse constraints, using defaults: {e}")
        constraints = {
            "recipe_type": "food",
            "simplicity": "simple",
            "store_constraint": None,
            "ingredient_availability": None,
            "budget": None,
            "max_cooking_time_minutes": None,
            "dietary_restrictions": [],
            "servings": None
        }
    
    return {
        **state,
        "output_language": output_language,
        "constraints": constraints
    }
