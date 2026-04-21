import { Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

export default function ExploreScreen() {
	return (
		<SafeAreaView style={{ flex: 1 }}>
			<View
				style={{
					flex: 1,
					alignItems: "center",
					justifyContent: "center",
					padding: 24,
				}}>
				<Text style={{ fontSize: 24, fontWeight: "700" }}>Explore</Text>
				<Text style={{ marginTop: 8, textAlign: "center" }}>
					Pantalla placeholder para que la segunda tab exista de verdad.
				</Text>
			</View>
		</SafeAreaView>
	);
}
