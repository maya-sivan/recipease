import clsx from "clsx";

export function TextBox({
	text,
	className,
}: {
	text: string;
	className?: string;
}) {
	return (
		<div
			className={clsx(
				"border rounded-md p-2 bg-gray-100 border-gray-300 overflow-y-scroll break-all",
				className,
			)}
		>
			{text}
		</div>
	);
}
