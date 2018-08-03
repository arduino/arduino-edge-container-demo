#include "arduino_secrets.h"

#include <MQTTClient.h>
#include <system.h>
#include <Servo.h>
#include <MQTT.h>
#include <MQTTClient.h>
#include <system.h>
#include <SPI.h>
#include <WiFiNINA.h>

///////please enter your sensitive data in the Secret tab/arduino_secrets.h
char ssid[] = SECRET_SSID;        // your network SSID (name)
char pass[] = SECRET_PASS;    // your network password (use for WPA, or use as key for WEP)
int status = WL_IDLE_STATUS;     // the Wifi radio's status
char ip_server[] = "192.168.12.1"; //ip of the Mqtt Broker
int port_server = 1883; //port of the Mqtt Broker
int led_pin = LED_BUILTIN;
int servo_pin = 9;
int button_pin = 2;
int button_state = LOW;// the current reading from the input pin
int old_button_state = LOW;   // the previous reading from the input pin
Servo servo;
WiFiClient net; // needed for connection with Mqtt
MQTTClient client;
char p_topic[] = "/arduino/button"; //topic where to publish messages
char s_topic[] = "/arduino/servo"; //topic where to subscribe

void setup() {
  pinMode(led_pin, OUTPUT);
  pinMode(button_pin, INPUT);
  servo.attach(servo_pin);
  servo.write(10); //bring servo in starting position
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  delay(1000); // wait for serial inizialization
  connectToWifi();
  connectToMqtt();
  
  //begin dovrebbe andare qui
  client.onMessage(messageReceived);
}

void loop() {
  status = WiFi.status(); // check if the wi-fi is still connected
  if(status == WL_DISCONNECTED) { // Access Point is down
    Serial.println("Communication with AP failed!");
    digitalWrite(led_pin, LOW); // turn the led off to let you know the connection is not working
    connectToWifi();
    connectToMqtt();
  }
  if(!client.connected()) { // check the connection between the client and Mqtt Broker
    Serial.println("Communication with Mqtt Broker failed!");
    connectToMqtt();
  }
  
  client.loop();
  
  button_state = digitalRead(button_pin); // check the state of the button

  if (!button_state && old_button_state) {
    client.publish(p_topic, "on"); // publish a message via Mqtt
    Serial.println("Button Pressed");
    // blink the led
    digitalWrite(led_pin, LOW);
    delay(30);
    digitalWrite(led_pin, HIGH);
    
    
  }
  old_button_state = button_state;
  delay(50);
}

void messageReceived(String &topic, String &payload) { //function called when a message is published
  Serial.println("incoming: " + topic + " - " + payload);
  if(topic==s_topic && payload == "on"){
    servo.write(170); // opens the door
    delay(1000);
    servo.write(10); // bring servo in the starting position
  }
}

void printWifiData() {
  // print your WiFi shield's IP address:
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  // print the received signal strength:
  Serial.print("Signal strength (RSSI): ");
  Serial.println(WiFi.RSSI());
}

void connectToWifi(){ //connects/reconnects to wifi
  Serial.print("Attempting to connect to WPA SSID: ");
  Serial.print(ssid);
  while (status != WL_CONNECTED) {
    Serial.print(".");
    WiFi.end(); //useful when the Access Point is not reachable
    status = WiFi.begin(ssid, pass);
    delay(10000); // wait 10 seconds for connection
  }
  Serial.println("\nYou're connected to the network");
  printWifiData();
  digitalWrite(led_pin, HIGH); // Light up the LED to let you know that is connected
}

void connectToMqtt(){
  Serial.print("Attempting to connect to Mqtt Broker");
  client.begin(ip_server, port_server, net);
  while (!client.connect("button")) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("\nYou're connected to Mqtt Broker");
  client.subscribe(s_topic);
}