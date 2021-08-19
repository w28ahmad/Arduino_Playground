#include <LiquidCrystal.h>
#include <Wire.h>
#include "ds3231.h"

// Pin mapping
#define rs 2
#define rw 3
#define en 4
#define d0 5
#define d1 6
#define d2 7
#define d3 8
#define d4 9
#define d5 10
#define d6 11
#define d7 12

// Globals
struct ts t;
float temperature;
const char* months[12] = {"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"};

// Initialize LCD
LiquidCrystal lcd(rs, rw, en, d0, d1, d2, d3, d4, d5, d6, d7);

void setup() {
  // put your setup code here, to run once:
  lcd.begin(16, 2);

  // Initialize to current time
  Wire.begin();
  DS3231_init(DS3231_CONTROL_INTCN);

  t.hour=1; 
  t.min=59;
  t.sec=50;
  t.mday=19;
  t.mon=8;
  t.year=2021;
 
  DS3231_set(t);
}

void loop() {
  // put your main code here, to run repeatedly:
  // Get datetime
  DS3231_get(&t);
  // Get temperature
  temperature = DS3231_get_treg();

  // Display Date
  lcd.setCursor(0,0);
  lcd.print( (t.mday < 10 ? "0" + String(t.mday) : String(t.mday)) +"th "+months[t.mon-1]+".");
  lcd.setCursor(12,0);
  lcd.print(String(t.year));

  // Display Time
  lcd.setCursor(0,1);
  lcd.print((t.hour < 10 ? "0"+String(t.hour) : String(t.hour)) +":"+  \
            (t.min < 10 ? "0"+String(t.min) : String(t.min)) + ":" +  \
            (t.sec < 10 ? "0"+String(t.sec) : String(t.sec)));

  // Display Temperature
  lcd.setCursor(10,1);
  lcd.print(String(temperature)+"C");
  
  // Update one second later
  delay(1000);
}
