import { Spin } from "antd";
import { useAllRecipes } from "../../api";
import { RecipeList } from "./RecipeList";

export function RecipesPage() {
	const { data, isLoading } = useAllRecipes();

	if (isLoading) return <Spin />;

	return <RecipeList recipes={data ?? []} />;
}
