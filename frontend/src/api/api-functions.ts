import type { BgJob, Query, Recipe } from "../types";

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

async function getQueryById(id: string): Promise<Query> {
	const response = await fetch(`${BACKEND_API_URL}/query/${id}`);
	if (!response.ok) {
		throw new Error("Failed to fetch query");
	}
	return await response.json();
}

async function getRecipesByQueryId(queryId: string): Promise<Recipe[]> {
	const response = await fetch(`${BACKEND_API_URL}/recipe/by-query/${queryId}`);
	if (!response.ok) {
		throw new Error("Failed to fetch recipes");
	}
	return await response.json();
}

async function createNewQueryBgJob(
	userEmail: string,
	query: string,
): Promise<{ job_id: string }> {
	const response = await fetch(`${BACKEND_API_URL}/query/create-new-bg-job`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ user_email: userEmail, query }),
	});
	if (!response.ok) {
		throw new Error("Failed to create new query background job");
	}
	return await response.json();
}

async function getBgJob(jobId: string): Promise<BgJob> {
	const response = await fetch(
		`${BACKEND_API_URL}/query/bg-job-status/${jobId}`,
	);
	if (!response.ok) {
		throw new Error("Failed to get job status");
	}
	return await response.json();
}

export {
	getAllRecipes,
	getAllQueries,
	getQueryById,
	getRecipesByQueryId,
	createNewQueryBgJob,
	getBgJob,
};
