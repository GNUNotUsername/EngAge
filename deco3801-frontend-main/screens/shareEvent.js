import { SafeAreaView, ScrollView, View, Text } from "react-native";
import Header from "../components/Header";
import Loading from "../components/Loading";
import styles from "../styles";
import { useEffect, useState } from "react";
import endpoints from "../endpoints";
import PrimaryButton from "../components/PrimaryButton";
import IcoButton from "../components/IcoButton"
import colors from "../colors";

// contacts get filled from a backend fetch
// and then a semi-hardcoded message to attend
// (filled with appropriate event name and time)
// is posted to the back end which passes it onto the appropriate 
// contacts 

let contacts = []

export default ({route, navigation}) => {
    const [feedback, setFeedback] = useState()
    const [hasLoaded, setLoaded] = useState()
    const [selected, updateSelect] = useState({})

    const { eventName, niceDate } = route.params

    useEffect(() => {
        const getContacts = async () => {
            try {
                const resp = await fetch(endpoints.getContacts, {
                    headers: {
                        'Authorization': `Token ${global.token}`
                    }
                })
                const data = await resp.json()
                //console.log(data);
                contacts = Object.values(data)
                setLoaded(true)
            } catch (e) {
                console.warn(e)
            }
        }

        getContacts()
    }, [])

    const sendMessages = async () => {
        const message = `Would you interested in going to ${eventName} on ${niceDate}?`
        console.log(message)
        try {
            for (let user in selected) {
                const sending = selected[user]
                if (sending) {
                    const form = new FormData()
                    form.append("user_2", user)
                    form.append("content", message)
                    const resp = await fetch(endpoints.sendMessage, {
                        method: 'POST',
                        headers: {
                            'Authorization': `Token ${global.token}`
                        },
                        body: form
                    })
                    const data = await resp.json()
                    console.log(data);
                }
            }
        } catch (e) {
            console.warn(e)
        }
    }

    return (
        <SafeAreaView style={[styles.engageBgContainer, {justifyContent:"flex-start"}]}>
            <Header text="Share Event" navigation={navigation} />
            <View style={{flexGrow:1, alignSelf:"stretch", margin:35, justifyContent:"space-between"}}>
                { hasLoaded ?
                    (contacts.length > 0) ?
                        <ScrollView>
                            {contacts.map(user => <IcoButton key={user} text={user} onPress={() => {
                                updateSelect({...selected, [user]: !selected[user]})
                            }} active={selected[user]} />)}
                        </ScrollView>
                    :
                        <Text style={{fontFamily:"Sansita", fontSize:22, textAlign:"center", color:colors.purple}}>No contacts. Please add somebody to share an event!</Text>
                :
                    <Loading />
                }
                <View style={{flexDirection:"row", justifyContent:"space-between"}}>
                    <PrimaryButton text="Back" size={22} style={{height:46,width:92}} onPress={navigation.goBack} />
                    <PrimaryButton text="Share" size={22} style={{height:46, width:109}} onPress={sendMessages} disabled={!Object.values(selected).includes(true)} />
                </View>
            </View>
        </SafeAreaView>
    )
}