import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import "antd/dist/reset.css";
import "./App.css";
import { Provider as JotaiProvider } from "jotai";
import React from "react";
import ReactDOM from "react-dom/client";
import { ErrorBoundary } from "react-error-boundary";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import {
	AboutPage,
	AppLayout,
	ErrorFallback,
	globalAtomStore,
	NotFoundPage,
	QueriesPage,
	QueryPage,
	RecipesPage,
} from "./components";
import { ROUTES } from "./constants";

export const queryClient = new QueryClient({
	defaultOptions: {
		queries: {
			throwOnError: true,
		},
		mutations: {
			throwOnError: true,
		},
	},
});

const router = createBrowserRouter([
	{
		path: "/",
		element: <AppLayout />,
		children: [
			{ index: true, element: <RecipesPage /> },
			{ path: ROUTES.queries, element: <QueriesPage /> },
			{ path: ROUTES.query, element: <QueryPage /> },
			{ path: ROUTES.recipes, element: <RecipesPage /> },
			{ path: ROUTES.about, element: <AboutPage /> },
			{ path: "*", element: <NotFoundPage /> },
		],
	},
]);

const container = document.getElementById("root")!;
const root = ReactDOM.createRoot(container);
root.render(
	<React.StrictMode>
		<QueryClientProvider client={queryClient}>
			<ErrorBoundary FallbackComponent={ErrorFallback}>
				<JotaiProvider store={globalAtomStore}>
					<RouterProvider router={router} />
				</JotaiProvider>
			</ErrorBoundary>
		</QueryClientProvider>
	</React.StrictMode>,
);
