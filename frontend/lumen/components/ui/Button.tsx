import React from "react";
import { Pressable, Text } from "react-native";

// 1. Defines qué props acepta el componente y sus tipos
interface ButtonProps {
	// Qué estilo visual tiene el botón (obligatorio)
	variant?: "primario" | "secundario" | "danger" | "outline";
	// Qué tamaño tiene (opcional, por defecto "md")
	size?: "sm" | "md" | "lg";
	// Función que se ejecuta al pulsar
	onPress?: () => void;
	// Si el botón está desactivado
	disabled?: boolean;
	// El texto u otros elementos dentro del botón
	children: React.ReactNode;
}

// 2. Mapas de clases según el valor del prop
const variantStyles = {
	primario: "bg-primary-v1 active:bg-primary-v2",
	secundario: "bg-secondary-v1 active:bg-secondary-v2",
	danger: "bg-feedback-danger-v1 active:bg-feedback-danger-v2",
	outline: "border-2 border-primary-v1 bg-transparent",
};

const variantTextStyles = {
	primario: "text-white",
	secundario: "text-white",
	danger: "text-white",
	outline: "text-primary-v1",
};

const sizeStyles = {
	sm: "px-3 py-1.5 rounded-md",
	md: "px-5 py-2.5 rounded-lg",
	lg: "px-7 py-3.5 rounded-xl",
};

const sizeTextStyles = {
	sm: "text-sm",
	md: "text-base",
	lg: "text-lg",
};

// 3. El componente desestructura los props con valores por defecto
export default function Button({
	variant = "primario",
	size = "md",
	onPress,
	disabled = false,
	children,
}: ButtonProps) {
	return (
		<Pressable
			onPress={onPress}
			disabled={disabled}
			className={`
        items-center justify-center
        ${variantStyles[variant]}
        ${sizeStyles[size]}
        ${disabled ? "opacity-50" : ""}
      `}>
			<Text
				className={`font-sans-bold ${variantTextStyles[variant]} ${sizeTextStyles[size]}`}>
				{children}
			</Text>
		</Pressable>
	);
}
