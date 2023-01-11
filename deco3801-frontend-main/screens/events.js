import { useEffect, useState } from 'react';
import { SafeAreaView, ScrollView, Text, View } from 'react-native'
import EventPreview from '../components/EventPreview';
import Header from '../components/Header';
import Hr from '../components/Hr';
import Loading from '../components/Loading'
import endpoints from '../endpoints';
import styles from "../styles"

// We pull events from the appropriate 
// backend endpoint and then render them in a jsx scrollview

export default ({navigation}) => {
  const [isLoaded, updateLoad] = useState(false)
  const [eventsData, setEvents] = useState([])

  useEffect(() => {
    const getEvents = async () => {
      // Make fetch for events here
      try {
        const raw = await fetch(endpoints.availableEvents + "?n_events=15", {
          headers: {
            "Authorization": `Token ${global.token}`
          }
        })
        const data = await raw.json()
        setEvents(data)
        console.log(data);
        updateLoad(true)
      } catch (e) {
        console.log("Events has failed");
        console.warn(e);
      }
    }
    getEvents()
  }, []);

  return (
    <SafeAreaView style={[styles.engageBgContainer, {justifyContent:"flex-start"}]}>
      <Header text="Events" navigation={navigation} />
      <View style={{flexGrow:1, alignSelf:"stretch"}}>
        <Text style={{fontFamily:"Sansita", textAlign:"center", fontSize:24, marginVertical:15}}>
          Upcoming events near you
        </Text>
        <Hr />
        {isLoaded ?
            (eventsData.length == 0 ? 
              <Text style={{fontFamily: "Sansita", textAlign: "center", fontSize:22, marginTop:100, marginHorizontal:20}}>We couldn't find any events for you. Please check back later.</Text>
              :
                <ScrollView style={{marginHorizontal:40, marginTop:20}}>
                  {eventsData.map(data => <EventPreview key={data[0]} eventData={data} onPress={() => {navigation.navigate("SpecificEvent", {eventData: data})}} /> )}
                </ScrollView>
              )
          :
          <Loading />
        }
      </View>
    </SafeAreaView>
  );
}