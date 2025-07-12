import { Spin, Typography } from "antd";
import { useState } from "react";
import { useAllQueries } from "../../api";
import type { Query } from "../../types";
import { QueryCard } from "./QueryCard";
import { QueryModal } from "./QueryPage";

export function RequestsPage() {
	const { data, isLoading } = useAllQueries();
	const [selectedQuery, setSelectedQuery] = useState<string | null>(null);
	if (isLoading) return <Spin />;

	return (
		<div className="flex flex-wrap gap-4">
			{data?.map((query, index) => (
				<QueryCard
					key={index}
					query={query}
					className="w-150 h-90"
					onClick={() => {
						setSelectedQuery(index); // TODO ref query id
					}}
				/>
			))}
		</div>
	);
}
