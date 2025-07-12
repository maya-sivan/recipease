import { useMutation, useQuery } from "@tanstack/react-query";
import { useAtom } from "jotai";
import { bgJobIdAtom } from "../atoms/bgJobAtom";
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

function useGetBgJob(jobId: string | undefined) {
	return useQuery({
		queryKey: ["bgJob", jobId],
		queryFn: () => getBgJob(jobId || ""),
		enabled: !!jobId,
	});
}

function useStartNewQueryBgJob() {
	const [, setBgJobId] = useAtom(bgJobIdAtom);
	return useMutation({
		mutationFn: ({ userEmail, query }: { userEmail: string; query: string }) =>
			createNewQueryBgJob(userEmail, query),
		onSuccess: ({ job_id: jobId }) => {
			console.log("setting bg job Id to ", jobId);
			setBgJobId(jobId);
		},
	});
}

export {
	useAllRecipes,
	useAllQueries,
	useGetQueryById,
	useGetRecipesByQueryId,
	useGetBgJob,
	useStartNewQueryBgJob,
};
