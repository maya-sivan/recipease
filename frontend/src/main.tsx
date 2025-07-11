import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import "antd/dist/reset.css";
import "./app.css";
import { AboutPage, RecipesPage, RequestsPage } from "./components";
import AppLayout from "./components/AppLayout";

const router = createBrowserRouter([
	{
		path: "/",
		element: <AppLayout />,
		children: [
			{ index: true, element: <RecipesPage /> },
			{ path: "about", element: <AboutPage /> },
			{ path: "all-requests", element: <RequestsPage /> },
			{ path: "all-recipes", element: <RecipesPage /> },
		],
	},
]);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
	<React.StrictMode>
		<RouterProvider router={router} />
	</React.StrictMode>,
);
