import { Tabs } from "expo-router";
import React from "react";

import colors from "@/constants/colors";
export default function TabLayout() {

	return (
		<Tabs
			screenOptions={{
				tabBarActiveTintColor: colors.colors.primary.v1,
				headerShown: false,
			}}>
			<Tabs.Screen
				name="index"
				options={{
					title: "Home",
			
				}}
			/>
			<Tabs.Screen
				name="explore"
				options={{
					title: "Explore",
				
				}}
			/>
		</Tabs>
	);
}
