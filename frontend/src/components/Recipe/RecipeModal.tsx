import { Image, Modal, Typography } from "antd";
import ReactMarkdown from "react-markdown";
import type { Recipe } from "../../types";
import { InfoTag, TextBox } from "../shared";

export function RecipeModal({
	recipe,
	onCancel,
}: {
	recipe: Recipe | null;
	onCancel: () => void;
}) {
	return (
		<Modal open={!!recipe} onCancel={onCancel} footer={null}>
			<div>
				<Typography.Title level={2}>
					<a href={recipe?.recipe_content.original_page_url} target="_blank">
						{recipe?.recipe_content.recipe_title}
					</a>
				</Typography.Title>
				<ReactMarkdown>
					{recipe?.recipe_content.modified_recipe_content}
				</ReactMarkdown>
				System Notes:
				<TextBox text={recipe?.recipe_content.notes ?? ""} />
				<div className="flex gap-2 flex-col my-4">
					<InfoTag
						title="Preferences"
						values={recipe?.recipe_content.relevant_preferences ?? []}
					/>
					<InfoTag title="Restrictions" values={recipe?.restrictions ?? []} />
				</div>
				<div className="flex justify-center">
					<Image
						src={recipe?.recipe_content.image_url}
						alt="Recipe Image"
						width={200}
						height={200}
					/>
				</div>
			</div>
		</Modal>
	);
}
