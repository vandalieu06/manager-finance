/** @type {import('tailwindcss').Config} */

const { colors } = require("./constants/colors");

module.exports = {
	content: ["./app/**/*.{js,jsx,ts,tsx}", "./components/**/*.{js,jsx,ts,tsx}"],
	presets: [require("nativewind/preset")],
	theme: {
		extend: {
			// Spread directo — Tailwind genera automáticamente todas las clases
			// bg-brand-primario-v1, text-info-danger-v2, etc.
			colors,
			fontFamily: {
				sans: ["Inter"],
				"sans-italic": ["Inter-Italic"],
				"sans-bold": ["Inter-Bold"],
				mono: ["RedHatMono"],
				"mono-italic": ["RedHatMono-Italic"],
				"mono-bold": ["RedHatMono-Bold"],
			},
		},
	},
	plugins: [],
};
