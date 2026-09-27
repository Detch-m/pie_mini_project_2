#include <Arduino.h>
#include <Servo.h>
#define servo_pin_1 9
#define servo_pin_2 10
#define pot_pin A0
// #define IR_sensor A1

Servo yawServo;
Servo pitchServo;
unsigned long previousMillis = 0;
float blinkInterval = 300;    // Updated live from the potentiometer
float val = 0;
float yawStart_val = 75;
float yawEnd_val = 130;
float pitchStart_val = 30;
float pitchEnd_val = 90;
float pitchAngle = 0;
float yawAngle = 0;
float readingVal = 0;
const double IR_sensor = A1; 

void readData(){
  readingVal = analogRead(IR_sensor); 
}

void sendData(float yawAngle= -1, float pitchAngle = -1, float readingVal = -1){
  // Sends data to serial port python
  Serial.print(readingVal); Serial.print(",");
  Serial.print(pitchAngle); Serial.print(",");
  Serial.println(yawAngle);
}

void moveYawServo(float yawAngle){
  // Yaw is also commonly understood as Pan
  // Moves servo to angle location
  yawServo.write(yawAngle);
  // Serial.print("Yaw: ");
  // Serial.println(yawAngle);
  delay(100);
}

void movePitchServo(float pitchStart, float pitchEnd){
  // Pitch is also commonly understood as Tilt
  // Moves pitch from pitchStart to pitchEnd, stoppping at each 5 degrees
  for (float angle = pitchStart; angle < pitchEnd; angle = angle + 2)
  {
    pitchAngle = angle;
    pitchServo.write(angle);
    readData();
    sendData(yawAngle, pitchAngle, readingVal);
    // Serial.print("Pitch: ");
    // Serial.println(angle);
    delay(100);
  }
}

void controlByPot(){
  // Manual control for the Servo, great for manual debugging
  val = analogRead(pot_pin);
  val = map(val, 0, 1023, 0, 180);
  moveYawServo(val);
  delay(1000);
  movePitchServo(pitchStart_val, pitchEnd_val);
}

void scanOnce(float yawStart, float yawEnd, float pitchStart, float pitchEnd){
  // Scans once, moving the Yaw servo a full 180 degrees, and then increments the Pitch servo
  // Yaw sweeps from 0 to 180, stopping each 5 degrees
  // Pitch servo is initially at 0, it will sweep to 180, stopping each 10 degrees
  for (float angle = yawStart; angle < yawEnd; angle = angle + 2)
  {
    yawAngle = angle;
    moveYawServo(angle);
    movePitchServo(pitchStart, pitchEnd); 
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
  pinMode(pot_pin, INPUT_PULLUP);
  // pinMode(IR_sensor, INPUT_PULLUP);

  // set both servo to default positions
  //yawServo.write(0);
  //pitchServo.write(0);
  while (!Serial);
  Serial.println("Ready");
  delay(2000);
  //controlByPot();
  kill();
  scanOnce(yawStart_val, yawEnd_val, pitchStart_val, pitchEnd_val);
  Serial.println("Done");
}

void loop() {
  // Code that loops
}