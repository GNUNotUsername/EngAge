import { StyleSheet, Text, View } from 'react-native'
import Checkbox from './Checkbox'

// this component is used for the mood check-in questions


const styles = StyleSheet.create({
    heading: {
        fontFamily: "Sansita",
        fontSize: 23,
        textAlign: "center"
    },
    boxes: {
        flexDirection: "row",
        justifyContent: "space-evenly"
        
    }
});

const defaultOptions = [
    'Awful',
    'Bad',
    'Okay',
    'Good',
    'Great'
]

export default (props) => {
    const options = props.options || defaultOptions
    const checkboxes = options.map(value => (
        <Checkbox key={value} label={value} onChange={props.onSelect} active={props.active}/>
    ))

    return (
        <View style={props.style}>
            <Text style={styles.heading}>{props.q}</Text>
            <View style={styles.boxes}>
                {checkboxes}
            </View>
        </View>
    )
}