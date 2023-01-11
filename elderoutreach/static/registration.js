function TestScreen({navigation}) {
  // first name, last name, email, phone number, password
  // super hacky right now
  const [firstName, onChangeFirst] = React.useState('first name');
  const [lastName, onChangeLast] = React.useState('last name');
  const [email, onChangeEmail] = React.useState('email');
  const [phone, onChangePhone] = React.useState('phone');
  const [password, onChangePassword] = React.useState('password');
  
  render(){
    return (
    <SafeAreaView style = {{flex : 1, alignItems : 'center', justifyContent : 'center'}}>
      <Text style = {styles.formText}> first name</Text>
      <TextInput
        onChangeText={onChangeFirst}
        value = {firstName}
      />
      <Text style = {styles.formText}> last name</Text>
      <TextInput
        onChangeText={onChangeLast}
        value = {lastName}
      />
      <Text style = {styles.formText}> email </Text>
      <TextInput
        onChangeText={onChangeEmail}
        value = {email}
      />
      <Text style = {styles.formText}> phone number </Text>
      <TextInput
        onChangeText={onChangePhone}
        value = {phone}
      />
      <Text style = {styles.formText}> password </Text>
      <TextInput
        onChangeText={onChangePassword}
        value = {password}
      />
    </SafeAreaView>
  );
  }
}

function HomeScreen({navigation})
{
  let [fontsLoaded] = useFonts({
    Prompt_400Regular
  });

  if (!fontsLoaded) {
    // TODO: Replace with proper loading element
    return (
      <View style={styles.container}>
        <Text>Loading...</Text>
      </View>
    )
  }

  return (    
    <>
    <View style={styles.container}>
      <LinearGradient colors={["#ffa700", "#ff8700", "#ff6700"]} locations={[0, 0.66, 1]} style={styles.bg} end={{x: 0.4, y: 0.9}} />
      <Text style={styles.text}>Welcome to the App.</Text>
      <StatusBar style="auto" />
      <Button 
        title = "go to test screen"
        onPress = {() => navigation.navigate('Test')}
       />
    </View>
    
    <MapView 
    style = {{flex: 1}}
    provider = {PROVIDER_GOOGLE}
    showsUserLocation
    // I guess you would pull latitude and longitude from
    // event locations
    initialRegion = {{
      latitude : -27.49, 
      longitude : 153,
      latitudeDelta : 0.0922,
      longitudeDelta: 0.0421,
    }}>
    </MapView>
    </>    
  );
}

const Stack = createNativeStackNavigator();

export default function App() {
  
  return (
    <NavigationContainer> 
    <Stack.Navigator initialRouteName= "Home">
      <Stack.Screen name = "Home" component = {HomeScreen} />
      <Stack.Screen name = "Test" component = {TestScreen} />
    </Stack.Navigator>
    </NavigationContainer> 
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'red',
    alignItems: 'center',
    justifyContent: 'center'
  },

  text: {
    color:'white',
    fontFamily: "Prompt_400Regular",
    fontSize: 40,
    textAlign: 'center'
  },

  formText: {
    color:'red',
    fontFamily: "Prompt_400Regular",
    fontSize : 20,
    textAlign: 'center'
  },

  bg: {
    position: 'absolute',
    left: 0,
    top: 0,
    right:0,
    bottom:0
  }
});
