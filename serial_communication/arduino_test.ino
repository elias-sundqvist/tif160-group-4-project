/*

    Serial communication code for Arduino Uno.
    Need to add the pos_min & pos_max to the move functions

*/
#include <Arduino.h>
#include <Servo.h>
#include <TimedAction.h>

#define INPUT_SIZE 42 // The size of char's from Pi
// Servo ID's
#define body_id 0
#define neck_pan_id 1
#define neck_tilt_id 2
#define shoulder_id 3
#define elbow_id 4
#define grip_id 5

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

                      //body:0 pan:1 tilt:2 shoulder:3 elbow:4 gripper:5
const int pos_init[] = {1425, 1425, 1870, 2180, 1400, 1700};

int curr_pos[6];
int new_servo_val[6];

const int pos_min[] = {560, 550, 950, 750, 550, 550};
const int pos_max[] = {2330, 2340, 2400, 2200, 2400, 2150};

void sendServoData(){  
    // Might change this to not send a string
    String data = String(neck_tilt_id)+':'+String(curr_pos[neck_tilt_id])+'&'+
                  String(neck_pan_id)+':'+String(curr_pos[neck_pan_id])+'&'+
                  String(shoulder_id)+':'+String(curr_pos[shoulder_id])+'&'+
                  String(elbow_id)+':'+String(curr_pos[elbow_id])+'&'+
                  String(body_id)+':'+String(curr_pos[body_id])+'&'+
                  String(grip_id)+':'+String(curr_pos[grip_id]);
    
    Serial.println(data);
}

//Create a couple timers that will fire repeatedly every x ms
TimedAction writeThread = TimedAction(1,sendServoData);

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
    if(now > pos_max[0]){
      now = pos_max[0];
    }
    else if(now < pos_min[0]){
      now = pos_min[0];
    }
    body.writeMicroseconds(now);
    curr_pos[0] = now;
    writeThread.check();
    delay(20);
  }
  
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
    if(now > pos_max[1]){
      now = pos_max[1];
    }
    else if(now < pos_min[1]){
      now = pos_min[1];
    }
    headPan.writeMicroseconds(now);
    curr_pos[1] = now;
    writeThread.check();
    delay(20);
  }
  
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
    if(now > pos_max[2]){
      now = pos_max[2];
    }
    else if(now < pos_min[2]){
      now = pos_min[2];
    }
    headTilt.writeMicroseconds(now);
    curr_pos[2] = now;
    writeThread.check();
    delay(20);
  }
  
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
    if(now > pos_max[3]){
      now = pos_max[3];
    }
    else if(now < pos_min[3]){
      now = pos_min[3];
    }
    shoulder.writeMicroseconds(now);
    curr_pos[3] = now;
    writeThread.check();
    delay(20);
  }
  
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
    if(now > pos_max[4]){
      now = pos_max[4];
    }
    else if(now < pos_min[4]){
      now = pos_min[4];
    }
    elbow.writeMicroseconds(now);
    curr_pos[4] = now;
    writeThread.check();
    delay(20);
  }
  
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
    if(now > pos_max[5]){
      now = pos_max[5];
    }
    else if(now < pos_min[5]){
      now = pos_min[5];
    }
    gripper.writeMicroseconds(now);
    curr_pos[5] = now;
    writeThread.check();
    delay(20);
  }
  
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

void loop() {
  
  //check on our threads. based on how long the system has been
  //running, do they need to fire and do work? if so, do it!
  writeThread.check();
  //writeThread.enable();
  
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
            case body_id:
              servo_body_ex((const int) position);
              break;
            case neck_pan_id:
              servo_neck_pan((const int) position);
              break;
            case neck_tilt_id:
              servo_neck_tilt((const int) position);
              break;
            case shoulder_id:
              servo_shoulder((const int) position);
              break;
            case elbow_id:
              servo_elbow((const int) position);
              break;
            case grip_id:
              servo_gripper_ex((const int) position);
              break;
            default:
              break;
          }
        
        // Find the next command in input string
        command = strtok(0, "&");
    }
    delay(100);

    // Serial.print("You sent me: ");  // Send it using utf-8 encoding
  }
  
}