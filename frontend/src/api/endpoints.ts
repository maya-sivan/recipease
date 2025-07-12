import { useQuery } from "@tanstack/react-query";
import { getAllQueries, getAllRecipes } from "./api-functions";

function useAllRecipes() {
	return useQuery({
		queryKey: ["recipes"],
		queryFn: getAllRecipes,
	});
}

function useAllQueries() {
	return useQuery({
		queryKey: ["queries"],
		queryFn: getAllQueries,
	});
}

export { useAllRecipes, useAllQueries };
