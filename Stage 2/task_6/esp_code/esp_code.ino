/*
▪ * Team Id: 1470
▪ * Author List: Akash Kolakkal, Parth Jain, Anikesh Kulal, Keshav Jha 
▪ * Filename: task6.ino
▪ * Theme: GeoGuide
▪ * Functions: setup(), loop(), nodeDetected(), eventReached(), takeTurn(), moveLeft(), moveRight(), moveForward(), stopMoving(), turnLeft(), turnRight(), activateBuzzer(), deactivateBuzzer(), activateLED(), deactivateLED(), reachedEnd()
▪ * Global Variables: in1, in2, in3, in4, irPinLeft, irPinRight, irPinLeftSide, irPinRightSide, ledPin, buzzerPin, ssid, password, port, host, recieved, didReachEvent, client, i, steps, connected
▪ */

#include <WiFi.h>

// defining the pins for the motors, IR sensors, LED and Buzzer
#define in1 16
#define in2 4
#define in3 2
#define in4 22

#define irPinLeft 21
#define irPinRight 18      
#define irPinLeftSide 19   
#define irPinRightSide 5  

#define ledPin 12
#define buzzerPin 14

// defining the WiFi credentials and the server details
const char* ssid = "Samsung M13 5G";    
const char* password =  "123456789";    
const uint16_t port = 8002;
const char * host = "192.168.60.163";
bool recieved = false;
bool didReachEvent = false;

WiFiClient client;

int i = 0;

String steps = "";
bool connected = false;

/*
 * Function Name: setup
 * Input: None 
 * Output: None
 * Logic: This function is called once at the start of the program. It sets up the pins for the motors, IR sensors, LED and Buzzer. It also connects to the WiFi and the server.
 * Example Call: called on its own
 */
void setup() {
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  Serial.begin(9600);

  WiFi.begin(ssid, password);
  // Wait for connection to be established before moving forward
  while (!connected) {
    if (WiFi.status() == WL_CONNECTED) {
      Serial.println("Connected to WiFi");
      if (client.connect(host, port)) {
        Serial.println("Connected to server");
        connected = true;
      } else {
        Serial.println("Connection to host failed");
        delay(1000);
      }
    } else {
      Serial.println("Connecting to WiFi...");
      delay(1000);
    }
  }


  pinMode(irPinLeft, INPUT);
  pinMode(irPinRight, INPUT);
  pinMode(irPinLeftSide, INPUT);
  pinMode(irPinRightSide, INPUT);

  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

}

/*
 * Function Name: loop
 * Input: None 
 * Output: None
 * Logic: This function is called repeatedly. It checks for instructions from the server and then moves the bot accordingly. It also checks for the IR sensors and takes the appropriate action.
 * Example Call: called on its own
 */
void loop() {

  // If instructions are not recieved, keep checking for instructions, and only move on when instructions are recieved
  if (!recieved) {
    String msg = client.readStringUntil('\n');
    Serial.println("Received from server: " + msg);

    // If the message is of the form "FFRL...", then the instructions are recieved
    if (msg.length() >= 3) {
      for (int i = 1; i < msg.length(); i++) {
        steps += msg[i]; 
      }
      recieved = true;
      Serial.println("Instructions Recieved!");
      delay(5000);
    }
    Serial.println("Trying..");
  } else {
    
    // If instructions are recieved, start moving the bot based on the instructions

    // Keep checking for instructions from the server, so that the bot can be stopped when it reaches the event
      if (client.available()) {
      char firstChar = client.read();
        if (firstChar != '\n'){
          stopMoving();
          eventReached();
          } 
      }

    // Read the IR sensors
      int irLeft = digitalRead(irPinLeft);
      int irRight = digitalRead(irPinRight);
      int irLeftSide = digitalRead(irPinLeftSide);
      int irRightSide = digitalRead(irPinRightSide);

    // If both the IR sensors are HIGH, then a node is detected
      if (irLeft == HIGH && irRight == HIGH) {
        // To reduce the chance of miss-fire, check for the IR sensors again after a delay of 30ms
        delay(30);
        irLeft = digitalRead(irPinLeft);
        irRight = digitalRead(irPinRight);

        // If both the IR sensors are still HIGH, then a node is surely detected
        if (irLeft == HIGH && irRight == HIGH ) nodeDetected(irLeftSide, irLeft,  irRight, irRightSide);
      }

    // If the bot is not at a node, then keep moving the bot based on the IR sensors
      else if (irLeftSide == HIGH && irRightSide == LOW) turnRight();
      else if (irLeftSide == LOW && irRightSide == HIGH) turnLeft();
      else if (irLeft == HIGH && irRight == LOW) moveLeft();
      else if (irLeft == LOW && irRight == HIGH) moveRight();
      else moveForward();
  }
}

/*
 * Function Name: nodeDetected
 * Input: int irleftSide, int irleft, int irRight, int irRightSide
 * Output: None
 * Logic: This function is called when a node is detected. It takes the appropriate action based on the instructions recieved from the server.
 * Example Call: nodeDetected(0,0,0,0);
 */
