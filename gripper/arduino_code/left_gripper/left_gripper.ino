#include <Servo.h>

int right_finger = 10;
int left_finger = 9; 

int left_fully_open = 40;
int right_fully_open = 20;

int left_fully_closed = 0;
int right_fully_closed = 60; 


Servo right_servo;
Servo left_servo;
 
 
void setup() {
  Serial.begin(9600);
  right_servo.attach(right_finger);
  left_servo.attach(left_finger); 
  pinMode(LED_BUILTIN, OUTPUT);
  
  delay(500);
  close_gripper();
  delay(500);

  //test_gripper();
}

void loop() {
  while (Serial.available() == 0){}
   char cmd = Serial.read();
   if (cmd == 'o')
   open_gripper();
   else if (cmd == 'c')
   close_gripper(); 
}

void open_gripper(void){
  right_servo.write(right_fully_open);
  left_servo.write(left_fully_open);
  //Serial.println("open gripper");
  digitalWrite(LED_BUILTIN, LOW);
}

void close_gripper(void){
  right_servo.write(right_fully_closed);
  left_servo.write(left_fully_closed);
  //Serial.println("close gripper");
  digitalWrite(LED_BUILTIN, HIGH);
} 

void test_gripper(void){
  
  for (int i=0; i<1000; i++){
    open_gripper();
    delay(5000);
    close_gripper();
    delay(5000);
  }
}
