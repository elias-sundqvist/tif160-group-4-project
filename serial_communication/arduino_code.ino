/*

    Serial communication code for Arduino Uno.
    Need to add the pos_min & pos_max to the move functions

*/
#include <Arduino.h>
#include <Servo.h>
#include <TimedAction.h>

#define INPUT_SIZE 69 // The size of char's from Pi
// Servo ID's
#define body_id 0
#define neck_pan_id 1
#define neck_tilt_id 2
#define shoulder_id 3
#define elbow_id 4
#define grip_id 5
#define ready_id 6
#define THRESHOLD 10

//Servos
Servo body;
Servo headPan;
Servo headTilt;
Servo shoulder;
Servo elbow;
Servo gripper;

char input[INPUT_SIZE + 1];
bool READY = false;

//Init position of all servos
const int servo_pins[] = {3, 5, 6, 9, 10, 11};

//body:0 pan:1 tilt:2 shoulder:3 elbow:4 gripper:5
const int pos_init[] = {1425, 1425, 1870, 1275, 1400, 1700};
const int pos_min[] = {560, 550, 950, 750, 550, 550};
const int pos_max[] = {2330, 2340, 2400, 2200, 2400, 2150};

int curr_pos[6];
int new_servo_val[6];

void sendServoData(){  
    // Might change this to not send a string
    String data = String(neck_tilt_id)+':'+String(curr_pos[neck_tilt_id])+'&'+
                  String(neck_pan_id)+':'+String(curr_pos[neck_pan_id])+'&'+
                  String(shoulder_id)+':'+String(curr_pos[shoulder_id])+'&'+
                  String(elbow_id)+':'+String(curr_pos[elbow_id])+'&'+
                  String(body_id)+':'+String(curr_pos[body_id])+'&'+
                  String(grip_id)+':'+String(curr_pos[grip_id])+'&'+
                  String(ready_id)+':'+String(READY);
    
    Serial.println(data);
}

//Create a couple timers that will fire repeatedly every x ms
TimedAction writeThread = TimedAction(1,sendServoData);

//Servo update function
void servo_body_ex(const int new_pos) {

  int diff, steps, now, CurrPwm, NewPwm, delta = 10;

  //current servo value
  now = curr_pos[body_id];
  CurrPwm = now;
  NewPwm = new_pos;

  /* determine interation "diff" from old to new position */
  diff = (NewPwm - CurrPwm)/abs(NewPwm - CurrPwm); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
  steps = abs(NewPwm - CurrPwm);
  delay(10);

  for (int i = 0; i < steps; i += delta) {
    now = now + delta*diff;
    if(now > pos_max[body_id]){
      now = pos_max[body_id];
    }
    else if(now < pos_min[body_id]){
      now = pos_min[body_id];
    }
    body.writeMicroseconds(now);
    curr_pos[body_id] = now;
    if(i%20==0){writeThread.check();}
    delay(20);
  }
  if(new_pos <= pos_max[body_id] && new_pos >= pos_min[body_id]){
    curr_pos[body_id] = new_pos;
    body.writeMicroseconds(new_pos);
  }
  
  delay(10);
}

//Servo update function
void servo_neck_pan(const int new_pos) {

  int diff, steps, now, CurrPwm, NewPwm, delta = 10;

  //current servo value
  now = curr_pos[neck_pan_id];
  CurrPwm = now;
  NewPwm = new_pos;

  /* determine interation "diff" from old to new position */
  diff = (NewPwm - CurrPwm)/abs(NewPwm - CurrPwm); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
  steps = abs(NewPwm - CurrPwm);
  delay(10);

  for (int i = 0; i < steps; i += delta) {
    now = now + delta*diff;
    if(now > pos_max[neck_pan_id]){
      now = pos_max[neck_pan_id];
    }
    else if(now < pos_min[neck_pan_id]){
      now = pos_min[neck_pan_id];
    }
    headPan.writeMicroseconds(now);
    curr_pos[neck_pan_id] = now;
    if(i%20==0){writeThread.check();}
    delay(20);
  }
  if(new_pos <= pos_max[neck_pan_id] && new_pos >= pos_min[neck_pan_id]){
    curr_pos[neck_pan_id] = new_pos;
    headPan.writeMicroseconds(new_pos);
  }
  
  delay(10);
}

//Servo update function
void servo_neck_tilt(const int new_pos) {

  int diff, steps, now, CurrPwm, NewPwm, delta = 10;

  //current servo value
  now = curr_pos[neck_tilt_id];
  CurrPwm = now;
  NewPwm = new_pos;

  /* determine interation "diff" from old to new position */
  diff = (NewPwm - CurrPwm)/abs(NewPwm - CurrPwm); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
  steps = abs(NewPwm - CurrPwm);
  delay(10);

  for (int i = 0; i < steps; i += delta) {
    now = now + delta*diff;
    if(now > pos_max[neck_tilt_id]){
      now = pos_max[neck_tilt_id];
    }
    else if(now < pos_min[neck_tilt_id]){
      now = pos_min[neck_tilt_id];
    }
    headTilt.writeMicroseconds(now);
    curr_pos[neck_tilt_id] = now;
    if(i%20==0){writeThread.check();}
    delay(20);
  }
  if(new_pos <= pos_max[neck_tilt_id] && new_pos >= pos_min[neck_tilt_id]){
    curr_pos[neck_tilt_id] = new_pos;
    headTilt.writeMicroseconds(new_pos);
  }
  
  delay(10);
}

