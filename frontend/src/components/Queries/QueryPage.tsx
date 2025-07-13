import { Spin, Typography } from "antd";
import { useParams } from "react-router-dom";
import { useGetQueryById, useGetRecipesByQueryId } from "../../api/endpoints";
import { RecipeList } from "../Recipe";
import { InfoTag, TextBox } from "../shared";

export function QueryPage() {
	const { id } = useParams();
	const { data: query } = useGetQueryById(id ?? "");
	const { data: queryRecipes, isLoading: isLoadingRecipes } =
		useGetRecipesByQueryId(id ?? "");
	return (
		<div>
			<Typography.Title level={2}>
				{query?.created_at.toLocaleString()}
			</Typography.Title>
			<TextBox text={query?.query ?? ""} />

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

			{isLoadingRecipes ? (
				<Spin />
			) : (
				<RecipeList recipes={queryRecipes ?? []} />
			)}
		</div>
	);
}
