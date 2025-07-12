import { Button, Spin } from "antd";
import { useAtom } from "jotai";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAllQueries, useGetBgJob } from "../../api";
import { bgJobIdAtom } from "../../atoms/bgJobAtom";
import { ROUTES } from "../../constants/routes";
import { BackgroundJobPanel } from "../BgJobPanel";
import { CreateNewQueryModal } from "./CreateNewQueryModal";
import { QueryCard } from "./QueryCard";

export function RequestsPage() {
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
			<BackgroundJobPanel />
			<CreateNewQueryModal
				open={isCreateNewQueryModalOpen}
				onCancel={() => setIsCreateNewQueryModalOpen(false)}
			/>
		</div>
	);
}
