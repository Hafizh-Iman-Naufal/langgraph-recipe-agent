"""Markdown writer for recipe output."""
from ..state import RecipeState


def render_recommendations_markdown(recommendations: list[dict], state: RecipeState) -> str:
    """Render recommendations as formatted markdown."""
    output_language = state.get("output_language", "en")
    
    lines = []
    
    # Title
    if output_language == "id":
        lines.append("# Rekomendasi Makanan dan Minuman")
        lines.append("")
        lines.append("Berdasarkan permintaan kamu, berikut rekomendasi yang cocok:")
    else:
        lines.append("# Food and Drink Recommendations")
        lines.append("")
        lines.append("Based on your request, here are the recommendations:")
    
    lines.append("")
    
    # Recommendations list
    for i, rec in enumerate(recommendations, 1):
        name = rec.get("name", "Unknown")
        rec_type = rec.get("type", "food")
        estimated_time = rec.get("estimated_time_minutes", "N/A")
        why_it_fits = rec.get("why_it_fits", "")
        
        if output_language == "id":
            type_label = "Makanan" if rec_type == "food" else "Minuman"
            time_label = f"{estimated_time} menit"
        else:
            type_label = "Food" if rec_type == "food" else "Drink"
            time_label = f"{estimated_time} minutes"
        
        lines.append(f"{i}. **{name}** ({type_label})")
        lines.append(f"   - {time_label}")
        if why_it_fits:
            lines.append(f"   - {why_it_fits}")
        lines.append("")
    
    return "\n".join(lines)


def render_recommend_then_recipe_markdown(
    recommendations: list[dict],
    selected_recommendation: dict,
    recipe: dict,
    videos: list[dict],
    state: RecipeState
) -> str:
    """Render recommendations + selected recipe as formatted markdown."""
    output_language = state.get("output_language", "en")
    
    lines = []
    
    # Title
    selected_name = selected_recommendation.get("name", "Selected Recipe")
    reason_selected = selected_recommendation.get("reason_selected", "")
    
    if output_language == "id":
        lines.append(f"# Rekomendasi Terbaik: {selected_name}")
        lines.append("")
        lines.append("## Kenapa Ini Dipilih")
        lines.append("")
        if reason_selected:
            lines.append(reason_selected)
        else:
            lines.append("Dari rekomendasi yang ada, resep ini paling cocok dengan permintaan kamu.")
    else:
        lines.append(f"# Best Recommendation: {selected_name}")
        lines.append("")
        lines.append("## Why This Was Selected")
        lines.append("")
        if reason_selected:
            lines.append(reason_selected)
        else:
            lines.append("From the recommendations, this recipe best matches your request.")
    
    lines.append("")
    
    # Shortlist
    if output_language == "id":
        lines.append("## Daftar Rekomendasi")
    else:
        lines.append("## Recommendation Shortlist")
    lines.append("")
    
    for i, rec in enumerate(recommendations, 1):
        name = rec.get("name", "Unknown")
        lines.append(f"{i}. {name}")
    
    lines.append("")
    
    # Full recipe
    if output_language == "id":
        lines.append("## Resep Lengkap")
    else:
        lines.append("## Full Recipe")
    lines.append("")
    
    # Recipe content
    lines.extend(render_recipe_content(recipe, output_language))
    
    # Video recommendations
    if videos:
        if output_language == "id":
            lines.append("## Video Rekomendasi")
        else:
            lines.append("## Video Recommendations")
        lines.append("")
        for video in videos:
            lines.append(f"- [{video['title']}]({video.get('shorts_url', video.get('url'))})")
        lines.append("")
    
    return "\n".join(lines)


def render_recipe_only_markdown(recipe: dict, videos: list[dict], state: RecipeState) -> str:
    """Render single recipe as formatted markdown."""
    output_language = state.get("output_language", "en")
    
    lines = []
    
    # Recipe content
    lines.extend(render_recipe_content(recipe, output_language))
    
    # Video recommendations
    if videos:
        if output_language == "id":
            lines.append("## Video Rekomendasi")
        else:
            lines.append("## Video Recommendations")
        lines.append("")
        for video in videos:
            lines.append(f"- [{video['title']}]({video.get('shorts_url', video.get('url'))})")
        lines.append("")
    
    return "\n".join(lines)


