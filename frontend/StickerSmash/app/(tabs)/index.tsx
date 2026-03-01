import { Link } from "expo-router";
import Button from "@/app/components/button";
import { StyleSheet, Text, View } from "react-native";
import ImageViewer from "@/app/components/imageViewer";
const PLACEHOLDERIMAGE = require("@/assets/stickers/images/background-image.png");

export default function Index() {
	return (
		<View style={styles.container}>
			<Text style={styles.text}>
				Hola con estilo personalizado con constantes
			</Text>
			<Link
				href="./about"
				style={styles.button}>
				Go to About screen
			</Link>
			<Link
				href="./hola"
				style={styles.button}>
				Hola
			</Link>
			<View style={styles.imageContainer}>
				<ImageViewer imgSource={PLACEHOLDERIMAGE} />
			</View>
			<View style={styles.footerContainer}>
				<Button
					theme="primary"
					label="Choose a photo"
				/>
				<Button label="Use this photo" />
			</View>
		</View>
	);
}

const styles = StyleSheet.create({
	container: {
		flex: 1,
		backgroundColor: "#6490c7",
		alignItems: "center",
		justifyContent: "center",
	},
	text: {
		color: "#042042",
	},

	button: {
		fontSize: 20,
		textDecorationLine: "underline",
		color: "#fff",
	},
	imageContainer: {
		flex: 1,
	},
	image: {
		width: 320,
		height: 440,
		borderRadius: 18,
	},
	footerContainer: {
		flex: 1 / 3,
		alignItems: "center",
	},
});
