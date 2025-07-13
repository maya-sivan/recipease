from shared.models import Recipe

def recipe_to_text(recipe: Recipe):
    return f"""
    {recipe.recipe_content.recipe_title}

    Found at: {recipe.found_at.isoformat()}

    Recipe:
    {recipe.recipe_content.modified_recipe_content}
    
    System notes:
    {recipe.recipe_content.notes}

 
    Original recipe URL: {recipe.recipe_content.original_page_url}


    Preferences: {", ".join(recipe.recipe_content.relevant_preferences)}
    Restrictions: {", ".join(recipe.restrictions)}

    """