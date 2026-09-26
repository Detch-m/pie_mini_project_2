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
int yawStart_val = 30;
int yawEnd_val = 120;
int pitchStart_val = 30;
int pitchEnd_val = 150;

void loop() {
  // Code that loops
}

void readData(){
  // Reads data from the sensor
}

void sendData(){
  // Sends data to serial port python 
}

void moveYawServo(int yawAngle){
  // Yaw is also commonly understood as Pan
  // Moves servo to angle location
  yawServo.write(yawAngle);
  Serial.println("Yaw " + yawAngle);
  delay(1000);
}

void movePitchServo(int pitchStart, int pitchEnd){
  // Pitch is also commonly understood as Tilt
  // Moves pitch from pitchStart to pitchEnd, stoppping at each 5 degrees
  for (int angle = pitchStart; angle < pitchEnd; angle = angle + 5)
  {
    Serial.println("pitch: " + angle);
    pitchServo.write(angle);
    delay(1000);
  }
}

void controlByPot(){
  // Manual control for the Servo, great for manual debugging
  val = analogRead(analog_pin);
  val = map(val, 0, 1023, 0, 180);
  unsigned long currentMicros = micros();
}

void scanOnce(int yawStart, int yawEnd, int pitchStart, int pitchEnd){
  // Scans once, moving the Yaw servo a full 180 degrees, and then increments the Pitch servo
  // Yaw sweeps from 0 to 180, stopping each 5 degrees
  // Pitch servo is initially at 0, it will sweep to 180, stopping each 10 degrees
  for (int angle = yawStart; angle < yawEnd; angle = angle + 10)
  {
    movePitchServo(pitchStart, pitchEnd);
    moveYawServo(angle); 
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
  delay(2000);
  scanOnce(yawStart_val, yawEnd_val, pitchStart_val, pitchEnd_val);
}