import { SafeAreaView, StyleSheet, Text, View, ScrollView } from 'react-native'
import globalStyles from "../styles"
import { useState } from 'react'
import Question from '../components/Question'
import PrimaryButton from '../components/PrimaryButton'
import Hr from '../components/Hr'
import Header from '../components/Header'
import AsyncStorage from '@react-native-async-storage/async-storage'
import endpoints from '../endpoints'

// this is where we poll the user's daily mood in detail
// via interactive emoticons
// and then pass it to the backend

const styles = StyleSheet.create({
  text: {
    fontFamily: "Sansita",
    textAlign: "left",
    // alignSelf: "flex-start",
    // marginLeft:25,
    fontSize: 24
  },
  textCont: {
    marginVertical:15
  }
})

const emoteMap = {
  "Happy": 5,
  "Satisfied": 4,
  "Neutral": 3,
  "Sad": 2,
  "Distress": 1
}

const answerMap = {
  "Awful": 1,
  "Bad": 2,
  "Okay": 3,
  "Good": 4,
  "Great": 5
}

const questions = [
  'How is your physical health?',
  'How is your mental health?',
  'How is your social life?',
  'How satisfactory is the support you are receiving?',
  'How useful do you feel to others?',
  'How independent do you feel?'
]

export default ({route, navigation}) => {
  let states = []

  const questionElements = questions.map((q, i) => {
    const [active, onSelect] = states[i] = useState(false);
    return (<Question key={i} q={q} active={active} onSelect={onSelect} style={{marginTop:50}}/>)
  });

  const submitQuestions = async () => {
    /* Need to go through questionElements and determine which checkbox is selected for each of them
    If one of them doesn't have a selection, error out and let the user know
    Else, bundle it all up into some JSON, send it off to the server and place the user back in the main app */
    // Note: the wellbeing emoji lives in route.params.feeling
    // console.log("Emote: ", emoteMap[route.params.feeling]);
    const emote = emoteMap[route.params.feeling]
    let score = 0;
    for (let i = 0; i < states.length; i++) {
      const currentVal = states[i][0];
      if (!currentVal) {
        // Question has not been filled out - reject
        return;
      }
      // console.log(answerMap[currentVal])
      score += answerMap[currentVal]

    }
    console.log("Final submission", `[${emote}, ${score}]`);

    const fd = new FormData()
    fd.append("emote", emote)
    fd.append("woop", score)
    fd.append("username", "adi@moe.com")
    const resp = await fetch(endpoints.addCheckin, {
      method: "POST",
      headers: {
        'Authorization': `Token ${global.token}`
      },
      body: fd
    })
    const data = await resp.json()
    console.log(data);

    const day = new Date().toLocaleDateString();
    AsyncStorage.setItem("lastSubmit", day)
    route.params.toggle(true)
    navigation.navigate("MainApp")

  }

  return (
    <SafeAreaView style={globalStyles.engageBgContainer}>
      <Header text="Welcome" navigation={navigation}/>
      <View style={styles.textCont}>
        <Text style={styles.text}>Thank you!</Text>
        <Text style={styles.text}>Please tell us a bit more.</Text>
        <Text style={[styles.text, {fontSize:22}]}>Make sure to answer all questions.</Text>
      </View>
      <Hr/>
      <ScrollView snapToInterval={100}>
        { questionElements }
        <View style = {globalStyles.buttonContainer}>
        <PrimaryButton text="Submit" size={22} style={{height:46, width:143, marginVertical:35, alignSelf:"flex-end", marginRight:20}} onPress={submitQuestions} />  
        </View>
      </ScrollView>
      
    </SafeAreaView>
  );
}