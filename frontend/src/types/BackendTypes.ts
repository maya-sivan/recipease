export type Query = {
	_id: string;
	user_email: string;
	query: string;
	user_info: UserInfo;
	created_at: Date;
};

export type Recipe = {
	query_id: string;
	recipe_content: ModifiedRecipeContent;
	restrictions: string[];
	found_at: Date;
};

export type UserInfo = {
	preferences: string[];
	restrictions: string[];
};

export type ModifiedRecipeContent = {
	original_page_url: string;
	modified_recipe_content: string;
	notes: string;
	image_url?: string;
	recipe_title: string;
	relevant_preferences: string[];
};
