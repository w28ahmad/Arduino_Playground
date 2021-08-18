#include "SegmentDisplay.h"
#include "Arduino.h"

SegmentDisplay::SegmentDisplay(int pin1, int pin2, int pin3, int pin4, int pin5, int pin6, int pin7) {
    
    pins[0] = pin1; // A
    pins[1] = pin2; // B
    pins[2] = pin3; // C
    pins[3] = pin4; // D
    pins[4] = pin5; // E
    pins[5] = pin6; // F
    pins[6] = pin7; // G

    
    for(int i = 0; i < 7; i++) {
        pinMode(pins[i], OUTPUT);
        digitalWrite(pins[i], HIGH);
    }
}

void SegmentDisplay::displayHex(int number) {
    boolean bitToWrite;
    for(int segment = 0; segment < 7; segment++) {
        bitToWrite = bitRead(numbersToDisplay[number], 6-segment);
        digitalWrite(pins[segment], bitToWrite);
    }
}
