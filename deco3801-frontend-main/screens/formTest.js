import { SafeAreaView, Text, TextInput } from "react-native";
import React from "react";
import styles from "../styles";

// obselete early prototype when we were figuring out how form input would work

export default ({navigation}) => {
    // first name, last name, email, phone number, password
    // super hacky right now
    const [firstName, onChangeFirst] = React.useState('first name');
    const [lastName, onChangeLast] = React.useState('last name');
    const [email, onChangeEmail] = React.useState('email');
    const [phone, onChangePhone] = React.useState('phone');
    const [password, onChangePassword] = React.useState('password');
    
    return (
      <SafeAreaView style = {styles.container}>
        <Text style = {styles.formText}> first name</Text>
        <TextInput 
          onChangeText={onChangeFirst}
          value = {firstName}
        />
        <Text style = {styles.formText}> last name</Text>
        <TextInput 
          onChangeText={onChangeLast}
          value = {lastName}
        />
        <Text style = {styles.formText}> email </Text>
        <TextInput 
          onChangeText={onChangeEmail}
          value = {email}
        />
        <Text style = {styles.formText}> phone number </Text>
        <TextInput 
          onChangeText={onChangePhone}
          value = {phone}
        />
        <Text style = {styles.formText}> password </Text>
        <TextInput 
          onChangeText={onChangePassword}
          value = {password}
        />
      </SafeAreaView>
    );
  }