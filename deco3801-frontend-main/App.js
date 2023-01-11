import { NavigationContainer } from '@react-navigation/native'
import { createNativeStackNavigator } from '@react-navigation/native-stack'
import { useFonts } from 'expo-font'
import { Prompt_400Regular } from '@expo-google-fonts/prompt'
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs'

import HomeScreen from './screens/home'
import WalkthroughScreen from './screens/walkthrough'
import CreateAccountScreen from './screens/createAccount'
import InterestScreen from './screens/interests'
import Events from './screens/events'
import CheckIn from './screens/homeScreen'
import Messages from './screens/messages'
import Options from './screens/options'
import Question from './screens/question'
import Notifications from './screens/notifications'
import SpecificEvent from './screens/specificEvent'
import Contacts from './screens/contacts'
import ComposeMessage from './screens/composeMessage'
import AddContact from './screens/addContact'
import ChangePasswordScreen from './screens/changePassword'
import FriendRequest from './screens/friendRequest'
import ShareEvent from './screens/shareEvent'

import NavBar from './components/NavBar'

import { SafeAreaView, LogBox, Text } from 'react-native'
import { StatusBar } from 'expo-status-bar'
import colors from './colors'
import specificMessage from './screens/specificMessage'

// these navigators are used 
// to allow us to swipe between screens
const Tabs = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

// There are two things that throw warnings in this app
// The first is something non-standard we do, but it doesn't break anything so it's all good
// The second is due to deprecated calls that an addon is making (we can't do anything about it)
// These warnings are not a problem, so we turn them off so they don't bother anyone
LogBox.ignoreLogs([
  'Non-serializable values were found in the navigation state',
  'ViewPropTypes will be removed from React Native'
])

const EventsStack = () => {
  return (
    <Stack.Navigator initialRouteName='MainEvents' screenOptions={{
      headerShown: false
    }}>
      <Stack.Screen name="MainEvents" component={Events} />
      <Stack.Screen name="SpecificEvent" component={SpecificEvent} />
      <Stack.Screen name="ShareEvent" component={ShareEvent} />
    </Stack.Navigator>
  )
}

const MessagingStack = () => {
  return (
    <Stack.Navigator initialRouteName='MainMessages' screenOptions={{
      headerShown:false
    }}>
      <Stack.Screen name="MainMessages" component={Messages} />
      <Stack.Screen name="Contacts" component={Contacts} />
      <Stack.Screen name="NewMessage" component={ComposeMessage} />
      <Stack.Screen name="AddContact" component={AddContact} />
      <Stack.Screen name="SpecificMessage" component={specificMessage} />
    </Stack.Navigator>
  )
}

// Things in the "main app" will have the bottom tab bar
const MainApp = () => {
  return (
    <Tabs.Navigator tabBar={NavBar} screenOptions={{headerShown:false}}>
      {/*
        Home
        Events
        Messages
        Options
      */}
      <Tabs.Screen name="HomeScreen" component={CheckIn} options={{title:"Home"}}/>
      <Tabs.Screen name="Events" component={EventsStack}/>
      <Tabs.Screen name="Messages" component={MessagingStack}/>
      <Tabs.Screen name="Options" component={Options}/>
    </Tabs.Navigator>
  )
}

/****
***** Execution begins here
*****/

export default function App() {

  const [fontsLoaded] = useFonts({
    Prompt_400Regular, // Body
    'Sansita': require("./assets/SansitaOne-Regular.ttf") // Headings
  });

  // this displays a loading symbol until fonts have loaded
  if (!fontsLoaded) return (<><Text>loading</Text></>)

  // the return value is a bunch of JSX that react native uses to render our UI  
  return (
    <>
      <NavigationContainer>
        <Stack.Navigator screenOptions={{headerShown:false}}>
          <Stack.Screen name="Login" component={HomeScreen} />
          <Stack.Screen name="MainApp" component={MainApp} />
          <Stack.Screen name="WalkthroughScreen" component={WalkthroughScreen} />
          <Stack.Screen name="CreateAccountScreen" component={CreateAccountScreen} />
          <Stack.Screen name="InterestScreen" component={InterestScreen} />
          <Stack.Screen name="QuestionScreen" component={Question} />
          <Stack.Screen name="NotificationsScreen" component={Notifications} />
          <Stack.Screen name="ChangePasswordScreen" component={ChangePasswordScreen} />
          <Stack.Screen name="FriendRequest" component={FriendRequest} />
        </Stack.Navigator>
      </NavigationContainer>
      <SafeAreaView style = {{backgroundColor: colors.white, borderWidth : 3, borderTopWidth : 0, borderColor : colors.purple}}>
      <StatusBar style="auto"/>
      </SafeAreaView>
    </>
  )
}
