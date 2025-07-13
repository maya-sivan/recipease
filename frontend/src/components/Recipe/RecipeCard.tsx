import { DownloadOutlined } from "@ant-design/icons";
import { Button, Card, Image, Typography } from "antd";
import clsx from "clsx";
import { useExportRecipe } from "../../api/endpoints";
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
	return (
		<Card
			title={
				<div className="flex flex-row gap-2">
					<Typography.Title
						level={4}
						className="flex justify-center text-center"
					>
						{recipe.recipe_content.recipe_title}
					</Typography.Title>
					<div className="flex justify-end">
						<Button
							type="primary"
							onClick={() => {
								exportRecipe(recipe);
							}}
							icon={<DownloadOutlined />}
						/>
					</div>
				</div>
			}
			className={clsx(className, "cursor-pointer")}
			onClick={onClick}
		>
			<div className="flex items-center justify-center flex-col hover:opacity-70">
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
			</div>
		</Card>
	);
}
