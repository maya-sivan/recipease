import { useState } from "react";
import type { Recipe } from "../../types";
import { RecipeCard } from "./RecipeCard";
import { RecipeModal } from "./RecipeModal";

export function RecipeList({ recipes }: { recipes: Recipe[] }) {
	const [selectedRecipe, setSelectedRecipe] = useState<Recipe | null>(null);

	return (
		<div className="flex flex-wrap gap-4 justify-center py-20">
			{recipes?.map((recipe, index) => (
				<RecipeCard
					key={index}
					recipe={recipe}
					className="w-100 h-100"
					onClick={() => {
						setSelectedRecipe(recipe);
					}}
				/>
			))}
			<RecipeModal
				recipe={selectedRecipe}
				onCancel={() => setSelectedRecipe(null)}
			/>
		</div>
	);
}
