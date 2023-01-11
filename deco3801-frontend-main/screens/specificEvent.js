import { Linking, Platform, SafeAreaView, ScrollView, StyleSheet, Text, View } from 'react-native'
import Header from '../components/Header';
import Loading from '../components/Loading';
import PrimaryButton from '../components/PrimaryButton';
import SelectableButton from '../components/SelectableButton';
import globalStyles from "../styles"
import Hr from '../components/Hr';

import { useState, useEffect } from 'react';
import fonts from '../fonts';
import colors from '../colors';
import endpoints from '../endpoints';

// this screen displays the full details for an event
// as well as the option to launch the address in the user's
// prefered maps app
// and the ability to 'attend' which is then passed on to the backend 

const styles = StyleSheet.create({
  row: {
    flexDirection:"row",
    justifyContent:"space-around",
    marginVertical:5
  },
  buttonContainer: {
    alignSelf:"stretch"
  },
  text: {
    fontSize: 30,
    fontFamily: fonts.prompt,
    color: colors.purple,
    marginHorizontal: 20
  },
  header: {
    fontFamily: "Sansita",
    fontSize: 32,
    marginHorizontal:25,
    marginVertical: 10,
    color: colors.purple
  }
})

const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

const openMaps = (location) => {
  Linking.openURL(Platform.select({
    ios: `maps:0,0?q=${location}`,
    android: `geo:0,0?q=${location}`
  }))
}

export default ({route, navigation}) => {
  const [loading, updateLoad] = useState(true)
  const [going, setGoing] = useState(false)
  const [details, setDetails] = useState([])

  useEffect(() => {
    const getDetails = async () => {
      if (route.params.loadFrom) {
        try {
          const resp = await fetch(endpoints.specificEvent + "?event_id=" + route.params.loadFrom, {
            headers: {
              'Authorization': `Token ${global.token}`
            }
          })
          const data = await resp.json()
          setDetails(data)
        } catch (e) {
          console.log("getting details failed");
          console.warn(e)
        }
      } else {
        setDetails(route.params.eventData)
      }

      try {
        const id = route.params.loadFrom || route.params.eventData[0]
        console.log("Getting attendance for ", id);
        const resp = await fetch(endpoints.isAttending + "?event_id=" + id, {
          'headers': {
            'Authorization': `Token ${global.token}`
          }
        })
        const data = await resp.json()
        console.log(data);
        if (!data.error && data.attending)
          setGoing(data.attending)

        updateLoad(false)
      } catch (e) {
        console.log("getting attendance failed");
        console.warn(e)
      }
    }
    getDetails()
  }, [])

  const toggleGoing = async () => {
    console.log("Current val of going: ", going);
    try {
      const form = new FormData()
      form.append("choice", going ? "leave" : "attend")
      form.append("event_id", details[0])
      const resp = await fetch(endpoints.eventSignOn, {
        method: "POST",
        headers: {
          'Authorization': `Token ${global.token}`
        },
        body: form
      })
      const data = await resp.json()
    } catch (e) {
      console.warn(e)
    }
    setGoing(!going)
  }


  let stamp, month, hour, minute, meridian
  if (!loading) {
    stamp = new Date(details[3])
    month = months[stamp.getMonth()]
    hour = stamp.getHours()
    minute = stamp.getMinutes()
    meridian = 'AM'
    if (hour > 12) {
      hour -= 12
      meridian = 'PM'
    }
    if (minute < 10) {
      minute = '0' + minute
    }
  }

  return (
    <SafeAreaView style={[globalStyles.engageBgContainer, {justifyContent:"flex-start"}]}>
      <Header text="Events" navigation={navigation}/>
      <View style={{flexGrow:1, justifyContent:"space-around", alignSelf:"stretch", paddingHorizontal:10}}>
        { loading ?
          <Loading />
          :
          <>
            <ScrollView style={{margin:0}} contentContainerStyle={{flexGrow:1, marginBottom:100}}>
              <View>
                <Text style={styles.text}>{details[1]}</Text>
                <Text style={[styles.text, {fontSize:26}]}>{`${stamp.getDate()} ${month}, ${hour}:${minute} ${meridian}`}</Text>
                <Text style={[styles.text, {fontSize:26}]}>{details[2]}</Text>
              </View>
              <View style={{marginVertical:10}}>
                <Hr />
                <Text style={styles.header}>Description</Text>
                <Hr />
              </View>
              <View style={{flexDirection:"row", alignItems:"center"}}>
                {/* <Image source={require("../assets/Transport.png")}/> */}
                <Text style={[styles.text, {marginRight:35, fontSize:22}]}>{details[4]}</Text>
              </View>
            </ScrollView>
            <View style={styles.buttonContainer}>
              <View style={styles.row}>
                <PrimaryButton text="Maps" size={22} style={{height:61, width:145}} onPress={() => openMaps(details[2])} />
                <SelectableButton text="Going" size={22} style={{height:61, width:145}} active={going} onPress={toggleGoing} image={going ? require("../assets/Tick.png") : require("../assets/Tick-Light.png")} />
              </View>
              <View style={[styles.row, {marginBottom:80}]}>
                <PrimaryButton text="Back" size={22} style={{height:46, width:92}} onPress={navigation.goBack} />
                <PrimaryButton text="Send to a Friend" size={22} style={{width:198}} onPress={() => {
                  navigation.navigate("ShareEvent", {
                    eventName: details[1],
                    niceDate: `${month} ${stamp.getDate()}`
                  })
                }} />
              </View>
            </View>
          </>
        }
      </View>
    </SafeAreaView>
  );
} 