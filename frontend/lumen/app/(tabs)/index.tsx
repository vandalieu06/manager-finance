import { View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import Input from "@/components/ui/FormInput";

export default function HomeScreen() {
	return (
		<View
			style={{
				flex: 1,
				justifyContent: "center",
				alignItems: "center",
			}}>
			<SafeAreaView>
				<Input
					variant="default"
					size="sm"
					placeholder="hola"
				/>
			</SafeAreaView>
		</View>
	);
}
