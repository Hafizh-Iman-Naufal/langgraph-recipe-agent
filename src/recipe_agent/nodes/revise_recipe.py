"""Revise recipe node."""
import json
from langchain_core.messages import HumanMessage, SystemMessage
from ..state import RecipeState
from ..config import load_config
from ..tools.llm import get_llm
from pathlib import Path


def load_revise_prompt():
    """Load revise recipe prompt template."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "revise_recipe.md"
    return prompt_path.read_text(encoding="utf-8")


def revise_recipe(state: RecipeState) -> RecipeState:
    """Revise the recipe based on critique feedback."""
    user_request = state["user_request"]
    draft_recipe = state["draft_recipe"]
    revision_instructions = state["revision_instructions"]
    constraints = state["constraints"]
    output_language = state["output_language"]
    revision_count = state["revision_count"]
    config = load_config()
    
    # Load prompt
    prompt_template = load_revise_prompt()
    
    # Format prompt
    prompt = prompt_template.format(
        user_request=user_request,
        recipe=json.dumps(draft_recipe, indent=2),
        revision_instructions="\n".join(f"- {instr}" for instr in revision_instructions),
        constraints=json.dumps(constraints, indent=2),
        output_language=output_language
    )
    
    llm = get_llm(config, temperature=0.5)
    response = llm.invoke([
        SystemMessage(content="You are a professional chef revising a recipe."),
        HumanMessage(content=prompt)
    ])
    
    # Parse revised recipe
    try:
        revised_text = response.content.strip()
        if revised_text.startswith("```"):
            lines = revised_text.split("\n")
            revised_text = "\n".join(lines[1:-1])
        
        revised_recipe = json.loads(revised_text)
    except Exception as e:
        print(f"Warning: Failed to parse revised recipe: {e}")
        revised_recipe = draft_recipe
    
    return {
        **state,
        "draft_recipe": revised_recipe,
        "revision_count": revision_count + 1
    }
