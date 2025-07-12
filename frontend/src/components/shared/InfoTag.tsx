import { Tag } from "antd";

function InfoTag({
	title,
	values,
	color = "blue",
}: {
	title: string;
	values: string[];
	color?: string;
}) {
	return (
		<div>
			<span>{title}: </span>
			{values.length > 0 ? (
				values.map((value) => (
					<Tag color={color} key={value}>
						{value}
					</Tag>
				))
			) : (
				<span className="text-gray-500">None</span>
			)}
		</div>
	);
}

export { InfoTag };
