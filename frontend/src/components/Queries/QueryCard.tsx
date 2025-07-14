import { DeleteOutlined } from "@ant-design/icons";
import { Button, Card, Popconfirm, Space } from "antd";
import { useDeleteQuery } from "../../api/endpoints";
import type { Query } from "../../types";
import { formatDate } from "../../utils";
import { InfoTag, TextBox } from "../shared";

export function QueryCard({
	query,
	className,
	onClick,
}: {
	query: Query;
	className?: string;
	onClick?: () => void;
}) {
	const { mutate: deleteQuery } = useDeleteQuery();
	return (
		<Card
			title={
				<div className="flex flex-row gap-2 justify-between w-full">
					Created at: {formatDate(query.created_at)}
					<Popconfirm
						title="Delete the query"
						description="Are you sure to delete this query?"
						okText="Yes"
						cancelText="No"
						onConfirm={() => {
							deleteQuery(query._id);
						}}
					>
						<Button type="primary" danger icon={<DeleteOutlined />} />
					</Popconfirm>
				</div>
			}
			className={className}
		>
			<Space
				onClick={onClick}
				className="flex flex-col gap-2 hover:opacity-70 cursor-pointer"
			>
				<div>
					<TextBox text={query.query} className="max-h-40 overflow-y-scroll" />
					<InfoTag
						title="Restrictions"
						values={query.user_info.restrictions}
						color="#68768c"
					/>
					<InfoTag
						title="Preferences"
						values={query.user_info.preferences}
						color="#adb7c7"
					/>
				</div>
			</Space>
		</Card>
	);
}
