import { useMutation, useQuery } from "@tanstack/react-query";
import { useAtom } from "jotai";
import { bgJobAtom } from "../atoms/bgJobAtom";
import {
	createNewQueryBgJob,
	getAllQueries,
	getAllRecipes,
	getBgJob,
	getQueryById,
	getRecipesByQueryId,
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

function useStartNewQueryBgJob() {
	const [, setJobId] = useAtom(bgJobAtom);
	return useMutation({
		mutationFn: ({ userEmail, query }: { userEmail: string; query: string }) =>
			createNewQueryBgJob(userEmail, query),
		onSuccess: (id) => setJobId({ jobId: id.jobId }),
	});
}

function useGetQueryBgJob(jobId: string) {
	return useQuery({
		queryKey: ["jobStatus", jobId],
		queryFn: () => getBgJob(jobId),
		refetchInterval: 2000,
	});
}

export {
	useAllRecipes,
	useAllQueries,
	useGetQueryById,
	useGetRecipesByQueryId,
	useGetQueryBgJob,
	useStartNewQueryBgJob,
};
