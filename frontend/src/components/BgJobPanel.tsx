import {
	CheckCircleOutlined,
	CloseCircleOutlined,
	SyncOutlined,
} from "@ant-design/icons";
import { Badge, Button, Drawer, FloatButton, Spin, Table } from "antd";
import { useAtom } from "jotai";
import { useState } from "react";
import {
	useGetAllBgJobs,
	useGetBgJobsCount,
	useUpdateBgJobResolved,
} from "../api";
import { unresolvedBgJobIdAtom } from "../atoms/bgJobAtom";
import type { DataQueryParams } from "../types";
import { type BgJob, BgJobStatus } from "../types/BackendTypes";

export function BackgroundJobPanel() {
	const [, setUnresolvedBgJobIds] = useAtom(unresolvedBgJobIdAtom);
	const [tableParams, setTableParams] = useState<DataQueryParams>({
		skip: 0,
		limit: 5,
	});

	console.log(tableParams);
	const filters = { is_resolved: false };
	const {
		data: unresolvedBgJobs,
		isPending,
		isLoading,
	} = useGetAllBgJobs({
		filters,
		tableParams,
	});

	const { data: bgJobsCount } = useGetBgJobsCount(filters);

	const { mutate: updateBgJobResolved } = useUpdateBgJobResolved();
	const [open, setOpen] = useState(
		!!unresolvedBgJobs && unresolvedBgJobs.length > 0,
	);
	if (!unresolvedBgJobs || unresolvedBgJobs.length === 0) return null;

	const allJobsCompleted = unresolvedBgJobs.every(
		(job) => job.status === BgJobStatus.Completed,
	);

	const anyJobRunning = unresolvedBgJobs.some(
		(job) => job.status === BgJobStatus.Running,
	);

	// Badge status logic
	const floatButonIcon = anyJobRunning ? (
		<SyncOutlined />
	) : allJobsCompleted ? (
		<CheckCircleOutlined />
	) : (
		<CloseCircleOutlined />
	);

	const columns = [
		{
			title: "Query",
			dataIndex: "query",
			key: "query",
		},
		{
			title: "Created At",
			dataIndex: "created_at",
			key: "created_at",
			render: (_: unknown, bgJob: BgJob) => (
				<span>{new Date(bgJob.created_at).toLocaleString()}</span>
			),
		},
		{
			title: "Status",
			dataIndex: "status",
			key: "status",
			render: (_: unknown, bgJob: BgJob) => (
				<Badge
					status={
						bgJob.status === BgJobStatus.Running
							? "processing"
							: bgJob.status === BgJobStatus.Completed
								? "success"
								: "error"
					}
				>
					{bgJob.status.charAt(0).toUpperCase() + bgJob.status.slice(1)}
				</Badge>
			),
		},
		{
			title: "Actions",
			key: "actions",
			render: (_: unknown, bgJob: BgJob) => (
				<Button
					onClick={() => {
						updateBgJobResolved({
							jobId: bgJob.job_id,
							isUserResolved: true,
						});
						setUnresolvedBgJobIds((prev) =>
							prev.filter((id) => id !== bgJob.job_id),
						);
					}}
				>
					Resolve
				</Button>
			),
		},
	];

	const renderContent = () => {
		if (isPending || isLoading) return <Spin tip="Checking..." />;
		return (
			<Table
				dataSource={unresolvedBgJobs}
				columns={columns}
				pagination={{
					pageSize: tableParams.limit,
					hideOnSinglePage: true,
					total: bgJobsCount,
					onChange: (page, pageSize) => {
						setTableParams({ skip: (page - 1) * pageSize, limit: pageSize });
					},
					pageSizeOptions: [5, 10, 20, 50, 100],
				}}
			/>
		);
	};

	return (
		<>
			<Drawer
				title="Background Job"
				placement="bottom"
				height={600}
				open={open}
				onClose={() => {
					setOpen(false);
				}}
				closable
			>
				{renderContent()}
			</Drawer>

			{!open && (
				<FloatButton
					type="default"
					description="Job"
					onClick={() => setOpen(true)}
					style={{
						right: 24,
						bottom: 100,
					}}
					icon={floatButonIcon}
					shape="square"
				/>
			)}
		</>
	);
}
