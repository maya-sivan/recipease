import { Form, Input, Modal } from "antd";
import { useStartNewQueryBgJob } from "../../api";

export function CreateNewQueryModal({
	open,
	onCancel,
}: {
	open: boolean;
	onCancel: () => void;
}) {
	const [form] = Form.useForm();

	const startNewQueryBgJob = useStartNewQueryBgJob();

	const handleOk = async () => {
		try {
			const values = await form.validateFields();
			startNewQueryBgJob.mutate({
				userEmail: "mayasivannj@gmail.com",
				query: values.query,
			});
		} catch (err) {
			// validation error; do nothing
		}
	};

	return (
		<Modal
			title="Create New Query"
			open={open}
			onCancel={onCancel}
			onOk={handleOk}
			confirmLoading={startNewQueryBgJob.isPending}
		>
			<Form form={form} layout="vertical">
				<Form.Item
					label="Query"
					name="query"
					rules={[{ required: true, message: "Please enter a query" }]}
				>
					<Input placeholder="e.g. Find apartments in NYC" />
				</Form.Item>
			</Form>
		</Modal>
	);
}
