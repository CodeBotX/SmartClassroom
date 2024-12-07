#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>  // For HTTPS
#include <HTTPClient.h>
#include <SPI.h>
#include <MFRC522.h>
#include <ArduinoJson.h>
#include <time.h>  // For time functions


#define SS_PIN    5   // Chip Select pin
#define RST_PIN   22    // Reset pin
#define SCK_PIN   18
#define MOSI_PIN  23
#define MISO_PIN  19
#define HONR_PIN  4
#define LED_PIN   15

//----------------------------------------------------------------------------
// Replace with your network credentials


// const char* ssid = "Minhquan 2.4G";
// const char* password = "0889903888";

// const char* ssid = "tuananh";
// const char* password = "khanhlong";

// const char* ssid = "iPhone";
// const char* password = "14122009";


const char* ssid = "pnhmy";
const char* password = "hmyyyyyy";



// Replace with your server URL
const char* serverName = "https://smartclassroom.click/api/attendance/attendance/";

// // Your server's root CA certificate (shortened example, get it from your server)
// const char* rootCACertificate = \
//   "-----BEGIN CERTIFICATE-----\n" \
//   "MIIDrzCCApegAwIBAgIQDfetc...\n" \
//   "-----END CERTIFICATE-----";


//--------------------------------------------------------------------------------

String deviceID = "as7dchu8d";  // This acts as the device token

// NTP server details
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 25200;   // Set to 7 hours in seconds
const int daylightOffset_sec = 0;

// Use WiFiClientSecure for HTTPS
WiFiClientSecure client;


MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create an instance of the MFRC522 class

byte blockAddr = 2;  // Block 2
byte buffer[18];     // Buffer to hold read data
byte size = sizeof(buffer);


void setup() {
  Serial.begin(115200);
  SPI.begin(SCK_PIN, MISO_PIN, MOSI_PIN, SS_PIN);
  mfrc522.PCD_Init();

  // Set up Horn and LED pins as output
  pinMode(HONR_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  // Set the default state of the Horn pin and LED pin to LOW (0)
  digitalWrite(HONR_PIN, LOW);
  digitalWrite(LED_PIN, HIGH);

  // Connect to Wi-Fi
  connectToWiFi();


  // Initialize time with NTP
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  Serial.println("Time synchronized with NTP server");

  // // Set root CA for secure connection
  // client.setCACert(rootCACertificate);

  client.setInsecure();  // Disable SSL verification for testing purposes
}



void connectToWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}






String readRFIDCard() {
  MFRC522::MIFARE_Key key;
  for (byte i = 0; i < 6; i++) key.keyByte[i] = 0xFF;  // Default key

  if (mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, blockAddr, &key, &(mfrc522.uid)) != MFRC522::STATUS_OK) {
    Serial.println("Authentication failed for block 2.");
    return "";  // Authentication failed, return empty string
  }

  // Read block 2
  MFRC522::StatusCode status = mfrc522.MIFARE_Read(blockAddr, buffer, &size);
  if (status != MFRC522::STATUS_OK) {
    Serial.print("Read failed with status: ");
    Serial.println(mfrc522.GetStatusCodeName(status));
    return "";  // Read failed, return empty string
  } 

  // Convert the first 10 characters back to the ID
  String studentID = "";
  for (int i = 0; i < 10; i++) {
    if (buffer[i] == 0) {
      Serial.println("Encountered null byte in buffer.");
      break;  // Stop if we encounter a null byte
    }
    studentID += (char)buffer[i];  // Convert each byte to char and append
  }

  // Halt PICC and stop encryption on PCD
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();

  Serial.print("Read student ID: ");
  Serial.println(studentID);

  return studentID;  // Return the student ID
}





String getAttendanceTime() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    Serial.println("Failed to obtain time");
    return "TimeError";  // Return an error string if time sync fails
  }
  
  char timeStringBuff[50];  // Buffer to store time string
  strftime(timeStringBuff, sizeof(timeStringBuff), "%Y-%m-%dT%H:%M:%S", &timeinfo);
  return String(timeStringBuff);  // Return the formatted time
}





void postAttendanceData(String studentID, String deviceID) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Prepare JSON payload
    DynamicJsonDocument jsonDoc(256);
    jsonDoc["student_id"] = studentID;  
    // jsonDoc["student_id"] = "3581635896";  
    jsonDoc["device_id"] = deviceID;     

    String jsonData;
    serializeJson(jsonDoc, jsonData);
    Serial.println("Sending JSON data: " + jsonData);

    // Send HTTP POST request
    http.begin(client, serverName);

    // http.setTimeout(1000); 

    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonData);

    // Check the response
    if (httpResponseCode == 201) { //success response
      // String response = http.getString();
      // Serial.println("Attended Successfully");
      // Serial.println("Server Response: " + response);
      digitalWrite(HONR_PIN, HIGH);
      digitalWrite(LED_PIN, LOW);
      delay(100);  

        // Set Horn and LED pins back to default
      digitalWrite(HONR_PIN, LOW);
      digitalWrite(LED_PIN, HIGH);

      String response = http.getString();
      Serial.println("Attended Successfully");
      Serial.println("Server Response: " + response);


    } else if (httpResponseCode > 0) { //attend fail
      // String response = http.getString();
      // Serial.println("Fail to attend"); 
      // Serial.println("Server Response: " + response); 
      for (int i = 0; i < 2; i++) {
        digitalWrite(HONR_PIN, HIGH);
        digitalWrite(LED_PIN, LOW);
        delay(70);  

          // Set Horn and LED pins back to default
        digitalWrite(HONR_PIN, LOW);
        digitalWrite(LED_PIN, HIGH);

        delay(50);
      }

      String response = http.getString();
      Serial.println("Fail to attend"); 
      Serial.println("Server Response: " + response); 

    } else {
      // Serial.println("Error on sending POST: " + String(httpResponseCode));
      for (int i = 0; i < 3; i++) {
        digitalWrite(HONR_PIN, HIGH);
        digitalWrite(LED_PIN, LOW);
        delay(70);  

          // Set Horn and LED pins back to default
        digitalWrite(HONR_PIN, LOW);
        digitalWrite(LED_PIN, HIGH);

        delay(50);
      }

      Serial.println("Error on sending POST: " + String(httpResponseCode));
    }

    http.end();  // End connection
  } else {
    Serial.println("WiFi Disconnected");
  }
}






void loop() {
  // Look for RFID card
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    // Extract student data (ID) from card
    String studentID = readRFIDCard();

    // Get attendance time (current time)
    String attendanceTime = getAttendanceTime();

    // Post data to server (device ID + student data)
    postAttendanceData(studentID, deviceID);


    delay(1000);  // Delay to avoid multiple reads from the same card
  }
}
