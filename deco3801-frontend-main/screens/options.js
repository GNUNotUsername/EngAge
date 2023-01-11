import { SafeAreaView, View } from 'react-native'
import styles from "../styles"
import IcoButton from '../components/IcoButton';
import Header from '../components/Header';

import { deleteItemAsync } from 'expo-secure-store';

// the options screen 
// renders a logout button (where we trash the token and return to the home screen)
// 

const logOut = async () => {
  console.log("hit async");
  try {
    console.log("attempting logout");
    await deleteItemAsync("authToken");
    // global.token = null;    
    console.log("returning");
    return true;

  } catch(exception) {
    console.log(exception);
    return false; 
  }
}

export default ({navigation}) => {  
  return (
    <SafeAreaView style={[styles.engageBgContainer, {justifyContent:"flex-start"}]}>
      <Header text="Options" navigation={navigation}/>
      <View>
        <IcoButton text="Change password" onPress = {() => {
          navigation.navigate('ChangePasswordScreen');
        }} image={require("../assets/Password.png")} />
        <IcoButton text="Interests" onPress={() => navigation.navigate("InterestScreen",{editing: true})} image={require("../assets/Interests.png")} />
        <IcoButton text="Log out" onPress={() => {
          logOut();
          navigation.navigate('Login')
        }} image={require("../assets/LogOut.png")} />
      </View>
    </SafeAreaView>
  );
}