import { StyleSheet, Text, View } from "react-native";

export default function hola() {
	return (
		<View style={stylos.ventana}>
			<Text style={stylos.text}>Hola</Text>
		</View>
	);
}

const stylos = StyleSheet.create({
	ventana: {
		backgroundColor: "#cfb914",
		paddingLeft:24 ,
	},

	text: {
		color: "black",
		fontSize: 24,
	},
});
