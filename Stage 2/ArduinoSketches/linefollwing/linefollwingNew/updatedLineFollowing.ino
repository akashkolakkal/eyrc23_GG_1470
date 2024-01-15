 Motor pin connections
#define in1 16
#define in2 4
#define in3 2
#define in4 15

 IR pin connections
#define irPinLeft 17    Left IR sensor for center line, connected to TX2 (GPIO17)
#define irPinRight 1   Right IR sensor for center line, connected to TX0 (GPIO1)
#define irPinLeftSide 3   Left IR sensor for side lines, connected to RX0 (GPIO3)
#define irPinRightSide 5   Right IR sensor for side lines, connected to RX2 (GPIO16)

 LED and Buzzer pin connections
#define ledPin 13    Red LED, connected to GPIO13
#define buzzerPin 12   Buzzer, connected to GPIO12

 Node configurations
#define startNode 0
#define nodeA 1
#define nodeB 2
#define nodeC 3
#define nodeD 4
#define nodeE 5
#define nodeF 6
#define nodeG 7
#define nodeH 8
#define nodeI 9
#define endNode 10

int currentNode = startNode;  Starting 
int irRightSide;
int irRight;

int i = 0;
char steps[] = {'F', 'F', 'R', 'L', 'R', 'R', 'R', 'F', 'R', 'F', 'L', 'F'};

void setup() {
   Motor pins as output
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

   Sensor pins as input
  pinMode(irPinLeft, INPUT);
  pinMode(irPinRight, INPUT);
  pinMode(irPinLeftSide, INPUT);
  pinMode(irPinRightSide, INPUT);

   LED and Buzzer pins as output
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

   Keeping all motors off initially
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);

   Initially, turn on the LED
  digitalWrite(ledPin, HIGH);
   Turn off the buzzer
  digitalWrite(buzzerPin, LOW);


}


void loop() {
   Read the values of the IR sensors
  int irLeft = digitalRead(irPinLeft);
  int irRight = digitalRead(irPinRight);
  int irLeftSide = digitalRead(irPinLeftSide);
  int irRightSide = digitalRead(irPinRightSide);

   Perform line following based on IR sensor readings
   if ((irLeft == LOW && irRight == HIGH)  (irLeftSide == HIGH && irRightSide == LOW)) {

  if (irLeft == HIGH && irRight == HIGH && (irLeftSide== HIGH  irRightSide == HIGH) ) nodeDetected();

  else if (irLeft == HIGH && irRight == LOW) moveLeft();
  else if (irLeft == LOW && irRight == HIGH) moveRight();

  else if (irLeftSide == HIGH && irRightSide == LOW) moveRight();
  else if (irLeftSide == LOW && irRightSide == HIGH) moveLeft();
  
  else if (irLeft == LOW && irRight == LOW) moveForward();
}

void nodeDetected() {

  char step = steps[i];
  
  i++;

  switch (step) {
    case 'R'
      stopMoving();
      delay(1000);
      nintyRight();
      delay(525);
      break;
    case 'L'
      stopMoving();
      delay(1000);
      nintyLeft();
      delay(525);
      break;
    case 'F'
      stopMoving();
      delay(1000);
      forward();
      break;
    
  }
}

void turnLeft() {
  digitalWrite(in1, LOW);
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

void forward() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  delay(550);
}

void nintyLeft() {
  forward();
  stopMoving();
  delay(250);
  turnLeft();
}
void nintyRight() {
  forward();
  stopMoving();
  delay(250);
  turnRight();
} 
 Function to move left
void moveLeft() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

 Function to move right
void moveRight() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

 Function to move forward
void moveForward() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

 Function to stop
void stopMoving() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}


 Function to activate the buzzer
void activateBuzzer() {
  digitalWrite(buzzerPin, HIGH);
}

 Function to deactivate the buzzer
void deactivateBuzzer() {
  digitalWrite(buzzerPin, LOW);
}