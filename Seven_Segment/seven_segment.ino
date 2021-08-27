/****************************************************
 *                    7 SEGMENT
 *
 *                        A=5
 *               ___________________
 *              |                   |
 *              |                   |
 *              |                   |
 *              |                   |
 *          F=8 |                   | B=4
 *              |                   |
 *              |         G=9       |
 *              |___________________|
 *              |                   |
 *              |                   |
 *              |                   |
 *              |                   |
 *          E=11|                   | C=5   ____
 *              |                   |      /    \
 *              |         D=10      |      | DP |   <- Not used
 *              |___________________|      \____/
 * 
 *
 *        ABCDEFG
 * ONE =  0110000
 *      .
 *      .
 *      .
 ********************************************************/

#include "SegmentDisplay.h"

/*
 * Defines
 */
#define A_PIN  5
#define B_PIN  4
#define C_PIN  3
#define D_PIN  10
#define E_PIN  11
#define F_PIN  8
#define G_PIN  9

#define BTN_PIN 2

/*
 * Typedefs
 */
typedef long long ll;

/*
 * Globals
 */
SegmentDisplay* s1;
int i=0;
ll lastSwitchDetectedMillis = (ll)millis();
int debounceInterval = 250;

/*
 * Functions
 */
void setup(){
  // put your setup code here, to run once:
  pinMode(BTN_PIN, INPUT);
  s1 = new SegmentDisplay(A_PIN, B_PIN, C_PIN, D_PIN, E_PIN, F_PIN, G_PIN);
}

void loop() {
  // put your main code here, to run repeatedly:
  s1->displayHex(i);

  if (millis() - lastSwitchDetectedMillis > debounceInterval) {  
    int btn_pressed = digitalRead(BTN_PIN);
    if(btn_pressed){
        i = (i+1) % 10;
    }
    lastSwitchDetectedMillis=(ll)millis();
  }
}
