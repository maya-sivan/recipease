import { Spin } from "antd";
import { useNavigate } from "react-router-dom";
import { useAllQueries } from "../../api";
import { ROUTES } from "../../constants/routes";
import { QueryCard } from "./QueryCard";

export function RequestsPage() {
	const { data, isLoading } = useAllQueries();
	const navigate = useNavigate();
	if (isLoading) return <Spin />;
	return (
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
	);
}
