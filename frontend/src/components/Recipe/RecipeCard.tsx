import { DeleteOutlined, DownloadOutlined } from "@ant-design/icons";
import { Button, Card, Image, Popconfirm, Space, Typography } from "antd";
import clsx from "clsx";
import { deleteRecipe } from "../../api/api-functions";
import { useDeleteRecipe, useExportRecipe } from "../../api/endpoints";
import type { Recipe } from "../../types";
import { InfoTag } from "../shared";

export function RecipeCard({
	recipe,
	className,
	onClick,
}: {
	recipe: Recipe;
	className?: string;
	onClick?: () => void;
}) {
	const { mutate: exportRecipe } = useExportRecipe();
	const { mutate: deleteRecipe } = useDeleteRecipe();
	return (
		<Card
			title={
				<div className="flex flex-row gap-2 justify-between w-[80%]">
					<span className="truncate">{recipe.recipe_content.recipe_title}</span>
					<div className="flex gap-2">
						<Button
							type="primary"
							onClick={(e) => {
								e.stopPropagation();
								exportRecipe(recipe);
							}}
							icon={<DownloadOutlined />}
						/>
						<Popconfirm
							title="Delete the recipe"
							description="Are you sure to delete this recipe?"
							okText="Yes"
							cancelText="No"
							onConfirm={() => {
								deleteRecipe(recipe._id);
							}}
						>
							<Button type="primary" danger icon={<DeleteOutlined />} />
						</Popconfirm>
					</div>
				</div>
			}
			className={clsx(className, "flex flex-col items-center")}
		>
			<Space
				onClick={onClick}
				className="flex items-center justify-center flex-col hover:opacity-70 cursor-pointer"
			>
				<Image
					src={recipe.recipe_content.image_url}
					alt="Recipe Image"
					preview={false}
					className="object-cover"
					width={200}
					height={200}
				/>
				<div>
					<InfoTag
						title="Restrictions"
						values={recipe.restrictions}
						color="#68768c"
					/>
					<InfoTag
						title="Preferences"
						values={recipe.recipe_content.relevant_preferences}
						color="#adb7c7"
					/>
				</div>
			</Space>
		</Card>
	);
}