void nodeDetected(int irleftSide, int irleft, int irRight, int irRightSide) {

  char step = steps[i];
  i++;
  float endTrackDuration = 1.5;
  float eventReachDuration = 2.5;

  unsigned long startTime = millis();
// Take the appropriate action based on the next instruction in the steps array
  switch (step) {
    case 'R':
      moveForward();
      delay(300);
      // set the motors to turn right for 450ms
      turnRight();
      delay(450);
      moveForward();
      break;
    
    case 'L':
      moveForward();
      delay(300);
        // set the motors to turn left for 450ms
      turnLeft();
      delay(450);
      moveForward();
      break;

    case 'F':
      moveForward();
      delay(150);
      break;

    case 'B':
    // set the motors to turn right for 900ms to take a U-turn
      turnRight();
      delay(900);
      break;

    case 'E':
    // this is the end sequence to track when the bot has reached the end of the run
    // For the edge case when the last event is A, the bot has to take a left turn and then move forward
      if (steps[i+1] == 'L') {
        turnLeft();
        delay(450);
        endTrackDuration = 1.0;
      }

      moveForward();
      delay(200);
      
      // keep moving the bot forward for 1.5 seconds
      while ((millis() - startTime) / 1000.0 < endTrackDuration) {
        int irLeft = digitalRead(irPinLeft);
        int irRight = digitalRead(irPinRight);

        if (irLeft == HIGH && irRight == LOW) moveLeft();
        else if (irLeft == LOW && irRight == HIGH) moveRight();
        else moveForward();
      }

      stopMoving();
      reachedEnd();
      delay(1000000);
      break;

    case 'S':
      moveForward();
      delay(225);
      break;
  }

}

/*
 * Function Name: eventReached
 * Input: None
 * Output: None
 * Logic: This function is called when an event is reached. It stops the bot, activates the buzzer and the LED and then waits for 1 second.
 * Example Call: eventReached();
 */
void eventReached() {
    // stop the bot, and activate the buzzer for 1 second
  stopMoving();
  activateBuzzer();
  delay(1000);
  nodeDetected(0,0,0,0);
}


/*
 * Function Name: moveLeft
 * Input: None
 * Output: None
 * Logic: This function is called when the bot is to move left. It sets the appropriate pins to move the bot left.
 * Example Call: moveLeft();
 */
void moveLeft() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

/*
 * Function Name: moveRight
 * Input: None
 * Output: None
 * Logic: This function is called when the bot is to move right. It sets the appropriate pins to move the bot right.
 * Example Call: moveRight();
 */
void moveRight() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

/*
 * Function Name: moveForward
 * Input: None
 * Output: None
 * Logic: This function is called when the bot is to move forward. It sets the appropriate pins to move the bot forward.
 * Example Call: moveForward();
 */
void moveForward() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

/*
 * Function Name: stopMoving
 * Input: None
 * Output: None
 * Logic: This function is called when the bot is to stop moving. It sets the appropriate pins to stop the bot.
 * Example Call: stopMoving();
 */

void stopMoving() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

/*
 * Function Name: turnLeft
 * Input: None
 * Output: None
 * Logic: This function is called when the bot is to turn left. It sets the appropriate pins to turn the bot left.
 * Example Call: turnLeft();
 */
void turnLeft() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

/*
 * Function Name: turnRight
 * Input: None
 * Output: None
 * Logic: This function is called when the bot is to turn right. It sets the appropriate pins to turn the bot right.
 * Example Call: turnRight();
 */

void turnRight() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}

/*
 * Function Name: activateBuzzer
 * Input: None
 * Output: None
 * Logic: This function is called when the buzzer is to be activated. It activates the buzzer for 1 second.
 * Example Call: activateBuzzer();
 */
void activateBuzzer() {
    // as we had damaged our buzzer, we had to use a passive buzzer that is triggered using this tone() function
    // we have already confirmed about this on https://discuss.e-yantra.org/ forum.
  tone(buzzerPin, 5300, 1000);
}

/*
 * Function Name: activateLED
 * Input: None
 * Output: None
 * Logic: This function is called when the LED is to be activated. It activates the LED.
 * Example Call: activateLED();
 */
void activateLED(){
  digitalWrite(ledPin, HIGH);
}

/*
 * Function Name: deactivateLED
 * Input: None
 * Output: None
 * Logic: This function is called when the LED is to be deactivated. It deactivates the LED.
 * Example Call: deactivateLED();
 */
void deactivateLED() {
  digitalWrite(ledPin, LOW);
}

/*
 * Function Name: reachedEnd
 * Input: None
 * Output: None
 * Logic: This function is called when the bot has reached the end of the track. It activates the LED and the buzzer and then waits for 5 seconds.
 * Example Call: reachedEnd();
 */
void reachedEnd(){
  digitalWrite(ledPin, HIGH);
  tone(buzzerPin, 5300, 5000);
  delay(5000);
  digitalWrite(ledPin, LOW);
}