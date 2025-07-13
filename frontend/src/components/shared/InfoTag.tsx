import { Space, Tag, Tooltip } from "antd";

function InfoTag({
	title,
	values,
	color = "blue",
	className,
	limit = 2,
}: {
	title: string;
	values: string[];
	color?: string;
	className?: string;
	limit?: number;
}) {
	const visibleValues = values.slice(0, limit);
	const remainingCount = values.length - limit;
	const hasExtra = remainingCount > 0;

	const tooltipContent = (
		<div className="flex flex-wrap gap-2 max-h-60 max-w-60 overflow-y-auto">
			{values.map((value) => (
				<Tag
					color="white"
					key={value}
					style={{ color: "black", borderColor: "#d9d9d9" }}
				>
					{value}
				</Tag>
			))}
		</div>
	);

	return (
		<div className={className}>
			<span>{title}: </span>
			<div className="flex flex-wrap ">
				<Space size={4} wrap>
					{values.length > 0 ? (
						<>
							{visibleValues.map((value) => (
								<Tag color={color} key={value}>
									{value}
								</Tag>
							))}
							{hasExtra && (
								<Tooltip title={tooltipContent}>
									<Tag color={color}>+{remainingCount}</Tag>
								</Tooltip>
							)}
						</>
					) : (
						<span className="text-gray-500">None</span>
					)}
				</Space>
			</div>
		</div>
	);
}

export { InfoTag };
