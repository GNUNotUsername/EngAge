import { useState, useEffect } from 'react';
import { Dimensions, SafeAreaView, ScrollView, Text, View } from 'react-native';
import colors from '../colors';
import Hr from '../components/Hr';
import IcoButton from '../components/IcoButton';
import Loading from '../components/Loading';
import PrimaryButton from '../components/PrimaryButton';
import styles from "../styles"
import images from "../images"
import endpoints from '../endpoints';

// we pull events from the backend and then allow a user to select
// their interests before posting 
// the interests to the backend

let interestsData = {}

export default ({route, navigation}) => {
  const isEditing = route.params && route.params.editing
  const [isLoaded, setLoaded] = useState(false)
  const [formData, updateForm] = useState({})

  const screenWidth = Dimensions.get('window').width;

  // Will only run ONCE - when the component first mounts
  useEffect(() => {
    const getInterests = async () => {
      try {
        // Get the list of interests
        const resp = await fetch(endpoints.getInterests)
        const json = await resp.json()
        interestsData = json

        // If we're editing, we need the previous list of interests
        if (isEditing) {
          const resp2 = await fetch(endpoints.getUserInterests, {
            headers: {
              'Authorization': `Token ${global.token}`
            }
          })
          const json2 = await resp2.json()
          // const json2 = await resp2.text()
          console.log(json2);

          let sentData = {}
          // const ids = Object.values(json2)
          // console.log(ids);
          for (let id in json2) {
            console.log(id);
            sentData[id] = true
          }

          updateForm(sentData)
        }

        setLoaded(true)
      } catch (err) {
        //navigation.navigate("MainApp");
        console.warn(err)
      }
    }
    getInterests()
  }, [])

  const interests = Object.entries(interestsData).map(([i,val]) => {
    return (
      <IcoButton key={i} text={val}
        onPress={() => {
          updateForm({...formData, [i]: !formData[i]})
        }}
        active={formData[i]} image={images[i - 1]}
      />
    )
  })

  const saveInterests = async () => {
    const fd = new FormData()
    const submission = []
    const interestEntries = Object.entries(formData);
    for (let [key, val] of interestEntries) {
      if (val === true) {
        console.log("Appending", key);
        // submission.append("interests", key)
        submission.push(key)
      }
    }

    fd.append("interests", submission.join())
    //console.log(Sending);
    try {
      let resp = await fetch(endpoints.saveInterests, {
        method: "POST",
        headers: {
          'Authorization': `Token ${global.token}`
        },
        body: fd
      })
      let parsed = await resp.text()
      console.log(parsed);
    } catch (e) {
      console.warn(e);
    }

    if (isEditing) {
      navigation.navigate("MainApp", {screen: "Options"});
    } else {
      navigation.navigate("MainApp");
    }
  }

  return (
    <SafeAreaView style={[styles.engageBgContainer, {justifyContent:"flex-start", alignItems:"flex-start"}]}>
      <Text style={{...styles.text, fontSize: 42, fontFamily: 'Sansita', marginTop: 40, marginLeft: 20, color: colors.purple}}>Welcome!</Text>
      <Text style={{...styles.purpleText, fontSize: 26, fontFamily: 'Sansita', marginHorizontal: 20, color: colors.purple, textAlign:"left", marginTop:5, marginBottom:20}}>Please select your interests</Text>
      <Hr/>
      <View style={{justifyContent:"center", alignItems:"center", flexGrow:1, alignSelf:"center", paddingHorizontal:30}}>
        {isLoaded ? <ScrollView contentContainerStyle={{paddingBottom: 200, paddingLeft: 10, paddingRight: 10}} >
          { interests }
          <PrimaryButton text="Continue" size={22} style={{height: 46, width: 143, alignSelf: "flex-end"}} onPress={saveInterests} />
        </ScrollView>
        :
        <Loading />
        }
      </View>
    </SafeAreaView>
  )
} 



