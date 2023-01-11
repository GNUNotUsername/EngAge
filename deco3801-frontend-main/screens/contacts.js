import { SafeAreaView, ScrollView, Text, View } from 'react-native'
import colors from '../colors';
import Header from '../components/Header';
import IcoButton from '../components/IcoButton';
import PrimaryButton from '../components/PrimaryButton';
import styles from "../styles"

// contacts are conditionally rendered in jsx
// after being fetched from the backend in the messages screen 

export default ({route, navigation}) => {

  const { contacts } = route.params;

  return (
    <SafeAreaView style={[styles.engageBgContainer, {justifyContent: "flex-start"}]}>
      <Header text="Contacts" />
      <View style={{marginHorizontal:35, paddingTop:10, flexGrow:1}}>
          <ScrollView style={{marginBottom: 300}}>
            {contacts.length > 0 ?
              contacts.map(name => <IcoButton key={name} text={name} onPress={() => {navigation.navigate("NewMessage", {to: name})}} />)
            : <Text style={{
              fontFamily:"Sansita",
              fontSize:22,
              color: colors.purple,
              marginTop:30
            }}>No contacts. Please add someone to start sending messages!</Text>
            }
          </ScrollView>
          <PrimaryButton text="Back" size={22} style={{height:46, width:92,marginBottom:100}} onPress={navigation.goBack} />
      </View>
    </SafeAreaView>
  );
} 