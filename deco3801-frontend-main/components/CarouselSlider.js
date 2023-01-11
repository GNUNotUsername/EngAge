import {React, useRef, useState} from "react";
import {Dimensions, View, Text, Button} from "react-native";
import Carousel from "react-native-snap-carousel";
import CarouselItem from "./CarouselItem";
import styles from "../styles";
import Paging from "./Paging";




const {width} = Dimensions.get("window");



// this function allows us to pass in data into the carousel for display

export default function CarouselSlider({data}) {
    const carouselRef = useRef(null);
    const [slideIndex, setSlideIndex] = useState(0);

    const settings = {
        sliderWidth : width,
        sliderHeight : width-40,
        itemWidth : width-10,
        itemHeight : 10,
        data : data,
        renderItem : CarouselItem,
        hasParallaxImages : true,
        onSnapToItem : (index) => setSlideIndex(index)

    };
    return (    
            <View style = {styles.carouselContainer}>
            <Carousel 
            ref = {carouselRef}
            {...settings} /> 
            <Paging data = {data} activeSlide = {slideIndex} />        
            </View>   
        
    );
}
