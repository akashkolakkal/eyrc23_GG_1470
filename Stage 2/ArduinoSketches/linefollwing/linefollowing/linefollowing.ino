// Motor pin connections
#define in1 16
#define in2 4
#define in3 2
#define in4 15

// IR pin connections
#define irPinLeft 1    // Left IR sensor, connected to TX0 (GPIO1)
#define irPinRight 17  // Right IR sensor, connected to TX2 (GPIO17)

void setup() {
  // Motor pins as output
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  // Sensor pins as input
  pinMode(irPinLeft, INPUT);
  pinMode(irPinRight, INPUT);

  // Keeping all motors off initially
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

void loop() {
  // Read the values of the IR sensors
  int irLeft = digitalRead(irPinLeft);
  int irRight = digitalRead(irPinRight);

  if (irLeft == LOW && irRight == HIGH) {
    // Turn left
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
  } else if (irLeft == HIGH && irRight == LOW) {
    // Turn right
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
  } else if (irLeft == LOW && irRight == LOW) {
    // Move forward
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
  } else {
    // Stop
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
  }
}
