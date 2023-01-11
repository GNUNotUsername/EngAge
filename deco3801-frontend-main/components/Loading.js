import { useEffect } from "react"
import { Animated, StyleSheet, Text, View } from "react-native"
import fonts from "../fonts"

const styles = StyleSheet.create({
    container: {
        alignItems: "center"
    },
    text: {
        fontFamily: fonts.prompt,
        fontSize: 32
    }
})

export default props => {
    const rotValue = new Animated.Value(0)

    useEffect(() => {
        Animated.loop(Animated.timing(rotValue, {
            toValue: 1,
            useNativeDriver: true,
            duration: 2200
        })).start()
    }, [rotValue])

    const amount = rotValue.interpolate({
        inputRange: [0, 1],
        outputRange: ['0deg', '360deg']
    })

    return (
        <View style={styles.container}>
            <Animated.Image source={require("../assets/Loading.png")} style={{transform: [{rotate: amount}]}}/>
            <Text style={styles.text}>Loading...</Text>
        </View>
    )
}