import { Pressable, StyleSheet, Text, View } from "react-native"
import colors from "../colors"
import fonts from "../fonts"

const styles = StyleSheet.create({
    container: {
        backgroundColor: colors.white,
        borderRadius: 10,
        borderWidth: 2,
        borderBottomWidth: 4,
        borderRightWidth: 4,
        borderColor: colors.purple,
        flexDirection:"row",
        alignItems: "center",
        padding:5,
        paddingRight: 50,
        marginVertical:5
    },
    text: {
        fontFamily: fonts.prompt,
        fontSize: 20
    }
})

const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

export default props => {
    const [id, name, location, timestamp ] = props.eventData

    const stamp = new Date(timestamp)

    return (
        <Pressable style={styles.container} onPress={props.onPress} >
            <View style={{alignItems:"center", padding:10, marginRight:5}}>
                <Text style={styles.text}>{stamp.getDate()}</Text>
                <Text style={styles.text}>{months[stamp.getMonth()]}</Text>
            </View>
            <View style={{marginRight:15}}>
                <Text style={[styles.text, {fontSize:24}]}>{name}</Text>
            </View>
        </Pressable>
    )
}