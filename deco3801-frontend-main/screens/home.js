import { SafeAreaView, Image, Text, View, TextInput } from 'react-native';
import styles from "../styles"
import { useState, useEffect } from 'react'
import PrimaryButton from '../components/PrimaryButton';
import SecondaryButton from '../components/SecondaryButton';
import endpoints from '../endpoints';
import globals from '../globals'

import { setItemAsync, getItemAsync } from 'expo-secure-store'

// logins are handled via a fetch request to the server
// and a session token is returned, which we then use throughout the user's 
// session for authentication
// additionally any login errors (wrong username/password combination )
// is conditionally rendered in jsx

export default ({navigation}) => {
  const [phoneEmail, onChangePhoneEmail] = useState('');
  const [password, onChangePassword] = useState('');
  const [loginError, setLoginError] = useState('');

  const onLogin = async () => {
    if (globals.backendOn) {
      try {
        console.log("about to fetch");      
        const respRaw = await fetch(endpoints.loginPoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',          
          },
          body: JSON.stringify({
            username: phoneEmail,
            password: password,
          })
      });
      const resp = await respRaw.json();
      console.log(resp);
      if (resp.token) {
        console.log("success");
        // do something with the token later
        await setItemAsync("authToken", resp.token);
        global.token = resp.token;
        navigation.navigate('MainApp');
        setLoginError("");
        
      } else {
        // couldn't log in
        console.log("no success");
        setLoginError("invalid username/password combination");
        // display a message
      }
      
      } catch (err) {
        // Do something creative with the error here.
        console.warn(err);
      }
  } else {
    navigation.navigate('WalkthroughScreen');
  }
  };

  useEffect(() => {
    // Check for token - if we have one, no need to log in again
    getItemAsync("authToken").then(token => {
      if (token)  {
        navigation.navigate("MainApp")
        global.token = token
      }
      //  for non-testing purposes: navigation.navigate("MainApp")
    }).catch(err => {
      console.log(err);
    })
  }, [])

  return (
    <SafeAreaView style={styles.engageBgContainer}>
      <View>
        <Image style={{width:281, height:93}} source={require("../assets/Wordmark.png")}/>
      </View>
      <View style={{alignItems:'center'}}>
        <TextInput style = {styles.inputContainer}
            onChangeText={onChangePhoneEmail}
            placeholder = "Email / Phone"
            placeholderTextColor="#7a7a7a"
            value = {phoneEmail}
            keyboardType="email-address"
        />
        <TextInput style = {styles.inputContainer}
            onChangeText={onChangePassword}
            placeholder = "Password"
            placeholderTextColor="#7a7a7a"
            value = {password}
            secureTextEntry={true}
        />
          <PrimaryButton text='Login' size={32} style={{width:230, height:60, marginTop:5}} onPress={onLogin} />
          {
            loginError.length > 0 &&
            <Text style = {styles.walkthroughText}>{loginError}</Text>
          }
      </View>
      <View>
        {/* <SecondaryButton text='Sign In Using Device' size={20} style={{width:230, height:60, marginBottom:8}} /> */}
        <SecondaryButton text='Create Account' size={26} style={{width:230, height:60}}
          onPress = {() => navigation.navigate('CreateAccountScreen')}
        />
      </View>
    </SafeAreaView>
  );
}

