import type { Recipe } from "../types";

const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

async function getAllRecipes(): Promise<Recipe[]> {
	const response = await fetch(`${BACKEND_API_URL}/recipe/all`);
	if (!response.ok) {
		throw new Error("Failed to fetch recipes");
	}
	return await response.json();
}

export { getAllRecipes };
