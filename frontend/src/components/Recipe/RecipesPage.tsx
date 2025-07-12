import { Space, Spin } from "antd";
import { useState } from "react";
import { useAllRecipes } from "../../api";
import type { Recipe } from "../../types";
import { RecipeCard } from "./RecipeCard";
import { RecipeList } from "./RecipeList";
import { RecipeModal } from "./RecipeModal";

export function RecipesPage() {
	const { data, isLoading } = useAllRecipes();

	if (isLoading) return <Spin />;

	return <RecipeList recipes={data ?? []} />;
}
