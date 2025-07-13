import {
	CheckCircleOutlined,
	CloseCircleOutlined,
	SyncOutlined,
} from "@ant-design/icons";
import { Button, Drawer, FloatButton, Spin } from "antd";
import { useAtom } from "jotai";
import { useState } from "react";
import { useGetAllBgJobs, useUpdateBgJobResolved } from "../api";
import { unresolvedBgJobIdAtom } from "../atoms/bgJobAtom";
import { BgJobStatus } from "../types/BackendTypes";

export function BackgroundJobPanel() {
	const [, setUnresolvedBgJobIds] = useAtom(unresolvedBgJobIdAtom);
	const {
		data: unresolvedBgJobs,
		isPending,
		isLoading,
	} = useGetAllBgJobs({ is_resolved: false });

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

	const renderContent = () => {
		if (isPending || isLoading) return <Spin tip="Checking..." />;
		return (
			<div className="flex flex-col gap-2">
				{unresolvedBgJobs.map((job) => (
					<div key={job.job_id} className="flex justify-between px-40">
						<span className="w-50 overflow-hidden text-ellipsis whitespace-nowrap">
							{job.query}
						</span>
						{job.status === BgJobStatus.Running && <SyncOutlined spin />}
						{job.status === BgJobStatus.Completed && <CheckCircleOutlined />}
						{job.status === BgJobStatus.Failed && <CloseCircleOutlined />}
						<Button
							onClick={() => {
								updateBgJobResolved({
									jobId: job.job_id,
									isUserResolved: true,
								});
								setUnresolvedBgJobIds((prev) =>
									prev.filter((id) => id !== job.job_id),
								);
							}}
						>
							Resolve
						</Button>
					</div>
				))}
			</div>
		);
	};

	return (
		<>
			<Drawer
				title="Background Job"
				placement="bottom"
				height={150}
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
