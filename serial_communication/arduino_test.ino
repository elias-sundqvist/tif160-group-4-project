/*

    Serial communication code for Arduino Uno.

*/
#include <Arduino.h>
#include <Servo.h>
#include <Serial.h>

#define INPUT_SIZE 30 // The size of char's from Pi
// Servo ID's
#define body = 0
#define neck_pan = 1
#define neck_tilt = 2
#define shoulder = 3
#define elbow = 4
#define grip = 5

//Servos
Servo body;
Servo headPan;
Servo headTilt;
Servo shoulder;
Servo elbow;
Servo gripper;
char input[INPUT_SIZE + 1];

//Init position of all servos
const int servo_pins[] = {3, 5, 6, 9, 10, 11};

const int pos_init[] = {1700, 1500, 2000, 2200, 1650, 1600};
int curr_pos[6];
int new_servo_val[6];

const int pos_min[] = {560, 550, 950, 750, 550, 550};
const int pos_max[] = {2330, 2340, 2400, 2200, 2400, 2150};

const int pos_move[] = {2200, 1500, 2000, 1100, 2300, 1600};

//Servo update function
void servo_body_ex(const int new_pos) {

  int diff, steps, now, CurrPwm, NewPwm, delta = 6;

  //current servo value
  now = curr_pos[0];
  CurrPwm = now;
  NewPwm = new_pos;

  /* determine interation "diff" from old to new position */
  diff = (NewPwm - CurrPwm)/abs(NewPwm - CurrPwm); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
  steps = abs(NewPwm - CurrPwm);
  delay(10);

  for (int i = 0; i < steps; i += delta) {
    now = now + delta*diff;
    body.writeMicroseconds(now);
    delay(20);
  }
  curr_pos[0] = now;
  delay(10);
}

//Servo update function
void servo_neck_pan(const int new_pos) {

  int diff, steps, now, CurrPwm, NewPwm, delta = 6;

  //current servo value
  now = curr_pos[1];
  CurrPwm = now;
  NewPwm = new_pos;

  /* determine interation "diff" from old to new position */
  diff = (NewPwm - CurrPwm)/abs(NewPwm - CurrPwm); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
  steps = abs(NewPwm - CurrPwm);
  delay(10);

  for (int i = 0; i < steps; i += delta) {
    now = now + delta*diff;
    headPan.writeMicroseconds(now);
    delay(20);
  }
  curr_pos[1] = now;
  delay(10);
}

//Servo update function
void servo_neck_tilt(const int new_pos) {

  int diff, steps, now, CurrPwm, NewPwm, delta = 6;

  //current servo value
  now = curr_pos[2];
  CurrPwm = now;
  NewPwm = new_pos;

  /* determine interation "diff" from old to new position */
  diff = (NewPwm - CurrPwm)/abs(NewPwm - CurrPwm); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
  steps = abs(NewPwm - CurrPwm);
  delay(10);

  for (int i = 0; i < steps; i += delta) {
    now = now + delta*diff;
    headTilt.writeMicroseconds(now);
    delay(20);
  }
  curr_pos[2] = now;
  delay(10);
}

//Servo update function
void servo_shoulder(const int new_pos) {

  int diff, steps, now, CurrPwm, NewPwm, delta = 6;

  //current servo value
  now = curr_pos[3];
  CurrPwm = now;
  NewPwm = new_pos;

  /* determine interation "diff" from old to new position */
  diff = (NewPwm - CurrPwm)/abs(NewPwm - CurrPwm); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
  steps = abs(NewPwm - CurrPwm);
  delay(10);

  for (int i = 0; i < steps; i += delta) {
    now = now + delta*diff;
    shoulder.writeMicroseconds(now);
    delay(20);
  }
  curr_pos[3] = now;
  delay(10);
}

