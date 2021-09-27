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

#include <Servo.h>                      //  You need to include Servo.h as it is used by the HB-25 Library
#include <HB25MotorControl.h>


#define INPUT_SIZE 16 // The size of char's from Pi    (my guess 2*8)
char input[INPUT_SIZE + 1];

#define leftWheel_id 0
#define rightWheel_id 1
const byte controlPin = {2,3};              //  Pin Definition
const int speed_init[] = {0,0};

int curr_speed[2];
int new_speed[2];

const int speed_min[] = {-500, -500};
const int speed_max[] = {500, 500};

HB25MotorControl motorControlL(controlPin(leftWheel_id));
HB25MotorControl motorControlR(controlPin(rightWheel_id));


//Servo update function
void servo_speed(const int new_speed, const int id) {

  int diff, steps, now, CurrVal, NewVal, delta = 6;

  //current servo value
  now = curr_speed[id];
  CurrVal = now;
  NewVal = new_speed;

  /* determine interation "diff" from old to new position */
  diff = (NewVal - CurrVal)/abs(NewVal - CurrVal); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
  steps = abs(NewVal - CurrVal);
  delay(10);

  for (int i = 0; i < steps; i += delta) {
    now = now + delta*diff;
    if(now > speed_max[id]){
      now = speed_max[id];
    }
    else if(now < pos_min[id]){
      now = pos_min[id];
    }
    if(id==leftWheel_id{
      motorControlL.moveAtSpeed(speed_init[leftWheel_id]);
    }
    else if(id==rightWheel_id){
      motorControlR.moveAtSpeed(speed_init[rightWheel_id]);
    }
    curr_speed[id] = now;
    writeThread.check();
    delay(20);
  }
  
  delay(10);
}


void setup() {
  Serial.begin(57600); // Starts the serial communication
  //Serial.println("Motor Control Test");

    motorControlL.begin();
    motorControlL.moveAtSpeed(speed_init[leftWheel_id]);
    
    motorControlR.begin();
    motorControlR.moveAtSpeed(speed_init[rightWheel_id]);

    //Initilize curr_pos and new_servo_val vectors
    byte i;
    for (i=0; i<(sizeof(pos_init)/sizeof(int)); i++){
      curr_speed[i] = speed_init[i];
      new_speed[i] = curr_speed[i];
    }

    delay(2000);
  
  
}

void loop() {

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
          int wheelId = atoi(command);
          ++separator;
          int position = atoi(separator);
          // Do something with servoId and position
          switch (wheelId){
            case leftWheel_id:
              servo_speed((const int) position, (const int) leftWheel_id);
              break;
            case leftWheel_id:
              servo_speed((const int) position, (const int) rightWheel_id);
              break;
            default:
              break;
          }
        
        // Find the next command in input string
        command = strtok(0, "&");
    }
  }
}
