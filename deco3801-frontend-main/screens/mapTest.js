import MapView, {PROVIDER_GOOGLE} from "react-native-maps";

// obsolete prototyping for using maps when we were starting out

export default ({navigation}) => {
  return (
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
  );
}