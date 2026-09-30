#include <Arduino.h>
#include <Servo.h>
#define servo_pin_1 9
#define servo_pin_2 11
#define pot_pin A0

Servo yawServo;
Servo pitchServo;
unsigned long previousMillis = 0;
float blinkInterval = 300;    // Updated live from the potentiometer
int val = 0;
int yawStart_val = 90;
int yawEnd_val = 180;
int pitchStart_val = 45;
int pitchEnd_val = 90;
int pitchAngle = 0;
int yawAngle = 0;
float readingVal = 0;
const double IR_sensor = A1; 

/** 
 * @brief reads sensor data
 */
void readData(){
  readingVal = analogRead(IR_sensor); 
}

/** 
 * @brief send the data over to the python files
 */
void sendData(int yawAngle= -1, int pitchAngle = -1, int readingVal = -1){
  // Sends data to serial port python
  Serial.print(readingVal); Serial.print(",");
  Serial.print(pitchAngle); Serial.print(",");
  Serial.println(yawAngle);
}

/** 
 * @brief Pitch is also commonly understood as Tilt
 * Moves pitch from pitchStart to pitchEnd, stoppping at each 2 degree
 * @param pitchStart integers representing the start of the pitch sweep
 * @param pitchEnd integers representing the ends of the pitch sweep
 */
void movePitchServo(int pitchStart, int pitchEnd){
  for (int angle = pitchStart; angle < pitchEnd; angle = angle + 2)
  {
    pitchAngle = angle;
    pitchServo.write(angle);
    readData();
    sendData(yawAngle, pitchAngle, readingVal);
    delay(100);
  }
}

/** 
 * @brief Moves servo to the angle. Yaw is understood as Pan.
 * @param angle an integer representing the angle to move to
 */
void moveYawServo(int angle){
  yawAngle = angle;
  yawServo.write(yawAngle);
  delay(250); 
}

/** 
 * @brief Scans over the object once sweeping across pitch and yaw values
 * it will use sweep over pitch fully then slowly increment yaws until the end
 * @param yawStart integers representing the start of the yaw sweep
 * @param yawEnd integers representing the ends of the yaw sweep
 * @param pitchStart integers representing the start of the pitch sweep
 * @param pitchEnd integers representing the ends of the pitch sweep
 */
void scanOnce(int yawStart, int yawEnd, int pitchStart, int pitchEnd) {
  for (int y = yawStart; y <= yawEnd; y += 4) {
    moveYawServo(y);
    
    for (int p = pitchStart; p <= pitchEnd; p += 2) {
      pitchAngle = p;
      pitchServo.write(pitchAngle);
      readData();
      sendData(yawAngle, pitchAngle, readingVal);
      
      delay(80); 
    }

    delay(80);
  }
}

/** 
 * @brief moves the motors to 0 degrees
 */
void kill(){
  // kill the motor
  yawServo.write(0);
  pitchServo.write(0);
}

/** 
 * @brief code that runs on startup, 
 */
void setup() {
  // Code that runs on startup
  Serial.begin(115200);
  yawServo.attach(9);
  pitchServo.attach(11);
  pinMode(pot_pin, INPUT_PULLUP);;

  while (!Serial);
  Serial.println("Ready");
  scanOnce(yawStart_val, yawEnd_val, pitchStart_val, pitchEnd_val);
  Serial.println("Done");
}

void loop() {
  // Code that loops
}