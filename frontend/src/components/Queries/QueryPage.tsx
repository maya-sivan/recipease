import { Modal, Typography } from "antd";
import type { Query } from "../../types";
import { InfoTag } from "../shared/InfoTag";
import { TextBox } from "../shared/TextBox";

export function QueryModal({
	query,
	onCancel,
}: {
	query: Query | null;
	onCancel: () => void;
}) {
	return (
		<Modal open={!!query} onCancel={onCancel} footer={null}>
			<div>
				<Typography.Title level={2}>
					{query?.created_at.toLocaleString()}
				</Typography.Title>
				<TextBox text={query?.query ?? ""} />

				<div className="flex gap-2 flex-col my-4">
					<InfoTag
						title="Preferences"
						values={query?.user_info.preferences ?? []}
					/>
					<InfoTag
						title="Restrictions"
						values={query?.user_info.restrictions ?? []}
					/>
				</div>
			</div>
		</Modal>
	);
}
