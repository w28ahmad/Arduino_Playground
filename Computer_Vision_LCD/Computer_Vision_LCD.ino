#include <LiquidCrystal.h>

#define rs 2
#define en 7
#define d4 3
#define d5 4
#define d6 5
#define d7 6

LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
int val;

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.clear();
//  lcd.print("Hello World");
}

void loop() {
  if (Serial.available() > 0){
    val = Serial.read()-'0';
    lcd.setCursor(0,0);
    lcd.print(String(val));
  }
}
