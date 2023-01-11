import { Pressable, StyleSheet, Text, View } from "react-native"
import colors from "../colors"
import fonts from "../fonts"

// we use the emoji component
// throughout the app in the questionaire

const styles = StyleSheet.create({
    container: {
        alignItems:"center",
        margin:8,
        // marginHorizontal:10
    },
    circle: {
        width:90,
        height:90,
        borderRadius:50,
        borderColor:colors.purple,
        borderTopWidth:2,
        borderLeftWidth:2,
        borderBottomWidth:4,
        borderRightWidth:4,
        paddingBottom: 2,
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: colors.white
    },
    selected: {
        backgroundColor: colors.blue
    },
    emote: {
        fontSize:50
    },
    label: {
        fontFamily: fonts.prompt,
        color: colors.purple,
        fontSize: 21
    }
})

export default (props) => {

    const onSelect = () => props.onPress(props.label)

    return (
        <View style={styles.container} accessibilityLabel={props.label} accessibilityRole="checkbox" accessibilityState={{checked: props.label==props.selected}}>
            <Pressable style={[styles.circle, props.selected===props.label && styles.selected]} onPress={onSelect}>
                <Text style={styles.emote}>{props.emote}</Text>
            </Pressable>
            <Text style={styles.label}>{props.label}</Text>
        </View>
    )
}