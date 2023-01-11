import { useState } from "react";
import { Keyboard, SafeAreaView, StyleSheet, Text, TextInput, View } from "react-native"
import Header from "../components/Header"
import PrimaryButton from "../components/PrimaryButton"
import endpoints from "../endpoints";
import globalStyles from "../styles"

// for contacts, we create a form to send to the backend,
// provide a token, and send the form. 
// then based on the response we either handle the error and provide the appropriate message, or 
// relay the successful adding of a new contact

const styles = StyleSheet.create({
    text: {
        fontFamily: "Sansita",
        fontSize: 24,
        marginBottom: 10
    },
    container: {
        justifyContent: "space-between",
        flexGrow: 1,
        marginHorizontal: 35,
        paddingVertical: 15
    },
});

export default ({navigation}) => {
    const [feedback, updateFeedback] = useState("")
    const [toAdd, updateToAdd] = useState("")

    const submitRequest = () => {
        const sendReq = async () => {
            try {
                const form = new FormData()
                form.append("user_2", toAdd)

                const raw = await fetch(endpoints.sendFriendRequest, {
                    method: "POST",
                    headers: {
                        'Authorization': `Token ${global.token}`
                    },
                    body: form
                })
                //const resp = await raw.json();
                const resp = await raw.text();
                console.log(resp);
                
                if (resp.error) {
                    switch (resp.error) {
                        case "not_found":
                            updateFeedback("We couldn't find anyone with that email address")
                            break;
                        case "save_error":
                            updateFeedback("You've already sent a request to this person")
                            break;
                        default:
                            updateFeedback("Something went wrong")
                    }
                } else {
                    updateFeedback("Your request has been sent!")
                }

            } catch (e) {
                console.warn(e);
            }
        }
        Keyboard.dismiss()
        updateFeedback("Sending...")
        sendReq()
    }

    return (
        <SafeAreaView style={[globalStyles.engageBgContainer, {justifyContent: "flex-start"}]}>
            <Header text="Contacts" navigation={navigation} />
            <View style={styles.container}>
                <View style={{justifyContent: "center", alignItems: "center"}}>
                    <Text style={styles.text}>
                        Enter the email address of the person you wish to add:
                    </Text>
                    <TextInput style={globalStyles.inputContainer} placeholder="Email Address" keyboardType="email-address" value={toAdd} onChangeText={updateToAdd} />
                    <PrimaryButton text="Send request" size={22} style={{height:46, width:190}} onPress={submitRequest} />
                </View>
                <View>
                    <Text style={[styles.text]}>{feedback}</Text>
                </View>
                <View>
                    <PrimaryButton style={{width:92, height:46}} text="Back" size={22} onPress={navigation.goBack} />
                </View>
            </View>
        </SafeAreaView>
    )
}