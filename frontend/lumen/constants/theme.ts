import { Platform } from "react-native";

const colors = {
	brand: {
		primario: {
			v1: "#4ECDC4",
			v2: "#81DBD5",
			v3: "#B3EAE6",
			v4: "#E6F8F7",
		},
		secundario: {
			v1: "#F76132",
			v2: "#FF8A65",
			v3: "#FFC7B5",
			v4: "#FFE2D9",
		},
		accent1: {
			v1: "#FFE66D",
			v2: "#FFED95",
			v3: "#FFF4BE",
			v4: "#FFFBE6",
		},
		accent2: {
			v1: "#FF6B6B",
			v2: "#FF9393",
			v3: "#FFBBBB",
			v4: "#FFE3E3",
		},
		accent3: {
			v1: "#F7FFF7",
			v2: "#F9FFF9",
			v3: "#FCFFFC",
			v4: "#FEFFFE",
		},
	},
	info: {
		success: {
			v1: "#22C55E",
			v2: "#76DE9A",
			v3: "#B3EED0",
			v4: "#DFF9ED",
		},
		info: {
			v1: "#0EA5E9",
			v2: "#68C1EF",
			v3: "#A9DBF4",
			v4: "#D8F0FA",
		},
		warning: {
			v1: "#F59E0B",
			v2: "#F8BD54",
			v3: "#FAD997",
			v4: "#FCEECF",
		},
		danger: {
			v1: "#EF4444",
			v2: "#ED7272",
			v3: "#EB9D9D",
			v4: "#E9C4C4",
		},
	},
	blackAndWhite: {
		blanco: "#FFFFFF",
		negro: "#000000",
	},
	light: {
		text: "#11181C",
		background: "#FFFFFF",
		tint: "#4ECDC4",
		icon: "#687076",
		tabIconDefault: "#687076",
		tabIconSelected: "#4ECDC4",
	},
	dark: {
		text: "#ECEDEE",
		background: "#151718",
		tint: "#4ECDC4",
		icon: "#9BA1A6",
		tabIconDefault: "#9BA1A6",
		tabIconSelected: "#4ECDC4",
	},
} as const;

const fontAssets = {
	Inter: require("../assets/fonts/Inter-VariableFont_opsz,wght.ttf"),
	"Inter-Italic": require("../assets/fonts/Inter-Italic-VariableFont_opsz,wght.ttf"),
	RedHatMono: require("../assets/fonts/RedHatMono-VariableFont_wght.ttf"),
	"RedHatMono-Italic": require("../assets/fonts/RedHatMono-Italic-VariableFont_wght.ttf"),
} as const;

const fonts = Platform.select({
	ios: {
		sans: "Inter",
		serif: "Inter",
		rounded: "Inter",
		mono: "RedHatMono",
	},
	default: {
		sans: "Inter",
		serif: "Inter",
		rounded: "Inter",
		mono: "RedHatMono",
	},
	web: {
		sans: "Inter, system-ui, sans-serif",
		serif: "Inter, serif",
		rounded: "Inter, system-ui, sans-serif",
		mono: "'Red Hat Mono', 'RedHatMono', monospace",
	},
});

export const Theme = {
	Colors: colors,
	FontAssets: fontAssets,
	Fonts: fonts,
} as const;

export const Colors = Theme.Colors;
export const FontAssets = Theme.FontAssets;
export const Fonts = Theme.Fonts;
