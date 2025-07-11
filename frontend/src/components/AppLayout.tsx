import {
	HomeOutlined,
	InfoCircleOutlined,
	UnorderedListOutlined,
} from "@ant-design/icons";
import { Layout, Menu, Typography } from "antd";
import type React from "react";
import { useState } from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";

const { Content, Sider, Header } = Layout;

const menuItems = [
	{
		key: "/all-recipes",
		icon: <HomeOutlined />,
		label: "Recipes",
	},
	{
		key: "/all-requests",
		icon: <UnorderedListOutlined />,
		label: "Requests",
	},
	{
		key: "/about",
		icon: <InfoCircleOutlined />,
		label: "About",
	},
];

const AppLayout: React.FC = () => {
	const [collapsed, setCollapsed] = useState(false);
	const navigate = useNavigate();
	const location = useLocation();

	const currentPath =
		location.pathname === "/" ? "/all-recipes" : location.pathname;

	return (
		<Layout style={{ minHeight: "100vh" }}>
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
					}}
				>
					<Typography.Title level={2} style={{ color: "#0952ab" }}>
						{menuItems.find((item) => item.key === currentPath)?.label}
					</Typography.Title>
				</Header>
				<Content
					style={{
						margin: 24,
						backgroundColor: "#cee7f5",
						border: "1px solid #b2d8ed",
						borderRadius: "10px",
					}}
				>
					<Outlet />
				</Content>
			</Layout>
		</Layout>
	);
};

export default AppLayout;