def render_recipe_content(recipe: dict, output_language: str) -> list[str]:
    """Render recipe content (title, ingredients, steps, etc.)."""
    lines = []
    
    # Title
    title = recipe.get("title", "Recipe")
    lines.append(f"# {title}")
    lines.append("")
    
    # Why this recipe fits
    if output_language == "id":
        lines.append("## Kenapa Resep Ini Cocok")
    else:
        lines.append("## Why This Recipe Fits")
    lines.append("")
    if recipe.get("description"):
        lines.append(recipe["description"])
    lines.append("")
    
    # Ingredients
    if output_language == "id":
        lines.append("## Bahan-Bahan")
    else:
        lines.append("## Ingredients")
    lines.append("")
    for ing in recipe.get("ingredients", []):
        if isinstance(ing, dict):
            item = ing.get("item", "")
            amount = ing.get("amount", "")
            unit = ing.get("unit", "")
            lines.append(f"- {amount} {unit} {item}")
        else:
            lines.append(f"- {ing}")
    lines.append("")
    
    # Steps
    if output_language == "id":
        lines.append("## Langkah-Langkah")
    else:
        lines.append("## Steps")
    lines.append("")
    for i, step in enumerate(recipe.get("steps", []), 1):
        if isinstance(step, dict):
            lines.append(f"{i}. {step.get('instruction', step)}")
        else:
            lines.append(f"{i}. {step}")
    lines.append("")
    
    # Estimated time
    if output_language == "id":
        lines.append("## Estimasi Waktu")
    else:
        lines.append("## Estimated Time")
    lines.append("")
    prep = recipe.get("prep_time_minutes", "N/A")
    cook = recipe.get("cook_time_minutes", "N/A")
    total = recipe.get("total_time_minutes", "N/A")
    if output_language == "id":
        lines.append(f"- Persiapan: {prep} menit")
        lines.append(f"- Memasak: {cook} menit")
        lines.append(f"- Total: {total} menit")
    else:
        lines.append(f"- Prep: {prep} minutes")
        lines.append(f"- Cook: {cook} minutes")
        lines.append(f"- Total: {total} minutes")
    lines.append("")
    
    # Difficulty
    if output_language == "id":
        lines.append("## Tingkat Kesulitan")
    else:
        lines.append("## Difficulty")
    lines.append("")
    difficulty = recipe.get("difficulty", "N/A")
    lines.append(difficulty.capitalize())
    lines.append("")
    
    # Substitutions
    if recipe.get("substitutions"):
        if output_language == "id":
            lines.append("## Alternatif Bahan")
        else:
            lines.append("## Substitutions")
        lines.append("")
        for sub in recipe["substitutions"]:
            lines.append(f"- {sub}")
        lines.append("")
    
    # Tips
    if recipe.get("tips"):
        if output_language == "id":
            lines.append("## Tips")
        else:
            lines.append("## Tips")
        lines.append("")
        for tip in recipe["tips"]:
            lines.append(f"- {tip}")
        lines.append("")
    
    return lines


def render_markdown(
    recipe: dict,
    videos: list[dict],
    state: RecipeState
) -> str:
    """Main render function that routes to appropriate formatter."""
    task_type = state.get("task_type", "recommend_then_recipe")
    
    if task_type == "recommendations_only":
        recommendations = state.get("recommendations", [])
        return render_recommendations_markdown(recommendations, state)
    elif task_type == "recommend_then_recipe":
        recommendations = state.get("recommendations", [])
        selected_recommendation = state.get("selected_recommendation", {})
        return render_recommend_then_recipe_markdown(
            recommendations, selected_recommendation, recipe, videos, state
        )
    else:  # recipe_only or unknown
        return render_recipe_only_markdown(recipe, videos, state)
