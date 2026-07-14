# LangGraph Recipe Recommendation Agent

An intelligent recipe recommendation system built with Python and LangGraph that understands natural language requests in English and Bahasa Indonesia.

## Features

- **Smart Task Routing**: Automatically determines what you need:
  - `recommendations_only`: Generate a list of food/drink ideas
  - `recipe_only`: Create a detailed recipe for a specific dish
  - `recommend_then_recipe`: Get recommendations, select the best, then generate a full recipe (default)
  - `clarification_needed`: Ask for more details when request is unclear
  
- **Intelligent Recommendations**: Generates 10 tailored food/drink suggestions by default based on your constraints
- **Quality Critique System**: Two-stage critique process:
  - Recommendation critique ensures suggestions match your needs
  - Recipe critique with 0.0-1.0 scoring threshold (default 0.85)
  - Automatic revisions up to max limit (default 3)
- **Bilingual Support**: Detects and responds in English or Bahasa Indonesia
- **Local Ingredient Knowledge**: Uses curated ingredient database for realistic store availability
- **Optional YouTube Integration**: Includes video tutorials when YouTube API is configured
- **Flexible Output**: Print to console or save to Markdown file

## Architecture

The agent uses a sophisticated LangGraph workflow with conditional routing:

```
parse_input → decide_task
    ↓
    ├─→ recommendations_only → generate_recommendations → critique_recommendations → render_output
    ├─→ recipe_only → generate_recipe → critique_recipe → (revise loop) → fetch_youtube_videos → render_output
    └─→ recommend_then_recipe → generate_recommendations → critique_recommendations → select_best_recommendation → generate_recipe → critique_recipe → (revise loop) → fetch_youtube_videos → render_output
    └─→ clarification_needed → render_output
```

### Nodes

1. **parse_input** - Detect language and extract constraints
2. **decide_task** - Route to appropriate workflow based on user intent
3. **generate_recommendations** - Create 10 food/drink ideas (configurable)
4. **critique_recommendations** - Validate recommendation quality (0.0-1.0)
5. **select_best_recommendation** - Pick the best candidate for recipe generation
6. **generate_recipe** - Create detailed recipe draft
7. **critique_recipe** - Score recipe quality using weighted rubric
8. **revise_recipe** - Improve recipe based on feedback
9. **fetch_youtube_videos** - Optional video recommendations
10. **render_output** - Final formatted output (3 different formats)

## Setup

### 1. Install Dependencies

```bash
cd /home/ubuntu/langgraph-recipe-agent
source venv/bin/activate
pip install pyyaml pytest
```

### 2. Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=your-openai-api-key-here
```

### Configuration Options

```env
# YouTube Data API v3 (optional)
YOUTUBE_API_KEY=

# Default settings
DEFAULT_LANGUAGE=auto
DEFAULT_OUTPUT_MODE=print
DEFAULT_TASK_TYPE=recommend_then_recipe
DEFAULT_RECOMMENDATION_COUNT=10
DEFAULT_MAX_REVISIONS=3
DEFAULT_APPROVAL_THRESHOLD=0.85
DEFAULT_RECOMMENDATION_THRESHOLD=0.80
DEFAULT_INCLUDE_VIDEO_URLS=false
DEFAULT_MAX_VIDEO_URLS=5
```

## Usage

### Basic Usage (recommend_then_recipe - default)

```bash
PYTHONPATH=src python -m recipe_agent.main \
  --request "Saya mau makanan simple yang bahannya bisa saya temukan di Alfamart terdekat"
```

This will:
1. Generate 10 recommendations
2. Critique the recommendations
3. Select the best one
4. Generate a full recipe
5. Critique and revise the recipe
6. Output the final result

### Recommendations Only

```bash
PYTHONPATH=src python -m recipe_agent.main \
  --request "Give me 10 simple drink ideas from minimarket ingredients" \
  --task-type recommendations_only
```

### Recipe Only (for a specific dish)

```bash
PYTHONPATH=src python -m recipe_agent.main \
  --request "Make me a recipe for mie telur keju pedas" \
  --task-type recipe_only
```

### Markdown Output

```bash
PYTHONPATH=src python -m recipe_agent.main \
  --request "Quick breakfast recipe" \
  --output-mode markdown
```

### Custom Settings

```bash
PYTHONPATH=src python -m recipe_agent.main \
  --request "Simple dinner ideas" \
  --max-revisions 5 \
  --language en
```

## Example Requests

**English:**
- "I need a quick dinner recipe under 30 minutes"
- "Give me 10 simple food ideas from Alfamart"
- "Make me a recipe for iced coffee"
- "What should I eat today?" (triggers clarification_needed)

**Bahasa Indonesia:**
- "Saya mau makanan simple yang bahannya bisa saya temukan di Alfamart terdekat"
- "Beri saya 10 ide minuman sederhana"
- "Buatkan resep mie telur keju pedas"
- "Resep sarapan yang cepat dan mudah"

## Output Formats

### Recommendations Only
```markdown
# Food and Drink Recommendations

Based on your request, here are the recommendations:

1. **Simple Egg Noodles** (Food)
   - 15 minutes
   - Quick and easy
```

### Recommend Then Recipe
```markdown
# Best Recommendation: Mie Telur Keju Pedas

## Why This Was Selected

