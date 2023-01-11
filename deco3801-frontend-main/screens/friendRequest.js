import { Text, SafeAreaView, StyleSheet, View } from "react-native"
import Header from "../components/Header"
import PrimaryButton from "../components/PrimaryButton"
import SelectableButton from "../components/SelectableButton"
import globalStyles from "../styles"
import { useState } from "react"
import endpoints from "../endpoints"

// friend requests are handled by posting a form
// (which has its fields set via callbacks)
// to backend

const styles = StyleSheet.create({
    buttons: {
        width:191,
        height: 46
    },
    text: {
        fontFamily: "Sansita",
        textAlign: "center",
        fontSize: 26
    }
})

export default ({route, navigation}) => {

    const { from } = route.params
    const [status, setStatus] = useState(false)
    const [feedback, setFeedback] = useState(false)

    const submit = async choice => {
        if (feedback) return
        setStatus(choice)
        if (choice == "accept")
            setFeedback(from + " has been added to your contacts!")
        else
            setFeedback(from + "'s request has been denied")
        
        const form = new FormData()
        form.append("user_1", from)
        form.append("choice", choice)
        const resp = await fetch(endpoints.acceptFriendRequest, {
            method: "POST",
            headers: {
                'Authorization': `Token ${global.token}`
            },
            body: form
        })
        const data = await resp.json()
        // console.log(data)
    }

    return (
        <SafeAreaView style={[globalStyles.engageBgContainer, {justifyContent:"flex-start"}]}>
            <Header text="Contacts" />
            <View style={{flexGrow: 1, alignSelf: "stretch", margin: 35, justifyContent: "space-between"}}>
                <View style={{alignItems:"center"}}>
                    <Text style={styles.text}>{from} sent you a friend request!</Text>
                    <SelectableButton text="Accept" size={22} style={[styles.buttons, {marginVertical:10}]} active={status == "accept"} onPress={() => submit("accept")} />
                    <SelectableButton text="Reject" size={22} style={styles.buttons} active={status == "reject"} onPress={() => submit("reject")} secondary />
                </View>
                { feedback ? <Text style={globalStyles.walkthroughText}>{feedback}</Text> : null
                }
                <PrimaryButton text="Back" size={22} style={{height:46, width:92}} onPress={navigation.goBack} />
            </View>
        </SafeAreaView>
    )
}