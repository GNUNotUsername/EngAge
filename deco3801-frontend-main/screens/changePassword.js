import { useState } from 'react';
import { SafeAreaView, Text, View, TextInput } from 'react-native';
import PrimaryButton from '../components/PrimaryButton';
import styles from "../styles"
import globals from '../globals'
import endpoints from '../endpoints';
import colors from '../colors';

// password changes just involve posting the new password
// to the appropriate endoint, which then performs all the appropriate 
// password validations for us
// and then we conditionally render some text in jsx to display the result

export default ({navigation}) => {
  
  
  const [password, onChangePassword] = useState('');
  const [confirmPassword, onChangeConfirmPassword] = useState('');
  const [passwordError, setPasswordError] = useState("");
  const onCreateAccount = async () => {
    if (globals.backendOn) {
      try {
        
        console.log("about to fetch for pw change");
        const form  = new FormData();
        form.append("password1", password);
        form.append("password2", confirmPassword);

        const resp = await fetch(endpoints.changePassword, {
          method: 'POST',
          headers: {
            
            'Authorization': `Token ${global.token}`        
          },
          body: form
        });
        const reply = await resp.json();
        console.log(reply);
        if (reply.status == "success") {
          console.log("success");
          setPasswordError("password updated!");
          // do something with the token later
          //navigation.navigate();
        } else {
          setPasswordError(reply.error);
        // couldn't log in
          console.log("no success");
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
        <Text style={{...styles.text, color: colors.purple,fontSize: 42, fontFamily:'Sansita'}}>Change Your Password</Text>        
       
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
        <PrimaryButton text='Update' size={32} style={{width:230, height:60}} onPress = {onCreateAccount} />  
        <PrimaryButton text='Back' size={32} style={{width:230, height:60}} onPress = {navigation.goBack} />
        
      </SafeAreaView>
    );
  }