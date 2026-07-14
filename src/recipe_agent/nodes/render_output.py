"""Render final output node."""
from pathlib import Path
from datetime import datetime
from ..state import RecipeState
from ..config import load_config
from ..tools.markdown_writer import render_markdown


def render_output(state: RecipeState) -> RecipeState:
    """Render the final recipe output."""
    recipe = state.get("draft_recipe", {})
    videos = state.get("video_urls", [])
    output_mode = state.get("output_mode", "print")
    task_type = state.get("task_type", "recommend_then_recipe")
    
    # Handle clarification_needed case
    if task_type == "clarification_needed":
        output_text = _render_clarification_message(state)
    else:
        # Render based on task_type
        output_text = render_markdown(recipe, videos, state)
    
    # Add quality info for recipe outputs
    if task_type in ("recipe_only", "recommend_then_recipe"):
        quality_info = f"\n\n---\n*Recipe quality score: {state.get('critique_score', 0):.2f}/1.00* | *Revisions: {state.get('revision_count', 0)}*"
        output_text += quality_info
    
    # Add recommendation score if applicable
    if task_type in ("recommendations_only", "recommend_then_recipe"):
        rec_score = state.get("recommendation_critique_score", 0.0)
        output_text += f"\n*Recommendation quality score: {rec_score:.2f}/1.00*"
    
    # Add warnings if any
    warnings = state.get("warnings", [])
    if warnings:
        output_text += "\n\n---\n**Warnings:**\n"
        for warning in warnings:
            output_text += f"- {warning}\n"
    
    # Output based on mode
    if output_mode == "markdown":
        output_dir = Path(__file__).parent.parent.parent.parent / "outputs"
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recipe_{timestamp}.md"
        output_path = output_dir / filename
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_text)
        
        print(f"\nOutput saved to: {output_path}")
        
        return {
            **state,
            "final_output": output_text,
            "output_path": str(output_path)
        }
    else:
        # Print to console
        print("\n" + "="*60)
        print(output_text)
        print("="*60 + "\n")
        
        return {
            **state,
            "final_output": output_text,
            "output_path": None
        }


def _render_clarification_message(state: RecipeState) -> str:
    """Render a helpful clarification message."""
    output_language = state.get("output_language", "en")
    user_request = state.get("user_request", "")
    
    if output_language == "id":
        return (
            "# Mohon Klarifikasi\n\n"
            "Permintaan kamu terlalu umum untuk menghasilkan rekomendasi yang berguna.\n\n"
            "Coba berikan lebih detail, misalnya:\n"
            "- Jenis makanan atau minuman yang diinginkan\n"
            "- Bahan yang tersedia atau toko terdekat\n"
            "- Waktu memasak yang diinginkan\n"
            "- Budget\n\n"
            f"Contoh: \"Saya mau makanan simple yang bahannya bisa ditemukan di Alfamart terdekat.\"\n"
        )
    else:
        return (
            "# Clarification Needed\n\n"
            "Your request is too general to provide useful recommendations.\n\n"
            "Try providing more detail, such as:\n"
            "- Type of food or drink you want\n"
            "- Available ingredients or nearby store\n"
            "- Desired cooking time\n"
            "- Budget\n\n"
            f"Example: \"I want a simple recipe with ingredients from a nearby convenience store.\"\n"
        )