//Servo update function
void servo_shoulder(const int new_pos) {

  int diff, steps, now, CurrPwm, NewPwm, delta = 10;

  //current servo value
  now = curr_pos[shoulder_id];
  CurrPwm = now;
  NewPwm = new_pos;

  /* determine interation "diff" from old to new position */
  diff = (NewPwm - CurrPwm)/abs(NewPwm - CurrPwm); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
  steps = abs(NewPwm - CurrPwm);
  delay(10);

  for (int i = 0; i < steps; i += delta) {
    now = now + delta*diff;
    if(now > pos_max[shoulder_id]){
      now = pos_max[shoulder_id];
    }
    else if(now < pos_min[shoulder_id]){
      now = pos_min[3];
    }
    shoulder.writeMicroseconds(now);
    curr_pos[shoulder_id] = now;
    if(i%20==0){writeThread.check();}
    delay(20);
  }
  if(new_pos <= pos_max[shoulder_id] && new_pos >= pos_min[shoulder_id]){
    curr_pos[shoulder_id] = new_pos;
    shoulder.writeMicroseconds(new_pos);
  }
  
  
  delay(10);
}

//Servo update function
void servo_elbow(const int new_pos) {

  int diff, steps, now, CurrPwm, NewPwm, delta = 10;

  //current servo value
  now = curr_pos[elbow_id];
  CurrPwm = now;
  NewPwm = new_pos;

  /* determine interation "diff" from old to new position */
  diff = (NewPwm - CurrPwm)/abs(NewPwm - CurrPwm); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
  steps = abs(NewPwm - CurrPwm);
  delay(10);

  for (int i = 0; i < steps; i += delta) {
    now = now + delta*diff;
    if(now > pos_max[elbow_id]){
      now = pos_max[elbow_id];
    }
    else if(now < pos_min[4]){
      now = pos_min[elbow_id];
    }
    elbow.writeMicroseconds(now);
    curr_pos[elbow_id] = now;
    if(i%20==0){writeThread.check();}
    delay(20);
  }
  if(new_pos <= pos_max[elbow_id] && new_pos >= pos_min[elbow_id]){
    curr_pos[elbow_id] = new_pos;
    elbow.writeMicroseconds(new_pos);
  }
  
  delay(10);
}

//Servo update function
void servo_gripper_ex(const int new_pos) {

  int diff, steps, now, CurrPwm, NewPwm, delta = 10;

  //current servo value
  now = curr_pos[grip_id];
  CurrPwm = now;
  NewPwm = new_pos;

  /* determine interation "diff" from old to new position */
  diff = (NewPwm - CurrPwm)/abs(NewPwm - CurrPwm); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
  steps = abs(NewPwm - CurrPwm);
  delay(10);

  for (int i = 0; i < steps; i += delta) {
    now = now + delta*diff;
    if(now > pos_max[grip_id]){
      now = pos_max[grip_id];
    }
    else if(now < pos_min[grip_id]){
      now = pos_min[grip_id];
    }
    gripper.writeMicroseconds(now);
    curr_pos[grip_id] = now;
    if(i%20==0){writeThread.check();}
    delay(20);
  }
  if(new_pos <= pos_max[grip_id] && new_pos >= pos_min[grip_id]){
    curr_pos[grip_id] = new_pos;
    gripper.writeMicroseconds(new_pos);
  }
  
  delay(10);
}

void setup() {
    Serial.begin(57600); // Starts the serial communication
    Serial.flush();
    
    //Attach each joint servo
    //and write each init position
    body.attach(servo_pins[body_id]);
    body.writeMicroseconds(pos_init[body_id]); 
    
    headPan.attach(servo_pins[neck_pan_id]);
    headPan.writeMicroseconds(pos_init[neck_pan_id]);
    
    headTilt.attach(servo_pins[neck_tilt_id]);
    headTilt.writeMicroseconds(pos_init[neck_tilt_id]);

    shoulder.attach(servo_pins[shoulder_id]);
    shoulder.writeMicroseconds(pos_init[shoulder_id]);

    elbow.attach(servo_pins[elbow_id]);
    elbow.writeMicroseconds(pos_init[elbow_id]);
    
    gripper.attach(servo_pins[grip_id]);
    gripper.writeMicroseconds(pos_init[grip_id]);

    //Initilize curr_pos and new_servo_val vectors
    byte i;
    for (i=0; i<(sizeof(pos_init)/sizeof(int)); i++){
      curr_pos[i] = pos_init[i];
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
      READY = false;
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
              if(abs(curr_pos[body_id] - position) > THRESHOLD){
                servo_body_ex((const int) position);  
              }
              break;
            case neck_pan_id:
              if(abs(curr_pos[neck_pan_id] - position) > THRESHOLD){
                servo_neck_pan((const int) position);  
              }
              break;
            case neck_tilt_id:
              if(abs(curr_pos[neck_tilt_id] - position) > THRESHOLD){
                servo_neck_tilt((const int) position);
              }
              break;
            case shoulder_id:
              if(abs(curr_pos[shoulder_id] - position) > THRESHOLD){
                servo_shoulder((const int) position);
              }
              break;
            case elbow_id:
              if(abs(curr_pos[elbow_id] - position) > THRESHOLD){
                servo_elbow((const int) position);
              }
              break;
            case grip_id:
              if(abs(curr_pos[grip_id] - position) > THRESHOLD){
                servo_gripper_ex((const int) position);
                Serial.println("Done");
              }
              break;
            default:
              break;
          }
        writeThread.check();
        // Find the next command in input string
        command = strtok(0, "&");
    }
    delay(100);

    // Serial.print("You sent me: ");  // Send it using utf-8 encoding
  }
  READY = true;
  writeThread.check();
}
