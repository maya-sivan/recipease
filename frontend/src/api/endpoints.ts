import { useQuery } from "@tanstack/react-query";
import { getAllRecipes } from "./api-functions";

function useAllRecipes() {
	return useQuery({
		queryKey: ["recipes"],
		queryFn: getAllRecipes,
	});
}

export { useAllRecipes };