From the recommendations, this recipe best matches your request because it uses simple ingredients available at Alfamart.

## Recommendation Shortlist

1. Mie Telur Keju Pedas
2. Roti Telur Mayo
...

## Full Recipe

# Mie Telur Keju Pedas

## Why This Recipe Fits
...

## Ingredients
...

## Steps
...
```

### Recipe Only
```markdown
# Mie Telur Keju Pedas

## Why This Recipe Fits
...

## Ingredients
...

## Steps
...
```

## Critique Scoring Rubrics

### Recipe Critique

| Criterion | Weight |
|-----------|--------|
| Matches user intent | 25% |
| Ingredient availability | 20% |
| Simplicity | 15% |
| Clarity of steps | 15% |
| Practicality / cooking time | 10% |
| Safety and food handling | 10% |
| Language quality | 5% |

### Recommendation Critique

| Criterion | Weight |
|-----------|--------|
| Matches user intent | 30% |
| Ingredient availability | 25% |
| Simplicity | 20% |
| Diversity | 10% |
| Practicality | 10% |
| Language quality | 5% |

## Project Structure

```
langgraph-recipe-agent/
├── pyproject.toml                  # Package configuration
├── .env.example                    # Environment template
├── data/
│   └── common_alfamart_ingredients.yaml  # Local ingredient knowledge base
├── outputs/                        # Generated recipes (if OUTPUT_MODE=markdown)
├── src/
│   └── recipe_agent/
│       ├── __init__.py
│       ├── main.py                # CLI entry point
│       ├── graph.py               # LangGraph workflow with conditional routing
│       ├── state.py               # State schema with TaskType
│       ├── config.py              # Configuration loader
│       ├── nodes/                 # 10 graph nodes
│       │   ├── parse_input.py
│       │   ├── decide_task.py
│       │   ├── generate_recommendations.py
│       │   ├── critique_recommendations.py
│       │   ├── select_best_recommendation.py
│       │   ├── generate_recipe.py
│       │   ├── critique_recipe.py
│       │   ├── revise_recipe.py
│       │   ├── fetch_youtube_videos.py
│       │   └── render_output.py
│       ├── tools/                 # Utility modules
│       │   ├── llm.py
│       │   ├── language.py
│       │   ├── ingredient_store.py
│       │   ├── youtube_search.py
│       │   └── markdown_writer.py
│       └── prompts/               # 7 prompt templates
│           ├── parse_input.md
│           ├── decide_task.md
│           ├── generate_recommendations.md
│           ├── critique_recommendations.md
│           ├── select_best_recommendation.md
│           ├── generate_recipe.md
│           ├── critique_recipe.md
│           └── revise_recipe.md
└── tests/                         # Test suite (23 tests)
    ├── test_graph.py
    ├── test_decide_task.py
    ├── test_recommendations.py
    ├── test_critique.py
    ├── test_youtube_optional.py
    └── test_markdown_writer.py
```

## Testing

Run the test suite:

```bash
PYTHONPATH=src pytest tests/ -v
```

All 23 tests should pass:
- Graph creation and routing tests
- Task decision logic tests
- Recommendation generation and structure tests
- Critique threshold logic tests
- YouTube optional behavior tests
- Markdown rendering tests for all 3 output formats

## Design Principles

- **KISS**: Simple, straightforward implementation
- **DRY**: Reusable components and utilities
- **YAGNI**: MVP focuses on core functionality
- **SOLID**: Modular design with clear separation of concerns
- **Graceful Degradation**: Works without YouTube API
- **Testable**: Each node is independently testable
- **Fail-Safe**: External tool failures don't break core recipe generation

## Development Phases Completed

✅ **Phase 1: Core Task Router**
- parse_input, decide_task, render_output

✅ **Phase 2: Recommendation Flow**
- generate_recommendations, critique_recommendations

✅ **Phase 3: Recommend Then Recipe Flow**
- select_best_recommendation, generate_recipe, critique_recipe, revise_recipe

✅ **Phase 4: Local Ingredient Knowledge Base**
- data/common_alfamart_ingredients.yaml, ingredient_store.py

✅ **Phase 5: Markdown Output**
- markdown_writer.py with 3 output formats, outputs/ directory

✅ **Phase 6: Optional YouTube API**
- youtube_search.py, fetch_youtube_videos node

## Acceptance Criteria

- ✅ App can run from CLI
- ✅ LangGraph flow works end-to-end with conditional routing
- ✅ decide_task node correctly routes common requests
- ✅ Agent generates 10 recommendations by default
- ✅ Agent can return recommendations only
- ✅ Agent can generate a direct recipe only
- ✅ Agent can generate recommendations first, then select one and create a recipe
- ✅ Recipe can be generated in English or Bahasa Indonesia
- ✅ Critique loop stops correctly
- ✅ Max revision limit works
- ✅ Markdown output mode works with 3 different formats
- ✅ App still works without YOUTUBE_API_KEY
- ✅ YouTube video recommendations included only when configured
- ✅ Tests cover task routing, recommendation count, and optional YouTube behavior (23 tests)
- ✅ README explains setup clearly

## Future Enhancements (Phase 7+)

- External recipe APIs (TheMealDB, DDGS)
- Advanced web scraping
- Additional store knowledge bases (Indomaret, local markets)
- User preference learning
- Recipe difficulty scaling

## License

MIT
