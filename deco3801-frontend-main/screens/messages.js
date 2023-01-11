import { Text, ScrollView, SafeAreaView, StyleSheet, View } from 'react-native'
import { useState, useEffect } from 'react';
import Header from '../components/Header';
import PrimaryButton from '../components/PrimaryButton';
import SecondaryButton from '../components/SecondaryButton';
import globalStyles from "../styles"
import Loading from '../components/Loading';
import endpoints from '../endpoints';
import Message from '../components/Message';

const styles = StyleSheet.create({
  button: {
    height:61,
    marginVertical:8
  }
});

export default ({navigation}) => {
  const [msgInfo, updateLoad] = useState(false)
  const [contactsData, updateContacts] = useState({})

  // Load EVERYTHING we need - messages AND contacts
  // We'll repeat this every so often to pick up any new messages or contacts
  useEffect(() => {
    const getMsgData = async () => {
      try {
        const raw = await fetch(endpoints.getMessages, {
          headers: {
            "Authorization": `Token ${global.token}`
          }
        });

        const data = await raw.json();
        if (data.error && data.error=="not_found") {
          switch (data.error) {
            case "not_found":
              console.log("User has no messages");
              break;
            default:
              console.warn("Unknown error", data.error);
          }
        }
        updateLoad(Object.entries(data));
      } catch (e) {
        console.warn(e);
      }
    }

    const getContactsData = async () => {
      try {
        const resp = await fetch(endpoints.getContacts, {
          headers: {
            "Authorization": `Token ${global.token}`
          }
        })
        const data = await resp.json()
        if (data.error) {
          console.warn('Error', data.error)
        }
        updateContacts(Object.values(data))
      } catch (e) {
        console.warn(e)
      }
    }

    const getAllData = () => {
      getMsgData()
      getContactsData()
    }

    const id = setInterval(getAllData, 30 * 1000)
    getAllData()
    return () => clearInterval(id)
  }, []);

  return (
    <SafeAreaView style={[globalStyles.engageBgContainer, {justifyContent:"flex-start"}]}>
      <Header text="Messages" navigation={navigation}/>
      <View style={{flexGrow:1, alignSelf:"stretch", marginHorizontal:35, marginTop:10}}>
        <SecondaryButton text="Send new message" size={22} style={styles.button} onPress={() => {navigation.navigate("Contacts", {contacts: contactsData})}} />
        <PrimaryButton text="Add new contact" size={22} style={styles.button} onPress={() => {navigation.navigate("AddContact")}} />
        <ScrollView contentContainerStyle={{flexGrow:1, marginTop:20, paddingBottom:300}}>
          { !msgInfo ? <Loading /> :
          msgInfo.length > 0 ?
            msgInfo.map(([i, [sent, sender,, msg]]) =>
              <Message key={i} from={sender.split('@')[0]} sent={sent} msg={msg} onPress={() => {navigation.navigate("SpecificMessage", {msgData: [sent, sender, msg]})}} />)
            :
            <Text style = {globalStyles.walkthroughText}>No messages</Text>
          }
        </ScrollView>
      </View>
    </SafeAreaView>
  );
}