import { useState } from 'react';
import { SafeAreaView, Text, View, TextInput, ScrollView } from 'react-native';
import PrimaryButton from '../components/PrimaryButton';
import styles from "../styles"
import globals from '../globals'
import endpoints from '../endpoints'

import { setItemAsync, getItemAsync } from 'expo-secure-store'
import colors from '../colors';

export default ({navigation}) => {
  const [passwordError, setPasswordError] = useState('');
  const [email, onChangeEmail] = useState('');
  const [confirmEmail, onChangeConfirmEmail] = useState('');
  const [password, onChangePassword] = useState('');
  const [confirmPassword, onChangeConfirmPassword] = useState('');

  const [name, onChangeName] = useState('');
  const [suburb, onChangeSuburb] = useState('');
  const [state, onChangeState] = useState('');
  const [maxDist, onChangeMaxDist] = useState('');
  const states = ["QLD", "NSW", "NT", "VIC", "TAS", "SA", "ACT", "WA"]

  const onCreateAccount = async () => {
    if (globals.backendOn) {
      try {
        
        console.log("about to fetch for create");

        const form = new FormData();
        form.append("username", email);
        form.append("email", confirmEmail);
        form.append("password1", password);
        form.append("password2", confirmPassword);
        form.append("state", state);
        form.append("suburb", suburb);
        form.append("real_name", name);
        form.append("travel_dist", maxDist);

        const resp = await fetch(endpoints.registerPoint, {
          method: 'POST',
          
          body: form
        });
        const reply = await resp.json();
        //const replytext = await resp.text();
        //console.log(replytext);
        //
        //console.log(reply);
        if (reply.status == "success") {
          console.log("success");
          console.log(reply);          
          
          // now we get a token and then login
          // automatically to save the user
          // having to do it 

          
          
          const loginForm = new FormData();
          loginForm.append("username", email);
          loginForm.append("password", password);
          const loginResp = await fetch(endpoints.loginPoint, {
            method: 'POST',
            body : loginForm
          });
          const loginReply = await loginResp.json();
          if (loginReply.token) {
            await setItemAsync("authToken", loginReply.token);
            global.token = loginReply.token;
            navigation.navigate('WalkthroughScreen');
          } else {
            console.log("y no token");
          }
          
        } else {
          
          //couldn't log in
          console.log("no success");
          console.log(reply.status);
          console.log(reply.err);
          //if (reply.messages)          
          setPasswordError(reply.messages);
        
          // display a message
        }
      
      } catch (err) {
        // Do something creative with the error here.
        console.log(err);
      }
  } else {
    navigation.navigate('WalkthroughScreen');
  }
  };


    return (
      <SafeAreaView style={styles.engageBgContainer}>
        <View style={{marginVertical:35}}>
          <Text style={{...styles.text, fontSize: 42, color : colors.purple, fontFamily:'Sansita'}}>Create Your Account</Text>
        </View>
        <ScrollView contentContainerStyle={{alignItems:"center"}}>
          <TextInput style = {styles.inputContainer}
            onChangeText={onChangeEmail}
            placeholderTextColor="#7a7a7a"
            placeholder = "Email"
            value = {email}
            keyboardType="email-address"
          />
          <TextInput style = {styles.inputContainer}
            placeholder = "Confirm Email"
            placeholderTextColor="#7a7a7a"
            onChangeText={onChangeConfirmEmail}
            value = {confirmEmail}
            keyboardType="email-address"
          />
          <TextInput style = {styles.inputContainer}
            placeholder = "Name"
            placeholderTextColor="#7a7a7a"
            onChangeText={onChangeName}
            value = {name}
          />
          <TextInput style = {styles.inputContainer}
            placeholder = "State"
            placeholderTextColor="#7a7a7a"
            onChangeText={onChangeState}
            value = {state}
          />
          <TextInput style = {styles.inputContainer}
            placeholder = "Suburb"
            placeholderTextColor="#7a7a7a"
            onChangeText={onChangeSuburb}
            value = {suburb}
          />
        <TextInput style = {styles.inputContainer}
            placeholder = "Max Travel Distance"
            placeholderTextColor="#7a7a7a"
            onChangeText={onChangeMaxDist}
            value = {maxDist}
          />
          <TextInput style = {styles.inputContainer}
            placeholder = "Password"
            placeholderTextColor="#7a7a7a"
            onChangeText={onChangePassword}          
            value = {password}
            secureTextEntry={true}
          />
          <TextInput style = {styles.inputContainer}
            placeholder = "Confirm password"
            onChangeText={onChangeConfirmPassword}
            placeholderTextColor="#7a7a7a"
            value = {confirmPassword}
            secureTextEntry={true}
          />
          
          { passwordError.length > 0 &&
            <Text style = {styles.walkthroughText}>{passwordError}</Text>
          }
          <PrimaryButton text='Create' size={32} style={{width:230, height:60, marginVertical:10}} onPress = {onCreateAccount} />  
          <PrimaryButton text='Back' size={32} style={{width:230, height:60, marginVertical: 10}} onPress = {navigation.goBack} />
        </ScrollView>
        
      </SafeAreaView>
    );
  }