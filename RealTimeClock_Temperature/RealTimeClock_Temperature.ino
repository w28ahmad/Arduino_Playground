#include <Wire.h>
#include "ds3231.h"

struct ts t;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Wire.begin();
  DS3231_init(DS3231_CONTROL_INTCN);

  t.hour=1; 
  t.min=11;
  t.sec=0;
  t.mday=19;
  t.mon=8;
  t.year=2021;
 
  DS3231_set(t);

}

void loop() {
  DS3231_get(&t);
  float temp = DS3231_get_treg();
  Serial.print("Date : ");
  Serial.print(t.mday);
  Serial.print("/");
  Serial.print(t.mon);
  Serial.print("/");
  Serial.print(t.year);
  Serial.print("\t Hour : ");
  Serial.print(t.hour);
  Serial.print(":");
  Serial.print(t.min);
  Serial.print(".");
  Serial.println(t.sec);

  Serial.print("Temperature : ");
  Serial.println(temp);
 
  delay(1000);
}
