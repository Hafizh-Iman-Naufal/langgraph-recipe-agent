"""Decide task type node."""
import json
from langchain_core.messages import HumanMessage, SystemMessage
from ..state import RecipeState
from ..config import load_config
from ..tools.llm import get_llm
from pathlib import Path


def load_prompt():
    """Load decide_task prompt template."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "decide_task.md"
    return prompt_path.read_text(encoding="utf-8")


def decide_task(state: RecipeState) -> RecipeState:
    """Decide what type of task the user wants."""
    user_request = state["user_request"]
    config = load_config()
    
    # Load prompt
    prompt_template = load_prompt()
    prompt = prompt_template.format(user_request=user_request)
    
    llm = get_llm(config, temperature=0.2)
    response = llm.invoke([
        SystemMessage(content="You are a helpful task router. Return only valid JSON."),
        HumanMessage(content=prompt)
    ])
    
    # Parse response
    try:
        content = response.content.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1])
        
        result = json.loads(content)
        task_type = result.get("task_type", "recommend_then_recipe")
        
        # Validate task_type
        valid_tasks = [
            "recommendations_only",
            "recipe_only",
            "recommend_then_recipe",
            "clarification_needed"
        ]
        
        if task_type not in valid_tasks:
            task_type = config.get("default_task_type", "recommend_then_recipe")
            
    except Exception as e:
        print(f"Warning: Failed to parse task decision: {e}")
        task_type = config.get("default_task_type", "recommend_then_recipe")
    
    return {
        **state,
        "task_type": task_type
    }
