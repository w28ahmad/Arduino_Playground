#include "Arduino.h"

class SegmentDisplay
{
    public:
      SegmentDisplay(int pin1, int pin2, int pin3, int pin4, int pin5, int pin6, int pin7);
      void displayHex(int numberToDisplay);
    private:
        int pins[7];
        byte numbersToDisplay[10] = {
            B1111110,  //  0
            B0110000,  //  1
            B1101101,  //  2
            B1111001,  //  3
            B0110011,  //  4
            B1011011,  //  5
            B1011111,  //  6
            B1110000,  //  7
            B1111111,  //  8
            B1111011,  //  9
        };
};
