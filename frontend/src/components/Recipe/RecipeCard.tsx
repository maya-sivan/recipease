import { Card, Image, Typography } from "antd";
import clsx from "clsx";
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
	return (
		<Card
			title={
				<Typography.Title level={4} className="flex justify-center text-center">
					{recipe.recipe_content.recipe_title}
				</Typography.Title>
			}
			className={clsx(className, "cursor-pointer hover:opacity-70")}
			onClick={onClick}
		>
			<div className="flex items-center justify-center flex-col">
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
