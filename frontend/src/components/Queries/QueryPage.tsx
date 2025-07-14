import { Spin, Typography } from "antd";
import { useParams } from "react-router-dom";
import { useGetQueryById, useGetRecipesByQueryId } from "../../api/endpoints";
import { formatDate } from "../../utils";
import { RecipeList } from "../Recipe";
import { InfoTag, TextBox } from "../shared";

export function QueryPage() {
	const { id } = useParams();
	const { data: query, isLoading: isLoadingQuery } = useGetQueryById(id ?? "");
	const { data: queryRecipes, isLoading: isLoadingRecipes } =
		useGetRecipesByQueryId(id ?? "");
	return (
		<>
			{isLoadingQuery || isLoadingRecipes ? (
				<div className="flex justify-center items-center h-screen">
					<Spin size="large" />
				</div>
			) : (
				<div className="flex justify-center flex-col p-20">
					<div className="flex flex-col gap-4 w-1/2">
						{query?.created_at && (
							<Typography.Title level={2}>
								Created at: {formatDate(query?.created_at)}
							</Typography.Title>
						)}

						<TextBox text={query?.query ?? ""} className="max-h-40 max-w-130" />

						<div className="flex gap-2 flex-col my-4">
							<InfoTag
								title="Preferences"
								values={query?.user_info.preferences ?? []}
							/>
							<InfoTag
								title="Restrictions"
								values={query?.user_info.restrictions ?? []}
							/>
						</div>
					</div>
					{isLoadingRecipes ? (
						<Spin />
					) : (queryRecipes?.length || 0) > 0 ? (
						<div className="flex flex-col gap-4 mt-10 items-start">
							<Typography.Title level={2}>Recipes</Typography.Title>
							<RecipeList recipes={queryRecipes ?? []} />
						</div>
					) : (
						<span>none</span>
					)}
				</div>
			)}
		</>
	);
}
