import { Image, Text, SafeAreaView } from 'react-native';
import styles from "../styles";
import PrimaryButton from '../components/PrimaryButton';
import CarouselSlider from '../components/CarouselSlider';

// this is where we use the carousel slider
// to present the walkthrough pages
// with their accompanying images loaded locally

import walkthroughImage1 from '../assets/walkthru_emojis.png';
import walkthroughImage2 from '../assets/walkthru_emojis_2.png';
import walkthroughImage3 from '../assets/walkthru_emojis_3.png';
import walkthroughImage4 from '../assets/walkthru_emojis_4.png';
import walkthroughImage5 from '../assets/walkthru_emojis_5.png';
import walkthroughImage6 from '../assets/walkthru_emojis_6.png';
import walkthroughImage7 from '../assets/walkthru_emojis_7.png';

const walkthruImage1Uri = Image.resolveAssetSource(walkthroughImage1).uri;
const walkthruImage2Uri = Image.resolveAssetSource(walkthroughImage2).uri;
const walkthruImage3Uri = Image.resolveAssetSource(walkthroughImage3).uri;
const walkthruImage4Uri = Image.resolveAssetSource(walkthroughImage4).uri;
const walkthruImage5Uri = Image.resolveAssetSource(walkthroughImage5).uri;
const walkthruImage6Uri = Image.resolveAssetSource(walkthroughImage6).uri;
const walkthruImage7Uri = Image.resolveAssetSource(walkthroughImage7).uri;

const walkthroughData = [
  {
    title: "Wellbeing Feedback",
    description: "Select an emoji that describes your current mood. Your selected mood should turn green. We will be collecting this feedback daily!",
    imageUri: walkthruImage1Uri
  },
  {
    title: "Wellbeing Feedback",
    description: "Select an option that best answers each question. The selected option should turn green. Make sure you scroll until you answer all questions.",
    imageUri: walkthruImage2Uri
  },
  {
    title: "Events",
    description: "Select any event you want to view more information about. If the event interests you, hit 'Going' or 'Send to a friend!'",
    imageUri: walkthruImage3Uri
  },
  {
    title: "Transport",
    description: "You can view available transport options. You will be able to select 'Maps' for more details.",
    imageUri: walkthruImage4Uri
  },
  {
    title: "Messages",
    description: "Select 'Send New Message' to send a message to a contact. You can view or continue previous conversations.",
    imageUri: walkthruImage5Uri
  },
  {
    title: "Messages",
    description: "Type a new message or select a message from the suggestions. Hit 'Send' when you're ready!",
    imageUri: walkthruImage6Uri
  },
  {
    title: "Notifications",
    description: "Click on the notifications bell in the top right corner to view reminders, upcoming events and event suggestions!",
    imageUri: walkthruImage7Uri
  },
];



export default ({route, navigation}) => {
  
  return (
    <SafeAreaView style={styles.engageBgContainer}>
      
      <Text style={{...styles.text, fontSize:60, fontFamily:'Sansita'}}>EngAge</Text>
      
      
      <CarouselSlider data = {walkthroughData} />
      
      <PrimaryButton text='Continue' fontSize={22} size={32} style={{width:230, height:60}} 
        onPress = {() => {
          if (route.params && route.params.goBack)
            navigation.goBack()
          else
            navigation.navigate('InterestScreen')
        }}
      />
    </SafeAreaView>
  );
}

