# Arduino Playground
This is a simple arduino repo for my some of my personal tests.

## Led Blink
Blinks the led at 1s intervals

## Seven Segment Display
Increments a seven segment counter display on button push via polling

## LCD Display
A simple hello world message on the LCD display

## RealTimeClock and Temperature Sensor
Prints a realtime clock and the temperature sensor data
ds3231.cpp, ds3231.h, config.h can be obtained at https://github.com/rodan/ds3231

## RTC LCD
Using the realtime clock with the LCD display and displaying the datetime as well as the temperature.

## Computer Vision LCD
The webcam feed is parsed using opencv to generate data on which a machine learning model is trained. The trained model then predicts how many fingers are held up are send the data via the serial interface to the arduino LCD display like so:


<p float="left">
    <img src="./Computer_Vision_LCD/demos/monitor.gif" width="400" height="400" />
    <img src="./Computer_Vision_LCD/demos/lcd.gif" width="400" height="400" />
</p>