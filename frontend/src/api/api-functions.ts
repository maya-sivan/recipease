import type { ModifiedRecipeContent, Query, Recipe } from "../types";

const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

async function getAllRecipes(): Promise<Recipe[]> {
	const response = await fetch(`${BACKEND_API_URL}/recipe/all`);
	if (!response.ok) {
		throw new Error("Failed to fetch recipes");
	}
	return await response.json();
}

async function getAllQueries(): Promise<Query[]> {
	const response = await fetch(`${BACKEND_API_URL}/query/all`);
	if (!response.ok) {
		throw new Error("Failed to fetch queries");
	}
	return await response.json();
}

export { getAllRecipes, getAllQueries };
