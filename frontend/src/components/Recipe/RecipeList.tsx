import { useState } from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import { useInfiniteRecipes } from "../../api";
import type { Recipe } from "../../types";
import { RecipeCard } from "./RecipeCard";
import { RecipeModal } from "./RecipeModal";

export function RecipeList({ recipes }: { recipes: Recipe[] }) {
	const [selectedRecipe, setSelectedRecipe] = useState<Recipe | null>(null);

	return (
		<div className="flex flex-wrap gap-4 justify-center py-20">
			{recipes?.map((recipe) => (
				<RecipeCard
					key={recipe._id}
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

export function InfiniteRecipeList() {
	const [selectedRecipe, setSelectedRecipe] = useState<Recipe | null>(null);
	const { data, fetchNextPage, hasNextPage, isFetchingNextPage, isLoading } =
		useInfiniteRecipes();

	const allRecipes = data?.pages.flatMap((page: Recipe[]) => page) ?? [];

	return (
		<div className="flex flex-col items-center py-20">
			{isLoading ? (
				<div className="flex justify-center items-center h-screen">
					<div className="text-center py-4">Loading recipes...</div>
				</div>
			) : (
				<InfiniteScroll
					dataLength={allRecipes.length}
					next={fetchNextPage}
					hasMore={hasNextPage ?? false}
					loader={
						isFetchingNextPage ? (
							<div className="text-center py-4">Loading more recipes...</div>
						) : null
					}
					endMessage={
						<div className="text-center py-4 text-gray-500">
							No more recipes to load.
						</div>
					}
					scrollThreshold={0.8}
				>
					<div className="flex flex-wrap gap-4 justify-center">
						{allRecipes?.map((recipe) => (
							<RecipeCard
								key={recipe._id}
								recipe={recipe}
								className="w-100 h-100"
								onClick={() => {
									setSelectedRecipe(recipe);
								}}
							/>
						))}
					</div>
				</InfiniteScroll>
			)}
			<RecipeModal
				recipe={selectedRecipe}
				onCancel={() => setSelectedRecipe(null)}
			/>
		</div>
	);
}
