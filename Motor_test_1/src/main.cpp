#include <Arduino.h>
#include <Servo.h>
#define servo_pin_1 9
#define servo_pin_2 10
#define analog_pin A0

Servo yawServo;
Servo pitchServo;
unsigned long previousMillis = 0;
int blinkInterval = 300;    // Updated live from the potentiometer
int val = 0;

void loop() {
  // Code that loops
}

void readData(){
  // Reads data from the sensor
}

void moveYawServo(){
  // Yaw is also commonly understood as Pan
  // Moves servo from 0 to 180, stopping at each 5 degrees
  // This method will always do a sweep from 0 to 180

  for (int angle = 0; angle < 180; angle = angle + 5)
  {
    Serial.println("Yaw: " + angle);
    yawServo.write(angle);
    delay(1000);
  }
}

void movePitchServo(int pitchAngle=0){
  // Pitch is also commonly understood as Tilt
  // This method writes the current pitch angle to the position
  pitchServo.write(pitchAngle);
  Serial.println("Pitch " + pitchAngle);
  delay(1000);
}

void sendData(){
  // Sends data to serial port python 
}

void controlByPot(){
  // Manual control for the Servo, great for manual debugging
  val = analogRead(analog_pin);
  val = map(val, 0, 1023, 0, 180);
  unsigned long currentMicros = micros();
}

void scanOnce(){
  // Scans once, moving the Yaw servo a full 180 degrees, and then increments the Pitch servo
  // Yaw sweeps from 0 to 180, stopping each 5 degrees
  // Pitch servo is initially at 0, it will sweep to 180, stopping each 10 degrees
  for (int angle = 0; angle < 180; angle = angle + 10)
  {
    movePitchServo(angle);
    //moveYawServo();
  }
}

void kill(){
  // kill the motor
  yawServo.write(0);
  pitchServo.write(0);
}

void setup() {
  // Code that runs on startup
  Serial.begin(9600);
  yawServo.attach(9);
  pitchServo.attach(10);
  pinMode(servo_pin_1, OUTPUT);
  pinMode(servo_pin_2, OUTPUT);
  pinMode(analog_pin, INPUT_PULLUP);

  // set both servo to default positions
  yawServo.write(0);
  pitchServo.write(0);
  scanOnce();
}