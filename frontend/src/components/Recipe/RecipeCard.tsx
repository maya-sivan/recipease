import { Card, Image } from "antd";
import clsx from "clsx";
import type { Recipe } from "../../types";
import { InfoTag } from "../shared/InfoTag";

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
			title={recipe.recipe_content.recipe_title}
			className={clsx(className, "cursor-pointer")}
			onClick={onClick}
		>
			<Image
				src={recipe.recipe_content.image_url}
				alt="Recipe Image"
				preview={false}
				width={200}
				height={200}
			/>
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
		</Card>
	);
}
