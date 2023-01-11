import { SafeAreaView, ScrollView, StyleSheet, Text, View } from 'react-native'
import colors from '../colors';
import Header from '../components/Header';
import PrimaryButton from '../components/PrimaryButton';
import fonts from '../fonts';
import globalStyles from "../styles"

// we use this screen to avoid having to display entire messages on the message screen since 
// that would fill the screen excessively.

// again, actual message data is pulled from the back end in a previous screen to be displayed here
// in jsx

const styles = StyleSheet.create({
  row: {
    flexDirection: "row",
    alignItems:"center"
  },
  button: {
    height:46,
    paddingHorizontal:15
  },
  label: {
    fontFamily: "Sansita",
    fontSize:22
  },
  text: {
    fontFamily: fonts.prompt,
    fontSize:22
  }
})

export default ({route, navigation}) => {

  const {msgData} = route.params;
  const stamp = new Date(msgData[0])

  return (
    <SafeAreaView style={[globalStyles.engageBgContainer, {justifyContent:"flex-start"}]}>
      <Header text="Message" navigation={navigation} />
      <View style={{flexGrow:1, justifyContent:"space-between", alignSelf:"stretch", marginHorizontal:30, marginVertical:15}}>
        <View>
          <View style={styles.row}>
            <Text style={styles.label}>From: </Text>
            <Text style={styles.text}>{msgData[1]}</Text>
          </View>
          <View style={styles.row}>
            <Text style={styles.label}>Sent: </Text>
            <Text style={styles.text}>{stamp.toDateString()}</Text>
          </View>
          <ScrollView style={{height:360, marginTop:10}}>
            <View style={{
              backgroundColor:colors.white,
              borderWidth:2,
              borderRadius:10,
              padding:10
            }}>
              <Text style={[styles.text, {fontSize:24}]}>{msgData[2]}</Text>
            </View>
          </ScrollView>
        </View>
        <View style={[styles.row, {justifyContent:"space-between", marginHorizontal:20}]}>
          <PrimaryButton text="Back" size={22} style={styles.button} onPress={navigation.goBack} />
          <PrimaryButton text="Reply" size={22} style={styles.button} onPress={() => {
            navigation.navigate("NewMessage", {
              to: msgData[1]
            })
          }} />
        </View>
      </View>
    </SafeAreaView>
  );
} 