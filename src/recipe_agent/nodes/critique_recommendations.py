"""Critique recommendations node."""
import json
from langchain_core.messages import HumanMessage, SystemMessage
from ..state import RecipeState
from ..config import load_config
from ..tools.llm import get_llm
from pathlib import Path


def load_prompt():
    """Load critique_recommendations prompt template."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "critique_recommendations.md"
    return prompt_path.read_text(encoding="utf-8")


def critique_recommendations(state: RecipeState) -> RecipeState:
    """Critique the recommendation list quality."""
    user_request = state["user_request"]
    recommendations = state["recommendations"]
    constraints = state["constraints"]
    config = load_config()
    
    # Load prompt
    prompt_template = load_prompt()
    prompt = prompt_template.format(
        user_request=user_request,
        recommendations=json.dumps(recommendations, indent=2),
        constraints=json.dumps(constraints, indent=2)
    )
    
    llm = get_llm(config, temperature=0.3)
    response = llm.invoke([
        SystemMessage(content="You are a strict recommendation quality reviewer."),
        HumanMessage(content=prompt)
    ])
    
    # Parse critique
    try:
        content = response.content.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1])
        
        critique = json.loads(content)
        score = float(critique.get("score", 0.5))
        notes = critique.get("issues", [])
        
    except Exception as e:
        print(f"Warning: Failed to parse recommendation critique: {e}")
        score = 0.5
        notes = ["Unable to parse critique, defaulting to moderate score"]
    
    return {
        **state,
        "recommendation_critique_score": score,
        "recommendation_critique_notes": notes
    }
