import { Dimensions, SafeAreaView, ScrollView, Text, View } from 'react-native'
import Header from '../components/Header';
import PrimaryButton from '../components/PrimaryButton';
import Loading from '../components/Loading';
import styles from "../styles"
import { useEffect, useState } from 'react';
import endpoints from '../endpoints';
import IcoButton from '../components/IcoButton';

// notifications are pulled from the backend
// and then rendered in jsx
// and the appropriate navigation is called

let notifs = []

export default ({navigation}) => {
  const [isLoaded, updateLoad] = useState(false)

  useEffect(() => {
    const getNotifs = async () => {
      try {
        const resp = await fetch(endpoints.getNotifications, {
          headers: {
            'Authorization': `Token ${global.token}`
          }
        })
        const data = await resp.json()
        notifs = data
        console.log(data);
        updateLoad(true)
      } catch (e) {
        console.warn(e)
      }
    }

    getNotifs()
  }, [])

  const height = Dimensions.get("screen").height

  return (
    <SafeAreaView style={[styles.engageBgContainer, {justifyContent:"flex-start"}]}>
      <Header text="Notifications"/>
      <View style={{flexGrow:1, alignSelf:"stretch", justifyContent:"space-between", marginHorizontal:35, marginBottom: 35}}>
        {isLoaded ?
          <View style={{marginBottom: 0}}>
            <ScrollView style={{height:height-230}}>
              {notifs.length > 0 ? notifs.map(notif => {
                switch (notif.type) {
                  case "CI":
                    return <IcoButton key={notif.timestamp} text={notif.content} onPress={() => navigation.navigate("HomeScreen")} />
                  case "UE":
                  case "RE":
                    return <IcoButton key={notif.timestamp} text={notif.content} onPress={() => navigation.navigate("Events", {screen: 'SpecificEvent', params: {loadFrom: notif.link_event}})} />
                  case "FC":
                    return <IcoButton key={notif.timestamp} text={notif.content} onPress={() => navigation.navigate("Messages", {screen: "NewMessage", params: {to: notif.link_user}})} />
                  case "FQ":
                    return <IcoButton key={notif.timestamp} text={notif.content} onPress={() => navigation.navigate("FriendRequest", {from: notif.link_user})} />
                  default:
                    return <IcoButton key={notif.timestamp} text={notif.content} />
                }})
              : <Text style={{fontFamily:"Sansita", fontSize:26, textAlign:"center", marginTop:50}}>No notifications</Text>
              }
            </ScrollView>
          </View>
          :
          <View style={{marginTop:50}}>
            <Loading />
          </View>
        }
        <PrimaryButton text="Back" size={22} style={{width:92, height:46, alignSelf:"flex-start"}} onPress={navigation.goBack}/>
      </View>
    </SafeAreaView>
  );
}