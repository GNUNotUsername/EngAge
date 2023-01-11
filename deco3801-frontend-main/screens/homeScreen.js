import { useEffect, useState } from 'react'
import { Text, View, SafeAreaView } from 'react-native'
import PrimaryButton from '../components/PrimaryButton'
import styles from "../styles"
import Emoji from '../components/Emoji'
import Header from '../components/Header'
import colors from '../colors'
import fonts from '../fonts'

import AsyncStorage from '@react-native-async-storage/async-storage'

// We have a one-user-per-device assumption here
// so we store the last submit in async storage
// to avoid repeatedly asking for mood checkins on the same day

export default ({navigation}) => {
  const [active, onSelect] = useState(false)
  const [submitted, updateSubmit] = useState(false)

  // When first mounted, check when we last submitted - if it's today, don't let them do it again
  useEffect(() => {
    const getLastSubmit = async () => {
      const day = await AsyncStorage.getItem("lastSubmit");
      if (day && day == new Date().toLocaleDateString())
        updateSubmit(true)
    }
    getLastSubmit()
  }, [])

  const onSubmit = () => {
    if (active)
      navigation.navigate("QuestionScreen", {
        feeling: active,
        toggle: updateSubmit
      })
  }

  return (
    <SafeAreaView style={[styles.engageBgContainer, {justifyContent:"flex-start"}]}>
      <Header text="Welcome" navigation={navigation} />
      { !submitted ?
        <View style={{flexGrow:1, justifyContent:"space-around"}}>
            <Text style={{fontSize:24, fontFamily:"Sansita", color:colors.purple}}>How are you feeling today?</Text>
            <View style={{alignItems:"center"}}>
              <View style={{flexDirection:"row"}}>
                <Emoji emote="😀" label="Happy" onPress={onSelect} selected={active}/>
                <Emoji emote="🙂" label="Satisfied" onPress={onSelect} selected={active}/>
              </View>
              <View style={{flexDirection:"row"}}>
                <Emoji emote="😐" label="Neutral" onPress={onSelect} selected={active}/>
                <Emoji emote="😟" label="Sad" onPress={onSelect} selected={active}/>
                <Emoji emote="😭" label="Distress" onPress={onSelect} selected={active}/>
              </View>
            </View>
            <PrimaryButton text="Continue" size={22} style={{height:46, width:143, alignSelf:"flex-end", marginRight:20}} onPress={onSubmit} disabled={!active} />
        </View>
        :
        <View style={{flexGrow: 1, justifyContent: "center"}}>
          <Text style={{fontFamily:"Sansita", color:colors.purple, textAlign:"center", fontSize:26, paddingHorizontal:10}}>Thanks for checking in! Remember to come back and check-in again tomorrow.</Text>
          <Text style={{fontFamily:fonts.prompt, textAlign:"center", fontSize:18, color:colors.purple, paddingHorizontal:10}}>In the mean time, make sure you've had a look at some of the upcoming events in your area.</Text>
        </View>
      }
    </SafeAreaView>
  );
}