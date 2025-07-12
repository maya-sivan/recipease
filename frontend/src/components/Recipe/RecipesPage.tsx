import { Space, Spin } from "antd";
import { useState } from "react";
import { useAllRecipes } from "../../api";
import type { Recipe } from "../../types";
import { RecipeCard } from "./RecipeCard";
import { RecipeModal } from "./RecipeModal";

export function RecipesPage() {
	const { data, isLoading } = useAllRecipes();
	const [selectedRecipe, setSelectedRecipe] = useState<Recipe | null>(null);

	if (isLoading) return <Spin />;

	return (
		<div className="flex flex-wrap gap-4">
			{data?.map((recipe, index) => (
				<RecipeCard
					key={index}
					recipe={recipe}
					className="w-150 h-90"
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
