import type { BgJob, DataQueryParams, Query, Recipe } from "../types";

const BACKEND_PREFIX = import.meta.env.VITE_BACKEND_PREFIX;
const BACKEND_API_URL = `${window.location.origin}/${BACKEND_PREFIX}`;

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
	const response = await fetch(`${BACKEND_API_URL}/query/bg-job`, {
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
	const response = await fetch(`${BACKEND_API_URL}/query/bg-job/${jobId}`);
	if (!response.ok) {
		throw new Error("Failed to get job status");
	}
	return await response.json();
}

async function updateBgJobResolved(
	jobId: string,
	isUserResolved: boolean,
): Promise<BgJob> {
	const response = await fetch(
		`${BACKEND_API_URL}/query/bg-job/${jobId}/is-resolved`,
		{
			method: "PUT",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ is_user_resolved: isUserResolved }),
		},
	);
	if (!response.ok) {
		throw new Error("Failed to update job status");
	}
	return await response.json();
}

async function getAllBgJobs({
	filters,
	tableParams,
}: {
	filters: Record<string, unknown>;
	tableParams: DataQueryParams;
}): Promise<BgJob[]> {
	const { skip, limit } = tableParams;
	const response = await fetch(
		`${BACKEND_API_URL}/query/bg-jobs/all?skip=${skip}&limit=${limit}`,
		{
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(filters),
		},
	);
	if (!response.ok) {
		throw new Error("Failed to fetch bg jobs");
	}
	return await response.json();
}

async function getBgJobsCount(
	filters: Record<string, unknown>,
): Promise<number> {
	const response = await fetch(`${BACKEND_API_URL}/query/bg-jobs/count`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(filters),
	});
	if (!response.ok) {
		throw new Error("Failed to fetch bg jobs count");
	}
	return await response.json();
}

async function exportRecipe(recipe: Recipe): Promise<void> {
	try {
		const response = await fetch(`${BACKEND_API_URL}/recipe/export/txt`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(recipe),
		});

		if (!response.ok) {
			throw new Error(`Export failed: ${response.status}`);
		}

		const blob = await response.blob();
		let filename = "recipe.txt";
		const disposition = response.headers.get("Content-Disposition");
		if (disposition) {
			const match = disposition.match(/filename\*?=['"]?([^'";]+)['"]?/);
			if (match) {
				filename = decodeURIComponent(match[1]);
			}
		}

		const url = window.URL.createObjectURL(blob);
		const a = document.createElement("a");
		a.href = url;
		a.download = filename;
		document.body.appendChild(a);
		a.click();
		a.remove();
		window.URL.revokeObjectURL(url);
	} catch (err) {
		console.error("Download error:", err);
	}
}

async function deleteQuery(
	queryId: string,
): Promise<{ query_id: string; related_recipes_deleted_count: number }> {
	try {
		const response = await fetch(`${BACKEND_API_URL}/query/${queryId}`, {
			method: "DELETE",
		});
		if (!response.ok) {
			throw new Error("Failed to delete query");
		}
		return await response.json();
	} catch (err) {
		console.error("Delete query error:", err);
		throw err;
	}
}

async function deleteRecipe(recipeId: string): Promise<{ recipe_id: string }> {
	try {
		const response = await fetch(`${BACKEND_API_URL}/recipe/${recipeId}`, {
			method: "DELETE",
		});
		if (!response.ok) {
			throw new Error("Failed to delete recipe");
		}
		return await response.json();
	} catch (err) {
		console.error("Delete recipe error:", err);
		throw err;
	}
}

export {
	getAllRecipes,
	getAllQueries,
	getQueryById,
	getRecipesByQueryId,
	createNewQueryBgJob,
	getBgJob,
	updateBgJobResolved,
	getAllBgJobs,
	getBgJobsCount,
	exportRecipe,
	deleteQuery,
	deleteRecipe,
};
