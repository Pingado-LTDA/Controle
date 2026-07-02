import 'react-native-gesture-handler';
import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { MaterialCommunityIcons } from '@expo/vector-icons';

import DashboardScreen from './src/screens/DashboardScreen';
import ControlScreen from './src/screens/ControlScreen';
import FieldMapScreen from './src/screens/FieldMapScreen';
import { colors } from './src/theme';

const Tab = createBottomTabNavigator();

const ICONS = {
  Painel: 'view-dashboard-outline',
  Controle: 'controller-classic-outline',
  Mapa: 'map-outline',
};

export default function App() {
  return (
    <SafeAreaProvider>
      <StatusBar style="light" />
      <NavigationContainer
        theme={{
          dark: true,
          colors: {
            primary: colors.chlorophyllLight,
            background: colors.soilBlack,
            card: colors.soilBlackLight,
            text: colors.huskCream,
            border: colors.border,
            notification: colors.amber,
          },
        }}
      >
        <Tab.Navigator
          screenOptions={({ route }) => ({
            headerShown: false,
            tabBarActiveTintColor: colors.chlorophyllLight,
            tabBarInactiveTintColor: colors.mist,
            tabBarStyle: {
              backgroundColor: colors.soilBlackLight,
              borderTopColor: colors.border,
              height: 64,
              paddingBottom: 10,
              paddingTop: 8,
            },
            tabBarLabelStyle: { fontSize: 11, fontWeight: '600', letterSpacing: 0.4 },
            tabBarIcon: ({ color, size }) => (
              <MaterialCommunityIcons name={ICONS[route.name]} color={color} size={size} />
            ),
          })}
        >
          <Tab.Screen name="Painel" component={DashboardScreen} />
          <Tab.Screen name="Controle" component={ControlScreen} />
          <Tab.Screen name="Mapa" component={FieldMapScreen} />
        </Tab.Navigator>
      </NavigationContainer>
    </SafeAreaProvider>
  );
}
