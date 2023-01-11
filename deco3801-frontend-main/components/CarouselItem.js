import React from 'react';
import { ParallaxImage } from 'react-native-snap-carousel';
import { View, Text, Pressable, SafeAreaView } from 'react-native';
import styles from '../styles';

function CarouselItem({item, index}, parallaxProps) {
    // basically returns a bunch of jsx for rendering the carousel   
    // also note that it takes an 'item', which we'll be using 
    // as an image + description + title 
    

    return (
      <Pressable onPress = {() => alert(item.title)}>
        <SafeAreaView style = {styles.carouselItem}>
        <Text style = {{...styles.purpleText, fontFamily: 'Sansita'}}>
            {item.title}
          </Text>
          <ParallaxImage          
          source = {{uri : item.imageUri}} 
          containerStyle = {styles.carouselImageContainer}
          style = {styles.carouselImage}
          {...parallaxProps}/>
          <Text style = {styles.walkthroughText}>
            {item.description}
          </Text>
        </SafeAreaView>
  
      </Pressable>
    );
  }

  export default CarouselItem;