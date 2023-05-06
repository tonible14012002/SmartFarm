import React from 'react';
import { NavigationContainer, useNavigationContainerRef } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { View, Text } from 'react-native';

import LoginPage from './src/screens/Login';
import Home from './src/screens/Home';
import Devices from './src/screens/Devices';
import Log from './src/screens/Log';

const Stack = createNativeStackNavigator()
const Tab = createBottomTabNavigator()

const tabLabel = (props) => {
  return (
    <View style={{height: '100%', justifyContent: 'center'}}>
      <Text style={{color: props.inherit.color, fontSize: 20, fontWeight: 700}}>
        {props.label}
      </Text>
    </View>
  )
}

const BottomTabNavigator = ({navigation}) => {
  return (
    <Tab.Navigator
      initialRouteName='Home'
      screenOptions={{
        headerShown: false,
        tabBarIconStyle: {display: 'none'},
        tabBarActiveTintColor: '#2a78e4',
        tabBarInactiveTintColor: 'silver',
        tabBarLabelStyle: {display: 'none'},
        tabBarStyle: {height: 80, bottom: 0, position: 'absolute'}
      }}
    >
      <Tab.Screen 
        name="Devices" 
        component={Devices} 
        options={{tabBarLabel: (props) => tabLabel({inherit:props, label:'Devices'})}}
      />
      <Tab.Screen 
        name="Home" 
        component={Home}  
        options={{tabBarLabel: (props) => tabLabel({inherit:props, label:'Home'})}}
      />
      <Tab.Screen 
        name="Log" 
        component={Log} 
        options={{tabBarLabel: (props) => tabLabel({inherit:props, label:'Log'})}}
      />
    </Tab.Navigator>
  )
}

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName='login'
        screenOptions={{headerShown: false}}
      >
        <Stack.Screen name='login' component={LoginPage}/>
        <Stack.Screen name='main'component={BottomTabNavigator}/>
      </Stack.Navigator>
    </NavigationContainer>
  );
}