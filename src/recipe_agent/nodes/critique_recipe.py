"""Critique recipe node."""
import json
from langchain_core.messages import HumanMessage, SystemMessage
from ..state import RecipeState
from ..config import load_config
from ..tools.llm import get_llm
from pathlib import Path


def load_critique_prompt():
    """Load critique recipe prompt template."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "critique_recipe.md"
    return prompt_path.read_text(encoding="utf-8")


def critique_recipe(state: RecipeState) -> RecipeState:
    """Critique the recipe and assign a quality score."""
    user_request = state["user_request"]
    draft_recipe = state["draft_recipe"]
    constraints = state["constraints"]
    config = load_config()
    
    # Load prompt
    prompt_template = load_critique_prompt()
    
    # Format prompt
    prompt = prompt_template.format(
        user_request=user_request,
        recipe=json.dumps(draft_recipe, indent=2),
        constraints=json.dumps(constraints, indent=2)
    )
    
    llm = get_llm(config, temperature=0.3)
    response = llm.invoke([
        SystemMessage(content="You are a strict recipe critic."),
        HumanMessage(content=prompt)
    ])
    
    # Parse critique
    try:
        critique_text = response.content.strip()
        if critique_text.startswith("```"):
            lines = critique_text.split("\n")
            critique_text = "\n".join(lines[1:-1])
        
        critique = json.loads(critique_text)
        score = float(critique.get("score", 0.5))
        passed = critique.get("passed", score >= state["approval_threshold"])
        issues = critique.get("issues", [])
        revision_instructions = critique.get("revision_instructions", [])
        
    except Exception as e:
        print(f"Warning: Failed to parse critique: {e}")
        score = 0.5
        passed = False
        issues = ["Unable to parse critique"]
        revision_instructions = ["Improve recipe clarity and completeness"]
    
    return {
        **state,
        "critique_score": score,
        "critique_passed": passed,
        "critique_notes": issues,
        "revision_instructions": revision_instructions
    }
