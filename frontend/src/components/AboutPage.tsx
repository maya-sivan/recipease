import {
	ClockCircleOutlined,
	SearchOutlined,
	SmileOutlined,
	UploadOutlined,
} from "@ant-design/icons";
import { Typography } from "antd";

export function AboutPage() {
	return (
		<div className="flex flex-col gap-4 p-4 max-w-2xl mx-auto justify-center">
			<Typography.Title className="text-center" level={2}>
				Welcome to RecipEase!
			</Typography.Title>
			<Typography.Text>
				Are you a foodie who loves to cook but also wants to eat healthy? Are
				you busy and don't want to spend hours searching for recipes that match
				your dietary needs? This site is for you!
			</Typography.Text>
			<Typography.Text>
				RecipEase is a tool that helps you tailor your food obsessions to your
				dietary needs.
			</Typography.Text>
			<Typography.Text>
				All you have to do is enter your wish and we will grant it{" "}
				<SmileOutlined />
			</Typography.Text>
			<Typography.Text>
				Not only will you get a recipe today, but your query will be saved into
				our system and generate relevant recipes daily! <ClockCircleOutlined />
			</Typography.Text>
			<Typography.Text>
				To get started, click on the "Create New Query" button in the top right
				corner. From there, you will be able to see all queries and the relevant
				recipes. <SearchOutlined />
			</Typography.Text>
			<Typography.Text>
				You can also export the recipes to a text file and share them with your
				friends! <UploadOutlined />
			</Typography.Text>
		</div>
	);
}