//Servo update function
void servo_elbow(const int new_pos) {

  int diff, steps, now, CurrPwm, NewPwm, delta = 6;

  //current servo value
  now = curr_pos[4];
  CurrPwm = now;
  NewPwm = new_pos;

  /* determine interation "diff" from old to new position */
  diff = (NewPwm - CurrPwm)/abs(NewPwm - CurrPwm); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
  steps = abs(NewPwm - CurrPwm);
  delay(10);

  for (int i = 0; i < steps; i += delta) {
    now = now + delta*diff;
    elbow.writeMicroseconds(now);
    delay(20);
  }
  curr_pos[4] = now;
  delay(10);
}

//Servo update function
void servo_gripper_ex(const int new_pos) {

  int diff, steps, now, CurrPwm, NewPwm, delta = 6;

  //current servo value
  now = curr_pos[5];
  CurrPwm = now;
  NewPwm = new_pos;

  /* determine interation "diff" from old to new position */
  diff = (NewPwm - CurrPwm)/abs(NewPwm - CurrPwm); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
  steps = abs(NewPwm - CurrPwm);
  delay(10);

  for (int i = 0; i < steps; i += delta) {
    now = now + delta*diff;
    gripper.writeMicroseconds(now);
    delay(20);
  }
  curr_pos[5] = now;
  delay(10);
}

void setup() {
    Serial.begin(57600); // Starts the serial communication
    
    //Attach each joint servo
    //and write each init position
    body.attach(servo_pins[0]);
    body.writeMicroseconds(pos_init[0]);
    
    headPan.attach(servo_pins[1]);
    headPan.writeMicroseconds(pos_init[1]);
    
    headTilt.attach(servo_pins[2]);
    headTilt.writeMicroseconds(pos_init[2]);

    shoulder.attach(servo_pins[3]);
    shoulder.writeMicroseconds(pos_init[3]);

    elbow.attach(servo_pins[4]);
    elbow.writeMicroseconds(pos_init[4]);
    
    gripper.attach(servo_pins[5]);
    gripper.writeMicroseconds(pos_init[5]);

    //Initilize curr_pos and new_servo_val vectors
    byte i;
    for (i=0; i<(sizeof(pos_init)/sizeof(int)); i++){
      curr_pos[i] = pos_init[i];
      new_servo_val[i] = curr_pos[i];
    }

    delay(2000);
}

void sendServoData(){  
    // Might change this to not send a string
    String data = neck_tilt+":"+curr_pos[neck_tilt]+'&'+
                  neck_pan+":"+curr_pos[neck_pan]+'&'+
                  shoulder+":"+curr_pos[shoulder]+'&'+
                  elbow+":"+curr_pos[elbow]+'&'+
                  body+":"+curr_pos[body]+'&'+
                  grip+":"+curr_pos[grip];
    
    Serial.println(data);
}

//Create a couple timers that will fire repeatedly every x ms
TimedAction readThread = TimedAction(100,sendServoData);

void loop() {
  if (Serial.available() > 0) {
    //check on our threads. based on how long the system has been
    //running, do they need to fire and do work? if so, do it!
    readThread.check();

    byte size = Serial.readBytes(input, INPUT_SIZE); //Might need a buffer if the Pi just spam the Arduino with commands
    // Add the final 0 to end the C string
    input[size] = 0;

    // Read each command pair 
    char* command = strtok(input, "&");
    while (command != 0){
        // Split the command in two values
        char* separator = strchr(command, ':');
        if (separator != 0){
            // Actually split the string in 2: replace ':' with 0
            *separator = 0;
            int servoId = atoi(command);
            ++separator;
            int position = atoi(separator);
            // Do something with servoId and position
            switch (servoId){
              case body:
                servo_body_ex((const int) position);
                break;
              case neck_pan:
                servo_neck_pan((const int) position);
                break;
              case neck_tilt:
                servo_neck_tilt((const int) position);
                break;
              case shoulder:
                servo_shoulder((const int) position);
                break;
              case elbow:
                servo_elbow((const int) position);
                break;
              case grip:
                servo_gripper_ex((const int) position);
                break;
              default:
                break;
            }
        }
        // Find the next command in input string
        command = strtok(0, "&");
    }

    // Serial.print("You sent me: ");  // Send it using utf-8 encoding
  }
}