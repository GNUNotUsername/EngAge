import ButtonCore from "./ButtonCore"
import colors from "../colors"

// this component derives from the button core and extends it for selectability

export default props => {
    const bg = props.secondary ? colors.white : colors.orange
    const fg = props.secondary ? colors.orange : colors.white

    return <ButtonCore {...props} bgColor={props.active ? colors.blue : bg} fgColor={props.active ? colors.purple : fg} />
}