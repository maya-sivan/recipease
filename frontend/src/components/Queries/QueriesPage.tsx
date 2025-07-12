import { Button, Spin } from "antd";
import { useAtom } from "jotai";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAllQueries } from "../../api";
import { bgJobAtom } from "../../atoms/bgJobAtom";
import { ROUTES } from "../../constants/routes";
import { BackgroundJobPanel } from "../BgJobPanel";
import { CreateNewQueryModal } from "./CreateNewQueryModal";
import { QueryCard } from "./QueryCard";

export function RequestsPage() {
	const { data, isLoading } = useAllQueries();
	const navigate = useNavigate();
	const [isCreateNewQueryModalOpen, setIsCreateNewQueryModalOpen] =
		useState(false);
	const [bgJobId] = useAtom(bgJobAtom);
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
			{!!bgJobId && <BackgroundJobPanel bgJobId={bgJobId.jobId} />}
			<CreateNewQueryModal
				open={isCreateNewQueryModalOpen}
				onCancel={() => setIsCreateNewQueryModalOpen(false)}
			/>
		</div>
	);
}
