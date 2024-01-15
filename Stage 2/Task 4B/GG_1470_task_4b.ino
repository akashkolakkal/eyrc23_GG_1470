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

int i = 0;

char steps[] = { 'S', 'F', 'R', 'L', 'R', 'R', 'F', 'R', 'F', 'L', 'E' };


void setup() {
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  pinMode(irPinLeft, INPUT);
  pinMode(irPinRight, INPUT);
  pinMode(irPinLeftSide, INPUT);
  pinMode(irPinRightSide, INPUT);

  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  roundStart();
}

void loop() {
  int irLeft = digitalRead(irPinLeft);
  int irRight = digitalRead(irPinRight);
  int irLeftSide = digitalRead(irPinLeftSide);
  int irRightSide = digitalRead(irPinRightSide);

  //double check to tackle false alarms due to noise
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
  if (i != 10) {
    stopMoving();
    activateBuzzer();
    delay(1000);
    deactivateBuzzer();
  }

  unsigned long startTime = millis();

  switch (step) {
    case 'R':
      moveForward();
      delay(605);
      stopMoving();
      turnRight();
      delay(605);
      moveForward();
      break;
    
    case 'L':
      moveForward();
      delay(660);
      stopMoving();
      turnLeft();
      delay(710);
      moveForward();
      break;

    case 'F':
      moveForward();
      delay(225);
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
  digitalWrite(buzzerPin, HIGH);
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
  activateLED();
  activateBuzzer();
  delay(1000);
  deactivateLED();
  deactivateBuzzer();
}
void reachedEnd(){
  activateLED();
  activateBuzzer();
  delay(5000);
  deactivateLED();
  deactivateBuzzer();
}
