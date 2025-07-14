export function ErrorFallback({ error }: { error: Error }) {
	return (
		<div className="flex flex-col items-center justify-center h-screen">
			<h1 className="text-2xl font-bold">Something went wrong</h1>
			<p className="text-gray-500">{error.message}</p>
		</div>
	);
}
