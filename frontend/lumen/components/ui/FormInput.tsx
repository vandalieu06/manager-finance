import React from "react";
import { Text, TextInput, TextInputProps, View } from "react-native";
const colors = require("../../constants/colors");

interface InputProps extends Omit<TextInputProps, "editable"> {
	label?: string;
	variant?: "default" | "disabled" | "withIcon";
	size?: "sm" | "md" | "lg";
	icon?: React.ReactNode;
}

// Centraliza las diferencias visuales por tamaño para no repetir lógica en el render.
const sizeStyles = {
	sm: {
		label: "text-sm",
		input: "text-sm",
		icon: 16,
		borderWidth: 3,
	},
	md: {
		label: "text-base",
		input: "text-base",
		icon: 18,
		borderWidth: 4,
	},
	lg: {
		label: "text-lg",
		input: "text-lg",
		icon: 24,
		borderWidth: 4,
	},
} as const;

export default function FormInput({
	label = "label",
	variant = "default",
	size = "sm",
	icon,
	placeholder = "placeholder",
	secureTextEntry = false,
	style,
	...textInputProps
}: InputProps) {
	// Obtiene la configuración visual correspondiente al tamaño seleccionado.
	const currentSize = sizeStyles[size];
	// Deriva estados simples para mantener el JSX más legible.
	const isDisabled = variant === "disabled";
	const showIcon = variant === "withIcon" && !!icon;

	return (
		<View
			className="flex-col items-start"
			style={{ gap: 5 }}>
			{/* El label cambia de tamaño y color según el estado del input. */}
			<Text
				className={`font-mono ${currentSize.label} ${
					isDisabled ? "text-secondary-v3" : "text-base-black"
				}`}>
				{label}
			</Text>

			{/* Contenedor del campo: aplica borde y espaciado siguiendo el diseño de Figma. */}
			<View
				className={`flex-row items-center px-3 py-2 ${isDisabled ? "border-secondary-v3" : "border-base-black"}`}
				style={{
					borderWidth: currentSize.borderWidth,
					gap: 10,
				}}>
				{/* El icono solo se renderiza en la variante con icono y mantiene tamaño por variante. */}
				{showIcon ? (
					<View style={{ height: currentSize.icon, width: currentSize.icon }}>
						{icon}
					</View>
				) : null}

				{/* Se propagan las props nativas del TextInput y se ajustan estado/colores del sistema. */}
				<TextInput
					{...textInputProps}
					placeholder={placeholder}
					placeholderTextColor={colors.secondary.v3}
					secureTextEntry={secureTextEntry}
					editable={!isDisabled}
					className={`min-w-[116px] flex-1 font-mono ${currentSize.input} ${
						isDisabled ? "text-secondary-v3" : "text-base-black"
					}`}
					style={style}
				/>
			</View>
		</View>
	);
}
