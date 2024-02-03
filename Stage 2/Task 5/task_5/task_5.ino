#include <WiFi.h>

#define in1 16
#define in2 4
#define in3 2
#define in4 15

#define irPinLeft 21
#define irPinRight 18      
#define irPinLeftSide 19   
#define irPinRightSide 5  

#define ledPin 12
#define buzzerPin 14

const char* ssid = "Samsung M13 5G";                    //Enter your wifi hotspot ssid
const char* password =  "anikeshkulal@gmail.com";               //Enter your wifi hotspot password
const uint16_t port = 8002;
const char * host = "192.168.102.163";                 //Enter the ip address of your laptop after connecting it to wifi hotspot

WiFiClient client;


 
int i = 0;

// char steps[] = { 'S', 'F', 'R', 'L', 'R', 'R', 'F', 'R', 'F', 'L', 'E' };
String steps = "";

const int ledcChannel = 0;
const int freq = 5000;
const int resolution = 8;
// const int ledPin = 12;




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

    // Initialize LED control module
  ledcSetup(ledcChannel, freq, resolution);
  ledcAttachPin(ledPin, ledcChannel);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Connect to the server
  if (!client.connect(host, port)) {
    Serial.println("Connection to host failed");
    delay(1000);
    return;
  }
  Serial.println("Connected to server");

  while (steps.length()) {
    String msg = client.readStringUntil('\n');
    Serial.println("Received from server: " + msg);

    for (int i = 1; i < msg.length() - 1; i++) {
      steps += msg[i]; 
    }
    Serial.println("Instructions Recieved!");
  }




  pinMode(irPinLeft, INPUT);
  pinMode(irPinRight, INPUT);
  pinMode(irPinLeftSide, INPUT);
  pinMode(irPinRightSide, INPUT);

  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);


  roundStart();


}

void loop() {

  if (!client.connected()) {
    Serial.println("Disconnected from server");
    return;
  }

  while (client.available()) {
    String msg = client.readStringUntil('\n');
    Serial.println("Received from server: " + msg);
    eventReached();
  }

  int irLeft = digitalRead(irPinLeft);
  int irRight = digitalRead(irPinRight);
  int irLeftSide = digitalRead(irPinLeftSide);
  int irRightSide = digitalRead(irPinRightSide);
  if (irLeft == HIGH && irRight == HIGH) {
    delay(30);
    irLeft = digitalRead(irPinLeft);
    irRight = digitalRead(irPinRight);
    if (irLeft == HIGH && irRight == HIGH ) nodeDetected(irLeftSide, irLeft,  irRight, irRightSide);
  }

  else if (irLeft == HIGH && irRight == LOW) moveLeft();
  else if (irLeft == LOW && irRight == HIGH) moveRight();
  // else if ((irLeft == HIGH && irRight == LOW) || (irLeftSide == LOW && irRightSide == HIGH)) moveLeft();
  // else if ((irLeft == LOW && irRight == HIGH) || (irLeftSide == HIGH && irRightSide == LOW)) moveRight();
  else if (irLeftSide == HIGH && irRightSide == LOW) moveRight();
  else if (irLeftSide == LOW && irRightSide == HIGH) moveLeft();
  else moveForward();
}

void nodeDetected(int irleftSide, int irleft, int irRight, int irRightSide) {

  char step = steps[i];
  i++;
  float endTrackDuration = 1.5;


  unsigned long startTime = millis();

  switch (step) {
    case 'R':
      moveForward();
      delay(300);
      stopMoving();
      // delay(1000);
      turnRight();
      delay(450);
      // takeTurn("right");
      moveForward();
      break;
    
    case 'L':
      moveForward();
      delay(300);
      stopMoving();
      turnLeft();
      delay(450);
      // takeTurn("left");
      moveForward();
      break;

    case 'F':
      moveForward();
      delay(250);
      break;

    case 'B':
      turnRight();
      delay(900);
      break;

    case 'E':
      moveForward();
      delay(200);
      while ((millis() - startTime) / 1000.0 < endTrackDuration) {
        int irLeft = digitalRead(irPinLeft);
        int irRight = digitalRead(irPinRight);

        if (irLeft == HIGH && irRight == LOW) moveLeft();
        else if (irLeft == LOW && irRight == HIGH) moveRight();
        else moveForward();
      }
      // moveRight();
      // delay(300);
      // moveForward();
      // delay(900);
      stopMoving();
      reachedEnd();
      delay(1000000);
      break;

    case 'S':
      moveLeft();
      delay(100);
      moveForward();
      delay(225);
      break;
  }
}

void eventReached() {
  activateBuzzer();
  activateLED();
  stopMoving();
  delay(1000);
  deactivateLED();
  nodeDetected(0,0,0,0);
}

void takeTurn(char direction[]) {
  moveForward();
  delay(300);

  if (direction == "right") {
    turnRight();
    int ir = HIGH;
    delay(150);

    do {
      ir = digitalRead(irPinLeft);
      turnRight();
      if (ir == LOW) {
        delay(10);
        ir = digitalRead(irPinLeft);
        if (ir != LOW) {
          Serial.println("Detected!");
        }
      }
      }
    
    while( ir == HIGH);

  } else {
    turnLeft();
    int ir = HIGH;
    delay(150);

    do {
      ir = digitalRead(irPinRight);
      turnLeft();
      
      if (ir == LOW) {
        delay(10);
        ir = digitalRead(irPinRight);
        if (ir != LOW) {
          Serial.println("Detected!");
        }
      }
    }
    while(ir == HIGH);

}
}

// Motor orientations
void moveLeft() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}
void moveRight() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}
void moveForward() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}
void stopMoving() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}
void turnLeft() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}
void turnRight() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}

void activateBuzzer() {
  tone(buzzerPin, 5300, 1000);
}
void deactivateBuzzer() {
  digitalWrite(buzzerPin, LOW);
}
void activateLED(){
  digitalWrite(ledPin, HIGH);
}
void deactivateLED() {
  digitalWrite(ledPin, LOW);
}

void roundStart() {
  delay(2000);
  digitalWrite(ledPin, HIGH);
  activateBuzzer();
  delay(1000);
  digitalWrite(ledPin, LOW);
}
void reachedEnd(){
  digitalWrite(ledPin, HIGH);
  // digitalWrite(buzzerPin, HIGH);
  tone(buzzerPin, 5300, 5000);
  delay(5000);
  digitalWrite(ledPin, LOW);
  // digitalWrite(buzzerPin, LOW);
}


