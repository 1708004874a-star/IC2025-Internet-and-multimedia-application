#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <M5StickCPlus2.h>
#include <DFRobot_DHT11.h>
#include "time.h"
#include<PubSubClient.h>

#define DHT_PIN 0
#define LED_PIN 26
#define BUZZER_PIN 2

const float TEMP_WARNING = 22.0;
const float TEMP_ALARM = 24.0;

const char *ssid = "icw502g";
const char *password = "8c122ase";
const char *mqtt_server = "ia.ic.polyu.edu.hk";

char *mqttTopic = "IC/TeamB06";


const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 8 * 3600;
const int daylightOffset_sec = 0;

DFRobot_DHT11 dht;
WiFiClient espClient;
PubSubClient client(espClient);
float temp, hum, ax, ay, az, gx, gy, gz;
byte reconnect_count = 0;
String ipAddress, macAddr;
char msg[100];
StaticJsonDocument<200> Jsondata;


//connect wifi
void setup_wifi() {
  WiFi.disconnect(); delay(100);
  Serial.printf("\nConnecting to %s\n", ssid);
  WiFi.begin(ssid, password);
  M5.Lcd.setCursor(0, 0); M5.Lcd.print("Connecting");
  unsigned long start = millis(); int dot = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print("."); M5.Lcd.print(".");
    if (++dot >= 6) { dot = 0; M5.Lcd.setCursor(0, 0); M5.Lcd.print("Connecting      "); }
    if (millis() - start > 30000) ESP.restart();
  }
  Serial.println("\nWiFi connected");
  ipAddress = WiFi.localIP().toString();
  macAddr = WiFi.macAddress();
  M5.Lcd.fillScreen(BLACK); M5.Lcd.setCursor(0, 0); M5.Lcd.print("WiFi connected!");
  delay(1000); M5.Lcd.fillScreen(BLACK);
}
//active check
bool detectMovement() {
  return (abs(ax) > 0.2 || abs(ay) > 0.2 || abs(az - 1) > 0.2);
}
//read IMU and display
void check_Accel() {
  bool moved = detectMovement();
  Jsondata["MOVED"] = moved ? "Yes" : "No";
  Serial.println(moved ? "The part is moved!!" : "No movement detected!!");
  Jsondata["TEMP"] = temp;
  Jsondata["HUM"] = hum;
  serializeJson(Jsondata, Serial);
  serializeJson(Jsondata, msg);
  client.publish(mqttTopic, msg);
  Serial.println();
}

void showTime() {
  struct tm t;
  if (!getLocalTime(&t)) {
    M5.Lcd.setCursor(0, 120); M5.Lcd.setTextColor(RED, BLACK); M5.Lcd.println("Time Error");
    return;
  }

  M5.Lcd.fillRect(0, 100, 160, 20, BLACK);
  M5.Lcd.setCursor(0, 100); M5.Lcd.setTextColor(WHITE, BLACK);
  M5.Lcd.printf("Date: %04d-%02d-%02d", t.tm_year + 1900, t.tm_mon + 1, t.tm_mday);

  M5.Lcd.fillRect(0, 120, 160, 20, BLACK);
  M5.Lcd.setCursor(0, 120);
  M5.Lcd.printf("Time: %02d:%02d:%02d", t.tm_hour, t.tm_min, t.tm_sec);
}
//battery display 
void drawBattery(int x, int y, float voltage) {
  int level = constrain((voltage - 3.4) * 10, 0, 4);
  M5.Lcd.drawRect(x, y, 26, 12, WHITE);
  M5.Lcd.fillRect(x + 26, y + 3, 2, 6, WHITE);
  M5.Lcd.fillRect(x + 1, y + 1, 24, 10, BLACK);
  for (int i = 0; i < level; i++)
    M5.Lcd.fillRect(x + 2 + i * 6, y + 2, 5, 8, (voltage < 3.6) ? RED : GREEN);
}
//initialization
void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT); digitalWrite(LED_PIN, LOW);
  pinMode(BUZZER_PIN, OUTPUT); digitalWrite(BUZZER_PIN, LOW);
  M5.begin(); M5.Imu.init();
  M5.Lcd.setRotation(3); M5.Lcd.fillScreen(BLACK);
  M5.Lcd.setTextSize(2);    //fixed word
  M5.Lcd.setCursor(0, 0); M5.Lcd.println("Tem    Hum");
  M5.Lcd.setCursor(0, 30); M5.Lcd.println("Accel X Y Z");
  M5.Lcd.setCursor(0, 60); M5.Lcd.println("Gyro  X Y Z");
  setup_wifi();
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  client.setServer(mqtt_server, 1883);
  Jsondata["DEVICE"] = "M5StickCPlus2";
}

void loop() {
  dht.read(DHT_PIN);
  hum = dht.humidity; temp = dht.temperature;
//display andalarm temp and hum
  if (temp == 255 || hum == 255) {
    M5.Lcd.setCursor(0, 15); M5.Lcd.setTextColor(RED, BLACK);
    M5.Lcd.print("Sensor Error   ");
  } else {
    M5.Lcd.setCursor(0, 15);
    M5.Lcd.setTextColor(WHITE, (temp > TEMP_ALARM) ? RED : (temp > TEMP_WARNING) ? YELLOW : GREEN);
    M5.Lcd.printf("Tem:%4.1fC", temp);

    M5.Lcd.setCursor(90, 15);
    M5.Lcd.setTextColor(WHITE, BLUE);
    M5.Lcd.printf("Hum:%4.1f%%", hum);
  }
//IMU read and display   acceleration
  if (M5.Imu.update()) {
    auto d = M5.Imu.getImuData();
    ax = d.accel.x; ay = d.accel.y; az = d.accel.z;
    gx = d.gyro.x; gy = d.gyro.y; gz = d.gyro.z;

    bool moved = detectMovement();
    uint16_t accelBg = moved ? RED : 0x4208;//when move the color is red
    M5.Lcd.fillRect(0, 45, 160, 20, accelBg);
    M5.Lcd.setCursor(0, 45);
    M5.Lcd.setTextColor(YELLOW, accelBg);
    M5.Lcd.printf("%5.2f %5.2f %5.2f G", ax, ay, az);

    M5.Lcd.fillRect(0, 75, 160, 20, 0x0010);
    M5.Lcd.setCursor(0, 75);
    M5.Lcd.setTextColor(CYAN, 0x0010);
    M5.Lcd.printf("%5.1f %5.1f %5.1f o/s", gx, gy, gz);

    check_Accel();
  }
//show time 
  showTime();
  drawBattery(110, 0, M5.Power.getBatteryVoltage() / 1000.0);

  if (temp > TEMP_ALARM) tone(BUZZER_PIN, 2000); else noTone(BUZZER_PIN);
  digitalWrite(LED_PIN, !digitalRead(LED_PIN));//LED flickering
  if (!client.connected()) reconnect();
  client.loop();
  delay(2000);//2 seconds times
} 