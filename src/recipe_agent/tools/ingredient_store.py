"""Ingredient store for local knowledge base."""
import yaml
from pathlib import Path


def load_ingredient_store() -> dict:
    """Load ingredient knowledge base from YAML file."""
    data_path = Path(__file__).parent.parent.parent.parent / "data" / "common_alfamart_ingredients.yaml"
    
    if not data_path.exists():
        return {}
    
    with open(data_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_all_ingredients() -> list[str]:
    """Get flat list of all available ingredients."""
    store = load_ingredient_store()
    ingredients = []
    for category, items in store.items():
        if isinstance(items, list):
            ingredients.extend(items)
    return ingredients


def get_ingredients_by_category(category: str) -> list[str]:
    """Get ingredients for a specific category."""
    store = load_ingredient_store()
    return store.get(category, [])
