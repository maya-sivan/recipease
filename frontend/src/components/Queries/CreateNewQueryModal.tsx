import { Form, Modal, Typography } from "antd";
import TextArea from "antd/es/input/TextArea";
import { useStartNewQueryBgJob } from "../../api";

export function CreateNewQueryModal({
	open,
	onCancel,
}: {
	open: boolean;
	onCancel: () => void;
}) {
	const [form] = Form.useForm();

	const { mutate: startNewQueryBgJob, isPending } = useStartNewQueryBgJob();

	const handleOk = async () => {
		try {
			const values = await form.validateFields();
			startNewQueryBgJob(
				{
					userEmail: "mayasivannj@gmail.com",
					query: values.query,
				},
				{
					onSuccess: () => {
						form.resetFields();
						onCancel();
					},
				},
			);
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
			confirmLoading={isPending}
			okText="Create"
			cancelText="Cancel"
		>
			<Typography.Paragraph>
				Please enter your food preferences and restrictions. Your query will be
				saved and start generating relevant recipes on a daily basis!
			</Typography.Paragraph>
			<Form form={form} layout="vertical">
				<Form.Item
					label="Query"
					name="query"
					rules={[{ required: true, message: "Please enter a query" }]}
				>
					<TextArea
						placeholder="e.g. I want to eat pancakes but I'm gluten-free"
						className="overflow-y-scroll h-40 break-all"
					/>
				</Form.Item>
			</Form>
		</Modal>
	);
}
