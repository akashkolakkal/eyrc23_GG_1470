#include <WiFi.h>

// WiFi credentials
const char* ssid = "Kolakkal's";                    //Enter your wifi hotspot ssid
const char* password =  "01149869";               //Enter your wifi hotspot password
const uint16_t port = 8002;
const char * host = "192.168.1.3";                 //Enter the ip address of your laptop after connecting it to wifi hotspot

char incomingPacket[80];
WiFiClient client;

String msg = "0";

//Motor pin connections
#define in1 16
#define in2 4
#define in3 2
#define in4 15
//ir pin connection
// #define irPin 17

void setup() {

  Serial.begin(115200);                          //Serial to print data on Serial Monitor

  //Motor pins as output
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  
  //Keeping all motors off initially
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);

  //Connecting to wifi
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }
 
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());

}

void loop() {
  Serial.print("Client connected: ");
  Serial.println(client.connected());

  if (!client.connected()) {
    if (!client.connect(host, port)) {
      Serial.println("Connection to host failed. Retrying...");
      delay(1000); // Wait for a second before retrying
      return;
    }
  }

  msg = client.readStringUntil('\n');
  client.print("ESP32 got input from Python");

  if(msg == "1"){
    forward();
  }
  else if(msg == "2"){
    backward();
  }
  else if(msg == "3"){
    leftward();
  }
  else if(msg == "4"){
    rightward();
  }
  else if(msg == "5"){
    stop();
  }
  else {
    client.print("Invalid");
  }
}

void forward()
{
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

void backward()
{
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}

void leftward()
{
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

void rightward()
{
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}

void stop()
{
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}