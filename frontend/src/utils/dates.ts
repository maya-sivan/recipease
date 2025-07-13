import dayjs from "dayjs";

export const formatDate = (date: Date) => {
	return dayjs(date).format("MMMM Do, YYYY @ HH:mm");
};
