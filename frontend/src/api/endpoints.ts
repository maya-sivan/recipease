import { useMutation, useQuery } from "@tanstack/react-query";
import { useAtom } from "jotai";
import { unresolvedBgJobIdAtom } from "../atoms/bgJobAtom";
import { queryClient } from "../main";
import type { DataQueryParams, Recipe } from "../types";
import {
	createNewQueryBgJob,
	exportRecipe,
	getAllBgJobs,
	getAllQueries,
	getAllRecipes,
	getBgJob,
	getBgJobsCount,
	getQueryById,
	getRecipesByQueryId,
	updateBgJobResolved,
} from "./api-functions";

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

function useGetQueryById(id: string) {
	return useQuery({
		queryKey: ["query", id],
		queryFn: () => getQueryById(id),
	});
}

function useGetRecipesByQueryId(queryId: string) {
	return useQuery({
		queryKey: ["recipes", queryId],
		queryFn: () => getRecipesByQueryId(queryId),
	});
}

function useGetBgJob(jobId: string | undefined) {
	return useQuery({
		queryKey: ["bgJob", jobId],
		queryFn: () => getBgJob(jobId || ""),
		enabled: !!jobId,
		refetchInterval: 2000,
	});
}

function useStartNewQueryBgJob() {
	const [, setUnresolvedBgJobIds] = useAtom(unresolvedBgJobIdAtom);
	return useMutation({
		mutationFn: ({ userEmail, query }: { userEmail: string; query: string }) =>
			createNewQueryBgJob(userEmail, query),
		onSuccess: ({ job_id: jobId }) => {
			setUnresolvedBgJobIds((prev) => [...prev, jobId]);
			queryClient.invalidateQueries({ queryKey: ["bgJobs"] });
		},
	});
}

function useUpdateBgJobResolved() {
	return useMutation({
		mutationFn: ({
			jobId,
			isUserResolved,
		}: {
			jobId: string;
			isUserResolved: boolean;
		}) => updateBgJobResolved(jobId, isUserResolved),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ["bgJobs"] });
		},
	});
}

function useGetAllBgJobs({
	filters,
	tableParams,
}: {
	filters: Record<string, unknown>;
	tableParams: DataQueryParams;
}) {
	return useQuery({
		queryKey: ["bgJobs", filters, tableParams],
		queryFn: () => getAllBgJobs({ filters, tableParams }),
		placeholderData: (prev) => prev, // keep previous data for pagination
	});
}

function useGetBgJobsCount(filters: Record<string, unknown>) {
	return useQuery({
		queryKey: ["bgJobsCount", filters],
		queryFn: () => getBgJobsCount(filters),
	});
}

function useExportRecipe() {
	return useMutation({
		mutationFn: (recipe: Recipe) => exportRecipe(recipe),
	});
}

export {
	useAllRecipes,
	useAllQueries,
	useGetQueryById,
	useGetRecipesByQueryId,
	useGetBgJob,
	useStartNewQueryBgJob,
	useUpdateBgJobResolved,
	useGetAllBgJobs,
	useGetBgJobsCount,
	useExportRecipe,
};
