import {
	HomeOutlined,
	InfoCircleOutlined,
	UnorderedListOutlined,
} from "@ant-design/icons";
import { Button, Layout, Menu, Typography } from "antd";
import type React from "react";
import { useState } from "react";
import { ErrorBoundary } from "react-error-boundary";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { ROUTES } from "../constants";
import { BackgroundJobPanel } from "./BgJobPanel";
import { ErrorFallback } from "./ErrorFallback";
import { CreateNewQueryModal } from "./Queries";

const { Content, Sider, Header } = Layout;

const menuItems = [
	{
		key: ROUTES.recipes,
		icon: <HomeOutlined />,
		label: "Recipes",
	},
	{
		key: ROUTES.queries,
		icon: <UnorderedListOutlined />,
		label: "Queries",
	},
	{
		key: ROUTES.about,
		icon: <InfoCircleOutlined />,
		label: "About",
	},
];

export const AppLayout: React.FC = () => {
	const [collapsed, setCollapsed] = useState(false);
	const navigate = useNavigate();
	const location = useLocation();
	const [isCreateNewQueryModalOpen, setIsCreateNewQueryModalOpen] =
		useState(false);

	const currentPath =
		location.pathname === "/" ? ROUTES.recipes : location.pathname;

	return (
		<Layout style={{ minHeight: "100vh" }}>
			<ErrorBoundary FallbackComponent={ErrorFallback}>
				<Sider
					collapsible
					collapsed={collapsed}
					onCollapse={setCollapsed}
					theme="light"
				>
					<Menu
						theme="light"
						mode="inline"
						selectedKeys={[currentPath]}
						items={menuItems}
						onClick={({ key }) => navigate(key)}
					/>
				</Sider>

				<Layout>
					<Header
						style={{
							padding: "10px 24px",
							background: "transparent",
							userSelect: "none",
							display: "flex",
							alignItems: "center",
							justifyContent: "space-between",
							position: "relative",
						}}
					>
						<div style={{ flex: 1 }}></div>

						<Typography.Title
							level={1}
							style={{
								color: "#0952ab",
								textAlign: "center",
								position: "absolute",
								left: "50%",
								transform: "translateX(-50%)",
								margin: 0,
								fontWeight: "bold",
							}}
						>
							{menuItems.find((item) => item.key === currentPath)?.label}
						</Typography.Title>

						<div
							style={{ flex: 1, display: "flex", justifyContent: "flex-end" }}
						>
							<Button
								type="primary"
								onClick={() => setIsCreateNewQueryModalOpen(true)}
							>
								Create New Query
							</Button>
						</div>
					</Header>
					<Content
						style={{
							margin: 24,
							backgroundColor: "#e1ecf2",
							border: "1px solid #b2d8ed",
							borderRadius: "10px",
						}}
					>
						<BackgroundJobPanel />

						<CreateNewQueryModal
							open={isCreateNewQueryModalOpen}
							onCancel={() => setIsCreateNewQueryModalOpen(false)}
						/>
						<Outlet />
					</Content>
				</Layout>
			</ErrorBoundary>
		</Layout>
	);
};
