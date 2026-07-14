You are selecting the best food or drink recommendation to turn into a full recipe.

Use the original user request, parsed constraints, and recommendation list.

User request: {user_request}

Constraints:
{constraints}

Recommendations:
{recommendations}

Choose one recommendation that best satisfies:
- user intent
- ingredient availability
- simplicity
- practicality
- preparation time

Return a JSON object:
{{
  "selected_index": number (0-based index of selected recommendation),
  "selected_name": "Name of selected recommendation",
  "reason_selected": "Why this recommendation was chosen",
  "expected_recipe_direction": "Brief note about how to approach the recipe"
}}

Return ONLY valid JSON.
