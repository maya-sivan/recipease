import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import "antd/dist/reset.css";
import "./app.css";
import { Provider as JotaiProvider } from "jotai";
import {
	AppLayout,
	globalAtomStore,
	QueriesPage,
	QueryPage,
	RecipesPage,
} from "./components";
import { NotFoundPage } from "./components/NotFoundPage";
import { ROUTES } from "./constants";

export const queryClient = new QueryClient();

const router = createBrowserRouter([
	{
		path: "/",
		element: <AppLayout />,
		children: [
			{ index: true, element: <RecipesPage /> },
			{ path: ROUTES.queries, element: <QueriesPage /> },
			{ path: ROUTES.query, element: <QueryPage /> },
			{ path: ROUTES.recipes, element: <RecipesPage /> },
			{ path: "*", element: <NotFoundPage /> },
		],
	},
]);

const container = document.getElementById("root")!;
const root = ReactDOM.createRoot(container);
root.render(
	<React.StrictMode>
		<QueryClientProvider client={queryClient}>
			<JotaiProvider store={globalAtomStore}>
				<RouterProvider router={router} />
			</JotaiProvider>
		</QueryClientProvider>
	</React.StrictMode>,
);
