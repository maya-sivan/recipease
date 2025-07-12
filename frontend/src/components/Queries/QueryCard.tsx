import { Card } from "antd";
import clsx from "clsx";
import type { Query } from "../../types";
import { InfoTag } from "../shared/InfoTag";
import { TextBox } from "../shared/TextBox";

export function QueryCard({
	query,
	className,
	onClick,
}: {
	query: Query;
	className?: string;
	onClick?: () => void;
}) {
	return (
		<Card
			title={query.created_at.toLocaleString()}
			className={clsx(className, "cursor-pointer")}
			onClick={onClick}
		>
			<div className="flex flex-col gap-2">
				<TextBox text={query.query} className="max-h-40" />
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
		</Card>
	);
}
