import {
	CheckCircleOutlined,
	CloseCircleOutlined,
	SyncOutlined,
} from "@ant-design/icons";
import { Alert, Drawer, FloatButton, Spin } from "antd";
import { useAtom } from "jotai";
import { useEffect, useState } from "react";
import { useGetQueryBgJob } from "../api";
import { bgJobAtom } from "../atoms/bgJobAtom";
import { BgJobStatus } from "../types/BackendTypes";

export function BackgroundJobPanel({ bgJobId }: { bgJobId: string }) {
	const [open, setOpen] = useState(true);

	const { data: bgJob, isLoading: isLoadingBgJob } = useGetQueryBgJob(bgJobId);
	const [, setBgJobId] = useAtom(bgJobAtom);

	useEffect(() => {
		if (bgJob?.status === BgJobStatus.Completed) {
			setBgJobId(null);
		}
	}, [bgJob, setBgJobId]);

	const { status } = bgJob || {};

	// Badge status logic
	const floatButonIcon =
		status === BgJobStatus.Running ? (
			<SyncOutlined />
		) : status === BgJobStatus.Completed ? (
			<CheckCircleOutlined />
		) : (
			<CloseCircleOutlined />
		);

	const renderContent = () => {
		if (isLoadingBgJob) return <Spin tip="Checking..." />;
		if (status === BgJobStatus.Running) return <Spin tip="Job is running..." />;
		if (status === BgJobStatus.Completed)
			return <Alert message="Job completed" type="success" showIcon />;

		return null;
	};

	return (
		<>
			<Drawer
				title="Background Job"
				placement="bottom"
				height={120}
				open={open}
				onClose={() => setOpen(false)}
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
				/>
			)}
		</>
	);
}
