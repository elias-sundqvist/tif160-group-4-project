//  HB-25 Library Test
//
//  Version:  1.1
//  Date:     10th December 2015
//
//  Valid speed ranges for the forwardAtSpeed and reverseAtSpeed methods are
//  0 (stop) to 500 (maximum speed). For rampToSpeed and moveAtSpeed you can use from -500 (full
//  reverse) to 500 (full forward). As before, a speed of 0 will stop the motor.
//
//  Remember to call the begin() method in setup().
//
//  Adapted from a sketch by zoomkat 10-22-11 serial servo test


//  Valid speed ranges for the forwardAtSpeed and reverseAtSpeed methods are
//  0 (stop) to 500 (maximum speed). For rampToSpeed and moveAtSpeed you can use from -500 (full
//  reverse) to 500 (full forward). As before, a speed of 0 will stop the motor.
//
//  Remember to call the begin() method in setup().


#include <Servo.h>                    //You need to include Servo.h as it is used by the HB-25 Library
#include <HB25MotorControl.h>
#include <TimedAction.h>


#define INPUT_SIZE 24                 //The size of char's from Pi
char input[INPUT_SIZE + 1];

#define leftWheel_id 7
#define rightWheel_id 8
#define timeStamp_id 9
#define ready_id 10

int curr_speedL;
int curr_speedR;
int new_speedL;
int new_speedR;
int curr_time = 0;
bool READY = true;

int leftSpeed, rightSpeed;

const int speed_min = -500;
const int speed_max = 500;

HB25MotorControl motorControlL(2);
HB25MotorControl motorControlR(3);


void sendServoData(){  
    // Might change this to not send a string
    String data = String(leftWheel_id)+':'+String(curr_speedL)+'&'+
                  String(rightWheel_id)+':'+String(curr_speedR)+'&'+
                  String(timeStamp_id)+':'+String(curr_time)+'&'+
                  String(ready_id)+':'+String(READY);
    
    Serial.println(data);
}


//Create a couple timers that will fire repeatedly every x ms
TimedAction writeThread = TimedAction(1,sendServoData);


//Servo update function
void servo_speed(const int new_speedL, const int new_speedR) {
  
  int diffL, stepsL, nowL, CurrValL, NewValL, delta = 6,
      diffR, stepsR, nowR, CurrValR, NewValR, steps; 
  
  nowL = curr_speedL;
  nowR = curr_speedR;
  CurrValL = nowL;
  CurrValR = nowR;
  NewValL = new_speedL;
  NewValR = new_speedR;
  
  // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
  diffL = (NewValL - CurrValL)/abs(NewValL - CurrValL); 
  diffR = (NewValR - CurrValR)/abs(NewValR - CurrValR);
  stepsL = abs(NewValL - CurrValL);
  stepsR = abs(NewValR - CurrValR);
  delay(10);

  steps = (stepsL>=stepsR) * stepsL + (stepsR>stepsL) * stepsR;
  
  for (int i = 0; i < steps+1; i += delta) {
    
    nowL += (i<=stepsL) * delta*diffL;
    nowR += (i<=stepsR) * delta*diffR;

    nowL = (nowL<speed_max) ? nowL : speed_max;
    nowR = (nowR<speed_max) ? nowR : speed_max;
    
    nowL = (nowL>speed_min) ? nowL : speed_min;
    nowR = (nowR>speed_min) ? nowR : speed_min;
    
    nowL = (abs(new_speedL-nowL)<=delta) ? new_speedL : nowL;
    nowR = (abs(new_speedR-nowR)<=delta) ? new_speedR : nowR;
    
    motorControlL.moveAtSpeed(nowL);
    motorControlR.moveAtSpeed(nowR);

    curr_speedL = nowL;
    curr_speedR = nowR;
    
    writeThread.check();
    delay(20);
  }

  if(new_speedL==curr_speedL && new_speedR==curr_speedR && curr_time>0) {
      int t = curr_time;
      for(int i = 0; i < t; i++){
          motorControlL.moveAtSpeed(curr_speedL);
          motorControlR.moveAtSpeed(curr_speedR);
          
          curr_time += -1;
          curr_time = (curr_time>0) * curr_time;
          
          writeThread.check();
          delay(50);
      }
  }
}


void setup() {
  Serial.begin(57600); // Starts the serial communication

    motorControlL.begin();
    motorControlL.moveAtSpeed(0);
    
    motorControlR.begin();
    motorControlR.moveAtSpeed(0);

    //Initilize curr_pos and new_servo_val vectors
    curr_speedL = 0;
    curr_speedR = 0;
    new_speedL = curr_speedL;
    new_speedR = curr_speedR;

    delay(2000);
}


void loop() {

  byte size = Serial.readBytes(input, INPUT_SIZE);  //Might need a buffer if the Pi just spam the Arduino with commands
  input[size] = 0;                                  //Add the final 0 to end the C string
  
  
  char* command = strtok(input, "&");
  while(command!=0){
      READY = false;
      int id = atoi(command);
      int val = atoi(strchr(command, ':')+1);

      leftSpeed  = (id==leftWheel_id)  ? val : leftSpeed;
      rightSpeed = (id==rightWheel_id) ? val : rightSpeed;
      curr_time  = (id==timeStamp_id)  ? val : curr_time;
      
      command = strtok(0, "&");
  }

  leftSpeed  = (curr_time>0) * leftSpeed;
  rightSpeed = (curr_time>0) * rightSpeed;
  
  servo_speed((const int) leftSpeed, (const int) rightSpeed);
  if(leftSpeed == 0 && rightSpeed == 0){ READY = true; }
}
