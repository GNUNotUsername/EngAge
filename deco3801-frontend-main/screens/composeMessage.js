import { Keyboard, Pressable, SafeAreaView, StyleSheet, Text, TextInput, View } from "react-native"
import { useState } from "react"
import Header from "../components/Header"
import globalStyles from "../styles"
import colors from "../colors"
import PrimaryButton from "../components/PrimaryButton"
import fonts from "../fonts"
import endpoints from "../endpoints"

// message composition gets a message via an updateMessage callback
// which is then posted in a form to the backend to the appropriate user

const styles = StyleSheet.create({
    row: {
        flexDirection: "row",
        alignItems:"center"
    },
    input: {
        height:130,
        textAlignVertical: 'top',
        paddingVertical: 10,
        paddingRight:10
    },
    response: {
        backgroundColor: colors.white,
        borderRadius: 10,
        borderWidth: 2,
        borderBottomWidth: 4,
        borderRightWidth: 4,
        borderColor: colors.purple,
        padding:10,
        marginVertical: 5
    },
    feedback: {
        fontFamily: fonts.prompt,
        fontSize: 28,
        textAlign: "center",
        marginHorizontal:10
    }
})

const QuickReply = props => {
    return (
        <Pressable style={styles.response} onPress={props.onPress}>
            <Text style={{fontFamily:fonts.prompt, fontSize: 20}}>{props.value}</Text>
        </Pressable>
    )
}

const replies = ['How are you?', "Let's get together.", "What are you doing today?"]

export default ({route, navigation}) => {
    const { to } = route.params
    const [message, updateMessage] = useState("")
    const [feedback, setFeedback] = useState(false)

    if (route.params.msg) {
        updateMessage(route.params.msg)
    }

    const onSend = () => {
        const sendMsg = async () => {
            const form = new FormData()
            form.append("user_2", to)
            form.append("content", message)

            try {
                const resp = await fetch(endpoints.sendMessage, {
                    method: "POST",
                    headers: {
                        'Authorization': `Token ${global.token}`
                    },
                    body: form
                })
                const reply = await resp.json()
                console.log(reply);

                if (reply.status && reply.status=="success") {
                    setFeedback(`Your message has been sent to ${to}`)
                    console.log(feedback);
                }

            } catch (e) {
                console.warn(e);
            }
        }

        Keyboard.dismiss()
        sendMsg()
    }

    return (
        <SafeAreaView style={[globalStyles.engageBgContainer, {justifyContent:"flex-start"}]}>
            <Header text="Messages" navigation={navigation} />
            <View style={{flexGrow:1, justifyContent:"space-between", alignItems:"center"}}>
                <View>
                    <View style={styles.row}>
                        <Text style={{fontFamily:"Sansita", fontSize:22}}>To: </Text>
                        <Text style={{fontFamily:fonts.prompt, fontSize:22}}>{to}</Text>
                    </View>
                    <TextInput style={[globalStyles.inputContainer, styles.input]} placeholder="Type your message here" multiline={true} value={message} onChangeText={updateMessage} />
                    { !feedback ?
                        <PrimaryButton text="Send" size={22} style={{height:46, width:109, alignSelf:"flex-end"}} onPress={onSend} />
                        : null
                    }
                </View>
                <View>
                    { !feedback ?
                        replies.map(val => (<QuickReply key={val} value={val} onPress={() => {
                            updateMessage(message + val)
                        }} />))
                        : <Text style={styles.feedback}>{feedback}</Text>
                    }
                </View>
                <View style={{alignSelf:"flex-start"}}>
                    <PrimaryButton text="Back" size={22} style={{height:46, width:92}} onPress={navigation.goBack} />
                </View>
            </View>
        </SafeAreaView>
    )
}