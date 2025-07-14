import { Empty, Spin } from "antd";
import { useNavigate } from "react-router-dom";
import { useAllQueries } from "../../api";
import { ROUTES } from "../../constants";
import { QueryCard } from "./QueryCard";

export function QueriesPage() {
	const { data, isLoading } = useAllQueries();
	const navigate = useNavigate();

	return (
		<>
			{isLoading ? (
				<div className="flex justify-center items-center h-screen">
					<Spin size="large" />
				</div>
			) : data && data.length === 0 ? (
				<div className="flex justify-center items-center h-screen">
					<Empty description="No queries found" />
				</div>
			) : (
				<div className="flex flex-wrap gap-4 justify-center py-20">
					{data?.map((query) => (
						<QueryCard
							key={query._id}
							query={query}
							className="w-150 h-70"
							onClick={() => {
								navigate(`${ROUTES.queries}/${query._id}`);
							}}
						/>
					))}
				</div>
			)}
		</>
	);
}
