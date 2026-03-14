import FontAwesome from "@expo/vector-icons/FontAwesome";
import { Pressable, Text, View } from "react-native";

type Props = {
	label: string;
	theme?: "primary";
	onPress?: () => void;
};

export default function Button({ label, theme, onPress }: Props) {
	if (theme === "primary") {
		return (
			<View className="mx-5 h-[68px] w-80 items-center justify-center rounded-[18px] border-4 border-[#ffd33d] p-[3px]">
				<Pressable
					className="h-full w-full flex-row items-center justify-center rounded-[10px] bg-white"
					onPress={onPress ?? (() => alert("You pressed a button."))}>
					<FontAwesome
						name="picture-o"
						size={18}
						color="#25292e"
						className="pr-2"
					/>
					<Text className="text-base text-[#25292e]">{label}</Text>
				</Pressable>
			</View>
		);
	}

	return (
		<View className="mx-5 h-[68px] w-80 items-center justify-center p-[3px]">
			<Pressable
				className="h-full w-full flex-row items-center justify-center rounded-[10px]"
				onPress={onPress ?? (() => alert("You pressed a button."))}>
				<Text className="text-base text-white">{label}</Text>
			</Pressable>
		</View>
	);
}
