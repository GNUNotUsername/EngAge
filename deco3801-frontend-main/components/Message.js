import { Pressable, StyleSheet, Text } from "react-native"
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
        paddingVertical: 5,
        paddingHorizontal: 10,
        marginVertical:5
    },
    text: {
        fontFamily: fonts.prompt
    }
})

const days = ['Sun', 'Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat']
const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

export default props => {

    const date = new Date(props.sent)
    const stamp = `${days[date.getDay()]} ${date.getDate()} ${months[date.getMonth()]}`

    return (
        <Pressable style={styles.container} onPress={props.onPress}>
            <Text style={[styles.text, {fontSize: 17}]}>From: {props.from}, {stamp}</Text>
            <Text style={[styles.text, {fontSize: 24}]} numberOfLines={5}>{props.msg}</Text>
        </Pressable>
    )
}