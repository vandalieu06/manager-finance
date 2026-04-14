import { Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Input from "../components/ui/FormInput";

export default function Index() {
	return (
		<View
			style={{
				flex: 1,
				justifyContent: "center",
				alignItems: "center",
			}}>
			<Text>Edit app/index.tsx to edit this screen.</Text>

			<SafeAreaView>
				{" "}
				<Input
					variant="default"
					size="sm"
					placeholder="hola"></Input>
			</SafeAreaView>
		</View>
	);
}
