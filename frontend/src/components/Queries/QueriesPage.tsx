import { Button, Spin } from "antd";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAllQueries } from "../../api";
import { ROUTES } from "../../constants";
import { CreateNewQueryModal } from "./CreateNewQueryModal";
import { QueryCard } from "./QueryCard";

export function QueriesPage() {
	const { data, isLoading } = useAllQueries();
	const navigate = useNavigate();
	const [isCreateNewQueryModalOpen, setIsCreateNewQueryModalOpen] =
		useState(false);
	if (isLoading) return <Spin />;
	return (
		<div>
			<Button onClick={() => setIsCreateNewQueryModalOpen(true)}>
				Create New Query
			</Button>
			<div className="flex flex-wrap gap-4">
				{data?.map((query, index) => (
					<QueryCard
						key={index}
						query={query}
						className="w-150 h-90"
						onClick={() => {
							navigate(`${ROUTES.queries}/${query._id}`);
						}}
					/>
				))}
			</div>
			<CreateNewQueryModal
				open={isCreateNewQueryModalOpen}
				onCancel={() => setIsCreateNewQueryModalOpen(false)}
			/>
		</div>
	);
}
