#!/usr/bin/env python3
"""Main entry point for the recipe recommendation agent."""
import argparse
from pathlib import Path
from .graph import create_recipe_graph
from .config import load_config, validate_config
from .state import RecipeState


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Recipe Recommendation Agent")
    parser.add_argument(
        "--request",
        type=str,
        required=True,
        help="User recipe request"
    )
    parser.add_argument(
        "--language",
        type=str,
        choices=["auto", "en", "id"],
        default="auto",
        help="Output language (default: auto-detect)"
    )
    parser.add_argument(
        "--task-type",
        type=str,
        choices=["recommendations_only", "recipe_only", "recommend_then_recipe", "clarification_needed"],
        default=None,
        help="Task type (default: auto-detect)"
    )
    parser.add_argument(
        "--output-mode",
        type=str,
        choices=["print", "markdown"],
        default=None,
        help="Output mode (default: from config)"
    )
    parser.add_argument(
        "--include-video-urls",
        type=bool,
        default=None,
        help="Include YouTube video URLs (default: from config)"
    )
    parser.add_argument(
        "--max-revisions",
        type=int,
        default=None,
        help="Maximum number of revisions (default: from config)"
    )
    
    args = parser.parse_args()
    
    # Load configuration
    try:
        config = load_config()
        validate_config(config)
    except Exception as e:
        print(f"Configuration error: {e}")
        print("\nMake sure you have:")
        print("1. Copied .env.example to .env")
        print("2. Set your OPENAI_API_KEY in .env")
        return
    
    # Build initial state
    initial_state = RecipeState(
        user_request=args.request,
        language=args.language,
        output_language=None,  # Will be set by parse_input
        output_mode=args.output_mode or config.get("default_output_mode", "print"),
        task_type=args.task_type,  # Will be auto-detected if None
        recommendation_count=config.get("default_recommendation_count", 10),
        recommendations=[],
        recommendation_critique_score=0.0,
        recommendation_critique_notes=[],
        include_video_urls=args.include_video_urls if args.include_video_urls is not None else config.get("default_include_video_urls", False),
        max_video_urls=config.get("default_max_video_urls", 5),
        constraints={},
        search_queries=[],
        recipe_candidates=[],
        selected_recommendation=None,
        selected_recipe=None,
        draft_recipe=None,
        critique_score=0.0,
        critique_passed=False,
        critique_notes=[],
        revision_instructions=[],
        revision_count=0,
        max_revisions=args.max_revisions or config.get("default_max_revisions", 3),
        approval_threshold=config.get("default_approval_threshold", 0.85),
        video_urls=[],
        final_output=None,
        output_path=None,
        errors=[],
        warnings=[]
    )
    
    # Create and run graph
    graph = create_recipe_graph()
    
    print("\n" + "=" * 80)
    print("RECIPE RECOMMENDATION AGENT")
    print("=" * 80)
    print(f"\nUser request: {args.request}")
    print(f"Language: {args.language}")
    if args.task_type:
        print(f"Task type: {args.task_type} (forced)")
    else:
        print("Task type: auto-detect")
    print()
    
    try:
        final_state = graph.invoke(initial_state)
        
        # Print summary
        task_type = final_state.get("task_type", "unknown")
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Task type: {task_type}")
        print(f"Language: {final_state.get('output_language', 'unknown')}")
        
        if task_type == "recommendations_only":
            recs = final_state.get("recommendations", [])
            print(f"Recommendations generated: {len(recs)}")
            print(f"Recommendation critique score: {final_state.get('recommendation_critique_score', 0.0):.2f}")
        elif task_type == "recommend_then_recipe":
            recs = final_state.get("recommendations", [])
            print(f"Recommendations generated: {len(recs)}")
            print(f"Recommendation critique score: {final_state.get('recommendation_critique_score', 0.0):.2f}")
            selected = final_state.get("selected_recommendation", {})
            print(f"Selected recommendation: {selected.get('name', 'N/A')}")
            print(f"Recipe critique score: {final_state.get('critique_score', 0.0):.2f}")
            print(f"Revisions: {final_state.get('revision_count', 0)}/{final_state.get('max_revisions', 3)}")
        elif task_type == "recipe_only":
            print(f"Recipe critique score: {final_state.get('critique_score', 0.0):.2f}")
            print(f"Revisions: {final_state.get('revision_count', 0)}/{final_state.get('max_revisions', 3)}")
        
        videos = final_state.get("video_urls", [])
        print(f"YouTube videos: {len(videos)}")
        
        if final_state.get("errors"):
            print(f"\nErrors: {len(final_state['errors'])}")
            for error in final_state["errors"]:
                print(f"  - {error}")
        
        if final_state.get("warnings"):
            print(f"\nWarnings: {len(final_state['warnings'])}")
            for warning in final_state["warnings"]:
                print(f"  - {warning}")
        
        print("=" * 80)
        
    except Exception as e:
        print(f"\nError running graph: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
