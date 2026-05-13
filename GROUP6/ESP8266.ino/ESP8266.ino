#include <ButtonDebounce.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "LedMatrix.h"
#define NUMBER_OF_DEVICES 1
#define CS_PIN D4
#define red_light_pin D0
#define green_light_pin D8
#define blue_light_pin D3
#define TRIG D2

LedMatrix ledMatrix = LedMatrix(NUMBER_OF_DEVICES, CS_PIN);
WiFiClient espClient;
PubSubClient client(espClient);
ButtonDebounce trigger(TRIG, 200);

const char *ssid = "icw502g";
const char *password = "8c122ase";
const char *mqtt_server = "ia.ic.polyu.edu.hk";
const char *mqttTopic_RX = "iot/sensor-B06";

int Mode = 0;
boolean keypress = true;
String ipAddress, macAddr;
int receivedLight = 0;
int receivedSound = 0;
const int LIGHT_THRESHOLD = 40;
const int SOUND_THRESHOLD = 50;
bool mqttDataReady = false;

static String scrollText = "";
static int pixelOffset = 0;
static unsigned long lastScrollTime = 0;
const unsigned long scrollInterval = 100;

void setup_wifi();
void callback(char* topic, byte* payload, unsigned int length);
void reconnect();
void buttonChanged(int state);

const char *deviceID = "B06";

void setup_wifi() {
  WiFi.disconnect();
  delay(100);
  Serial.print("\nConnecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    digitalWrite(green_light_pin, digitalRead(green_light_pin) ^ 1);
    if (millis() - start > 30000) {
      Serial.println("\nWiFi timeout, restarting...");
      ESP.restart();
    }
  }
  Serial.println("\nWiFi connected");
  Serial.print("IP: "); Serial.println(WiFi.localIP());
  Serial.print("MAC: "); Serial.println(WiFi.macAddress());
  ipAddress = WiFi.localIP().toString();
  macAddr = WiFi.macAddress();
  digitalWrite(green_light_pin, LOW);  // Green ON
}

void callback(char* topic, byte* payload, unsigned int length) {
  digitalWrite(blue_light_pin, LOW);  
  delay(100);
  digitalWrite(blue_light_pin, HIGH);

  String recMsg = "";
  for (unsigned int i = 0; i < length; i++) {
    recMsg += (char)payload[i];
  }

  Serial.print("\n[MQTT] Received [");
  Serial.print(topic);
  Serial.print("]: ");
  Serial.println(recMsg);

  StaticJsonDocument<512> json;
  DeserializationError error = deserializeJson(json, recMsg);
  if (error) {
    Serial.print("JSON parse failed: ");
    Serial.println(error.c_str());
    return;
  }

  if (json.containsKey("light")) {
    receivedLight = json["light"].as<int>();
    Serial.print("Parsed light: ");
    Serial.println(receivedLight);
  }

  if (json.containsKey("snd")) {
    receivedSound = json["snd"].as<int>();
    Serial.print("Parsed sound: ");
    Serial.println(receivedSound);
  }

  mqttDataReady = true;
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("MQTT reconnecting...");
    if (client.connect(macAddr.c_str())) {
      Serial.println("connected");
      client.subscribe(mqttTopic_RX);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying...");
      delay(5000);
    }
  }
}

void buttonChanged(int state) {
  if (state == LOW && keypress) {
    Mode = (Mode + 1) % 3;
    keypress = false;
    Serial.print("Switched Mode: ");
    Serial.println(Mode);
  } else if (state == HIGH) {
    keypress = true;
  }
}

void setup() {
  pinMode(TRIG, INPUT_PULLUP);
  pinMode(red_light_pin, OUTPUT);
  pinMode(green_light_pin, OUTPUT);
  pinMode(blue_light_pin, OUTPUT);

  digitalWrite(red_light_pin, HIGH);
  digitalWrite(green_light_pin, HIGH);
  digitalWrite(blue_light_pin, HIGH);

  Serial.begin(115200);
  Serial.println("System Start!");

  ledMatrix.init();
  ledMatrix.setIntensity(8);
  ledMatrix.setTextAlignment(TEXT_ALIGN_LEFT);
  ledMatrix.setCharWidth(6);

  client.setCallback(callback);
  trigger.setCallback(buttonChanged);

  setup_wifi();
  client.setServer(mqtt_server, 1883);

  ledMatrix.setText("READY");
  ledMatrix.drawText();
  ledMatrix.commit();
}

void loop() {
  trigger.update();
  if (!client.connected()) reconnect();
  client.loop();

  static int lastMode = -1;

  if (Mode != lastMode) {
    digitalWrite(red_light_pin, HIGH);
    digitalWrite(green_light_pin, Mode == 0 || Mode == 1 ? LOW : HIGH);
    digitalWrite(blue_light_pin, HIGH);
    ledMatrix.clear();
    ledMatrix.commit();
    lastMode = Mode;
  }

  switch (Mode) {
    case 0: {
      if (!mqttDataReady) {
        digitalWrite(green_light_pin, HIGH);
        digitalWrite(red_light_pin, LOW);
        Serial.println("Waiting for MQTT...");
        ledMatrix.setText("NO DATA");
        ledMatrix.drawText();
        ledMatrix.commit();
        break;
      }

      bool lightAlarm = receivedLight > LIGHT_THRESHOLD;
      bool soundAlarm = receivedSound > SOUND_THRESHOLD;
      bool alarmNow = lightAlarm || soundAlarm;

      static unsigned long lastBlinkTime = 0;
      static bool ledState = false;

      if (alarmNow) {
        if (millis() - lastBlinkTime >= 200) {
          lastBlinkTime = millis();
          ledState = !ledState;
          digitalWrite(red_light_pin, ledState ? LOW : HIGH);
        }
        digitalWrite(green_light_pin, HIGH);
      } else {

        digitalWrite(red_light_pin, LOW);
        digitalWrite(green_light_pin, LOW);
      }

      scrollText = "L: " + String(receivedLight) + " S: " + String(receivedSound) + "   ";
      ledMatrix.setText(scrollText);

      if (millis() - lastScrollTime > scrollInterval) {
        lastScrollTime = millis();
        ledMatrix.drawSmoothText(pixelOffset);
        ledMatrix.commit();
        pixelOffset++;
        int totalWidth = scrollText.length() * 6;
        if (pixelOffset >= totalWidth) pixelOffset = 0;
      }
      break;
    }

    case 1: {
      digitalWrite(green_light_pin, LOW);
      digitalWrite(red_light_pin, HIGH);
      digitalWrite(blue_light_pin, HIGH);
      ledMatrix.setText(deviceID);
      ledMatrix.drawText();
      ledMatrix.commit();
      break;
    }

    case 2: {
      ledMatrix.setIntensity(2);
      digitalWrite(red_light_pin, HIGH);
      digitalWrite(green_light_pin, HIGH);
      digitalWrite(blue_light_pin, HIGH);
      ledMatrix.setText("ZZ");
      ledMatrix.drawText();
      ledMatrix.commit();
      delay(1000);
      break;
    }
  }

  delay(50);
}

