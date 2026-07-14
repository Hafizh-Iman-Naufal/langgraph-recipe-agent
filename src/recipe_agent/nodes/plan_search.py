"""Plan search queries node."""
from ..state import RecipeState


def plan_search(state: RecipeState) -> RecipeState:
    """Create search queries based on parsed constraints."""
    constraints = state["constraints"]
    output_language = state["output_language"]
    
    search_queries = []
    
    # Build queries based on constraints
    recipe_type = constraints.get("recipe_type", "food")
    simplicity = constraints.get("simplicity", "simple")
    store_constraint = constraints.get("store_constraint")
    max_time = constraints.get("max_cooking_time_minutes")
    
    if output_language == "id":
        # Indonesian queries
        if store_constraint:
            search_queries.append(f"resep {recipe_type} simple bahan {store_constraint}")
        search_queries.append(f"resep {recipe_type} simple")
        if max_time:
            search_queries.append(f"resep {recipe_type} cepat {max_time} menit")
    else:
        # English queries
        if store_constraint:
            search_queries.append(f"simple {recipe_type} recipe {store_constraint} ingredients")
        search_queries.append(f"simple {recipe_type} recipe")
        if max_time:
            search_queries.append(f"quick {recipe_type} recipe under {max_time} minutes")
    
    # Add generic queries
    search_queries.append(f"easy {recipe_type} convenience store recipe")
    
    # Limit to 5 queries
    search_queries = search_queries[:5]
    
    return {
        **state,
        "search_queries": search_queries
    }
