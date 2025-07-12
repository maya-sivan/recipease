import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import "antd/dist/reset.css";
import "./app.css";
import { Provider as JotaiProvider } from "jotai";
import { AboutPage, RecipesPage, RequestsPage } from "./components";
import AppLayout from "./components/AppLayout";
import { globalAtomStore } from "./components/context/global-atom-store";
import { QueryPage } from "./components/Queries/QueryPage";
import { ROUTES } from "./constants/routes";

const queryClient = new QueryClient();

const router = createBrowserRouter([
	{
		path: "/",
		element: <AppLayout />,
		children: [
			{ index: true, element: <RecipesPage /> },
			{ path: ROUTES.about, element: <AboutPage /> },
			{ path: ROUTES.queries, element: <RequestsPage /> },
			{ path: ROUTES.query, element: <QueryPage /> },
			{ path: ROUTES.recipes, element: <RecipesPage /> },
		],
	},
]);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
	<React.StrictMode>
		<QueryClientProvider client={queryClient}>
			<JotaiProvider store={globalAtomStore}>
				<RouterProvider router={router} />
			</JotaiProvider>
		</QueryClientProvider>
	</React.StrictMode>,
);
