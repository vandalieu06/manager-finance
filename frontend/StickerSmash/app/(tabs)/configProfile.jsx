import Ionicons from "@expo/vector-icons/Ionicons";
import { Image } from "expo-image";
import * as ImagePicker from "expo-image-picker";
import React from "react";
import { Alert, Pressable, ScrollView, Text, View } from "react-native";
import { SafeAreaProvider, SafeAreaView } from "react-native-safe-area-context";
import TextInput from "../components/textInput";

const PLACEHOLDERIMAGE = require("../../assets/stickers/images/background-image.png");

// Datos simulados del usuario (sustituir por llamada a API/store real)
const USUARIO_INICIAL = {
	nombre: "Adrián",
	apellido: "García",
	email: "adrian@ejemplo.com",
	telefono: "+34 612 345 678",
	avatarUri: null,
};

export default function ConfigProfile() {
	const [isEditing, setIsEditing] = React.useState(false);

	// Datos mostrados (confirmados)
	const [datos, setDatos] = React.useState(USUARIO_INICIAL);

	// Copia temporal durante edición
	const [draft, setDraft] = React.useState(USUARIO_INICIAL);

	// Campos de contraseña solo visibles en modo edición
	const [passwordActual, setPasswordActual] = React.useState("");
	const [passwordNueva, setPasswordNueva] = React.useState("");
	const [passwordConfirmar, setPasswordConfirmar] = React.useState("");

	const handleCambiarFoto = async () => {
		const permiso = await ImagePicker.requestMediaLibraryPermissionsAsync();
		if (!permiso.granted) {
			Alert.alert("Permiso requerido", "Necesitamos acceso a tu galería.");
			return;
		}

		const resultado = await ImagePicker.launchImageLibraryAsync({
			mediaTypes: ImagePicker.MediaTypeOptions.Images,
			allowsEditing: true,
			aspect: [1, 1],
			quality: 0.8,
		});

		if (!resultado.canceled) {
			setDraft((d) => ({ ...d, avatarUri: resultado.assets[0].uri }));
		}
	};

	const handleEditar = () => {
		setDraft({ ...datos });
		setIsEditing(true);
	};

	const handleCancelar = () => {
		setPasswordActual("");
		setPasswordNueva("");
		setPasswordConfirmar("");
		setIsEditing(false);
	};

	const handleGuardar = () => {
		if (passwordNueva && passwordNueva !== passwordConfirmar) {
			Alert.alert("Error", "Las contraseñas nuevas no coinciden.");
			return;
		}
		setDatos({ ...draft });
		setPasswordActual("");
		setPasswordNueva("");
		setPasswordConfirmar("");
		setIsEditing(false);
		Alert.alert("Éxito", "Datos guardados correctamente.");
	};

	return (
		<SafeAreaProvider>
			<SafeAreaView className="flex-1 bg-[#1a1d23]">
				<ScrollView
					contentContainerClassName="px-5 pb-10"
					showsVerticalScrollIndicator={false}>
					{/* Avatar */}
					<View className="mb-6 items-center">
							<Image
								className="h-[100px] w-[100px] rounded-full border-[3px] border-[#ffd33d] bg-[#2c3038]"
							source={
								(isEditing ? draft.avatarUri : datos.avatarUri)
									? { uri: isEditing ? draft.avatarUri : datos.avatarUri }
									: PLACEHOLDERIMAGE
							}
							contentFit="cover"
							transition={500}
						/>
						{isEditing && (
							<Pressable
								className="mt-2"
								onPress={handleCambiarFoto}>
								<Text className="text-sm text-[#ffd33d]">Cambiar foto</Text>
							</Pressable>
						)}
					</View>

					{/* Sección: Información Personal */}
					<View className="mb-5 rounded-xl bg-[#2c3038] p-4">
						<View className="mb-2 flex-row items-center justify-between">
							<Text className="text-base font-bold text-[#ffd33d]">Información Personal</Text>
							{!isEditing && (
								<Pressable
									onPress={handleEditar}
									className="flex-row items-center gap-1">
									<Ionicons
										name="pencil-outline"
										size={18}
										color="#ffd33d"
									/>
									<Text className="text-[13px] text-[#ffd33d]">Editar</Text>
								</Pressable>
							)}
						</View>

						<TextInput
							label="Nombre"
							placeholder="Ingresa tu nombre"
							value={isEditing ? draft.nombre : datos.nombre}
							onChangeText={(v) => setDraft((d) => ({ ...d, nombre: v }))}
							editable={isEditing}
							onPress={handleEditar}
						/>
						<TextInput
							label="Apellido"
							placeholder="Ingresa tu apellido"
							value={isEditing ? draft.apellido : datos.apellido}
							onChangeText={(v) => setDraft((d) => ({ ...d, apellido: v }))}
							editable={isEditing}
							onPress={handleEditar}
						/>
						<TextInput
							label="Correo electrónico"
							placeholder="ejemplo@correo.com"
							value={isEditing ? draft.email : datos.email}
							onChangeText={(v) => setDraft((d) => ({ ...d, email: v }))}
							keyboardType="email-address"
							editable={isEditing}
							onPress={handleEditar}
						/>
						<TextInput
							label="Teléfono"
							placeholder="Ingresa tu teléfono"
							value={isEditing ? draft.telefono : datos.telefono}
							onChangeText={(v) => setDraft((d) => ({ ...d, telefono: v }))}
							keyboardType="phone-pad"
							editable={isEditing}
							onPress={handleEditar}
						/>
					</View>

					{/* Sección: Seguridad — solo en modo edición */}
					{isEditing && (
						<View className="mb-5 rounded-xl bg-[#2c3038] p-4">
							<Text className="text-base font-bold text-[#ffd33d]">Cambiar contraseña</Text>
							<TextInput
								label="Contraseña actual"
								placeholder="••••••••"
								value={passwordActual}
								onChangeText={setPasswordActual}
								secureTextEntry
							/>
							<TextInput
								label="Nueva contraseña"
								placeholder="••••••••"
								value={passwordNueva}
								onChangeText={setPasswordNueva}
								secureTextEntry
							/>
							<TextInput
								label="Confirmar nueva contraseña"
								placeholder="••••••••"
								value={passwordConfirmar}
								onChangeText={setPasswordConfirmar}
								secureTextEntry
							/>
						</View>
					)}

					{/* Botones de acción */}
					{isEditing && (
						<View className="flex-row gap-3">
							<Pressable
								className="flex-1 items-center rounded-xl border border-[#ffd33d] py-3.5"
								onPress={handleCancelar}>
								<Text className="text-base font-bold text-[#ffd33d]">Cancelar</Text>
							</Pressable>
							<Pressable
								className="flex-1 items-center rounded-xl bg-[#ffd33d] py-3.5"
								onPress={handleGuardar}>
								<Text className="text-base font-bold text-[#1a1d23]">Guardar</Text>
							</Pressable>
						</View>
					)}
				</ScrollView>
			</SafeAreaView>
		</SafeAreaProvider>
	);
}
