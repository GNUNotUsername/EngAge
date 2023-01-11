import * as React from "react";
import data from "react-native-ico-material-design/src/data";
import {Pagination} from "react-native-snap-carousel";
import styles from "../styles";

// this component is used to get the status dots for the walkthrough screen
// so any aesthetic adjusments to that are done here

export default function Paging({data, activeSlide}) {
    const settings = {
        dotsLength : data.length,
        activeDotIndex : activeSlide,
        containerStyle : styles.carouselDotContainer,
        dotStyle : styles.carouselDotStyle,
        inactiveDotStyle : styles.carouselInactiveDotStyle,
        inactiveDotOpacity : 0.9,
        inactiveDotScale : 0.6,
    };
    return <Pagination {...settings} />;
}