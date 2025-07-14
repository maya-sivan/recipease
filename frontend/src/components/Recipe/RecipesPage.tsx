import { Empty, Spin } from "antd";
import { useAllRecipes } from "../../api";
import { RecipeList } from "./RecipeList";

export function RecipesPage() {
	const { data, isLoading } = useAllRecipes();

	return (
		<>
			{isLoading ? (
				<div className="flex justify-center items-center h-screen">
					<Spin size="large" />
				</div>
			) : data && data.length === 0 ? (
				<div className="flex justify-center items-center h-screen">
					<Empty description="No recipes found" />
				</div>
			) : (
				<RecipeList recipes={data ?? []} />
			)}
		</>
	);
}
