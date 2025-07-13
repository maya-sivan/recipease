import { Card } from "antd";
import clsx from "clsx";
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
	return (
		<Card
			title={
				<div className="flex justify-center">
					Created at: {formatDate(query.created_at)}
				</div>
			}
			className={clsx(className, "cursor-pointer hover:opacity-70")}
			onClick={onClick}
		>
			<div className="flex flex-col gap-2">
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
		</Card>
	);
}
