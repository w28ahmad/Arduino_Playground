#define TRIGPIN 2
#define ECHOPIN 3
#define FANPIN 8

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); // Starting Serial Terminal
  pinMode(TRIGPIN, OUTPUT);
  pinMode(ECHOPIN, INPUT);
  pinMode(FANPIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
   long duration, inches, cm;

   digitalWrite(TRIGPIN, LOW);
   delayMicroseconds(2);
   digitalWrite(TRIGPIN, HIGH);
   delayMicroseconds(10);
   digitalWrite(TRIGPIN, LOW);

   duration = pulseIn(ECHOPIN, HIGH);
   cm = duration /29 / 2;
   
   Serial.print(cm);
   Serial.print("cm");
   Serial.println();
   Serial.print(duration);
   Serial.print("ms");
   Serial.println();
  Serial.println();
  if(cm < 150){
    analogWrite(FANPIN, 255);
  }else{
    analogWrite(FANPIN, 0);
  }
  
  
   delay(1000);
}
