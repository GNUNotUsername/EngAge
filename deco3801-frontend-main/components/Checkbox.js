import { Pressable, StyleSheet, Text, View } from "react-native"
import colors from "../colors"
import fonts from "../fonts"

// we use the checkbox 
// for selecting interests 


// note how much more convenient this is compared to css/html
const style = StyleSheet.create({
    square: {
        width:45,
        height:45,
        backgroundColor: colors.white,
        borderRadius: 10,
        borderColor: colors.purple,
        borderBottomWidth: 4,
        borderRightWidth: 4,
        borderTopWidth: 2,
        borderLeftWidth: 2
    },
    selected: {
        backgroundColor: colors.blue
    },
    label: {
        fontFamily: fonts.prompt,
        textAlign: "center",
        fontSize: 20
    },
    container: {
        alignItems: "center"
    }
})


export default (props) => {

    const onSelect = () => {
        props.onChange(props.label);
    }

    return (
        <View style={style.container} accessibilityLabel={props.label} accessibilityRole="checkbox" accessibilityState={{checked: props.label==props.active}}>
            <Pressable style={[style.square, props.active==props.label && style.selected]} onPress={onSelect}/>
            <Text style={style.label}>{props.label}</Text>
        </View>
    )
}