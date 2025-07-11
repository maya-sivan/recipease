import colors from "tailwindcss/colors";

export default {
	content: ["./index.html", "./src/**/*.{ts,tsx}"],
	theme: {
		colors: {
			gray: colors.slate,
			blue: colors.sky,
			red: colors.rose,
			pink: colors.fuchsia,
		},
		fontFamily: {
			sans: ["Graphik", "sans-serif"],
			serif: ["Merriweather", "serif"],
		},
		extend: {
			spacing: {
				"128": "32rem",
				"144": "36rem",
			},
			borderRadius: {
				"4xl": "2rem",
			},
		},
	},
};
