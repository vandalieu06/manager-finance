import { TextInput as RNTextInput, Text, View } from "react-native";

type Props = {
	label?: string;
	placeholder?: string;
	value?: string;
	onChangeText?: (text: string) => void;
	secureTextEntry?: boolean;
	keyboardType?: "default" | "email-address" | "numeric" | "phone-pad";
	editable?: boolean;
	onPress?: () => void;
};

export default function TextInput({
	label,
	placeholder,
	value,
	onChangeText,
	secureTextEntry = false,
	keyboardType = "default",
	editable = true,
	onPress,
}: Props) {
	return (
		<View className="my-2 w-full">
			{label && <Text className="mb-1 text-sm text-white">{label}</Text>}
			<RNTextInput
				className={
					editable
						? "rounded-lg border border-[#3d4350] bg-[#2c3038] px-3 py-2.5 text-base text-white"
						: "px-0 py-2.5 text-base text-[#d0d3d8]"
				}
				placeholder={placeholder}
				placeholderTextColor="#9ba1a6"
				value={value}
				onChangeText={onChangeText}
				secureTextEntry={secureTextEntry}
				keyboardType={keyboardType}
				editable={editable}
				onPressIn={!editable ? onPress : undefined}
			/>
		</View>
	);
}
