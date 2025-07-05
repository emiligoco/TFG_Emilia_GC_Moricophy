// #include <Arduino.h>
// #include <Wire.h>
// #include <SHT31.h>
// #include <ArduinoJson.h>
// #include <BLEDevice.h>
// #include <BLEServer.h>
// #include <BLEUtils.h>
// #include <BLE2902.h>
// #include <math.h> 

// //Configuració Sensors Temperatura i Humitat
// #define TCAADDR     0x70
// const uint8_t NUM_TEMP = 8;
// SHT31 sht31[NUM_TEMP] = {
//   SHT31(0x45), SHT31(0x45), SHT31(0x45), SHT31(0x45),
//   SHT31(0x45), SHT31(0x45), SHT31(0x45), SHT31(0x45)
// };
// void tcaselect(uint8_t ch) {
//   if (ch > 7) return;
//   Wire.beginTransmission(TCAADDR);
//   Wire.write(1 << ch);
//   Wire.endTransmission();
// }

// //Configuració Sensors pressió
// const uint8_t NUM_VOLT = 8;
// const int pinVolt[NUM_VOLT] = {36, 39, 34, 35, 32, 33, 25, 26};
// float voltSuave[NUM_VOLT] = {0.0f};
// const int N_MUESTRAS = 5;
// const float vRef     = 3.3f;
// const int   resolADC = 4095;

// //BLE
// #define SERVICE_UUID   "6c8dfa24-87a0-41b4-a47c-f1674f1974c7"
// #define CHAR_UUID_RX   "941e2b96-2189-4482-92ef-8abdca2412b7"
// #define CHAR_UUID_TX   "8053f0ba-2459-4622-9838-a4f5d2b55e61"
// BLECharacteristic *pTxCharacteristic;

// void setup() {

//   Serial.begin(115200);
//   //Comunicació I2C temp
//   Wire.begin(21, 22);
//   Wire.setClock(400000);
//   for (uint8_t ch = 0; ch < NUM_TEMP; ch++) {
//     tcaselect(ch);
//     delay(50);
//     sht31[ch].begin();
//   }
//   //Ressolució pressió
//   analogReadResolution(12);

//  //BLE
//   BLEDevice::init("ESP32-Sensores");
//   BLEServer *pServer = BLEDevice::createServer();
//   BLEService *pService = pServer->createService(SERVICE_UUID);
//   pService->createCharacteristic(CHAR_UUID_RX,
//                                   BLECharacteristic::PROPERTY_WRITE
//                                 );
//   pTxCharacteristic = pService->createCharacteristic(CHAR_UUID_TX,
//                                                      BLECharacteristic::PROPERTY_NOTIFY
//                                                     );
//   pTxCharacteristic->addDescriptor(new BLE2902());
//   pService->start();
//   pServer->getAdvertising()->start();
//   Serial.println("BLE UART iniciado");
// }


// void loop() {
//   //Preparem el Json
//   StaticJsonDocument<1024> doc;
//   char objName[12];
//   //Llegim els valors dels sensors de temperatura i humitat
//   for (uint8_t i = 0; i < NUM_VOLT; i++) {
//     tcaselect(i);
//     delay(20);
//     float t = NAN, h = NAN;
//     if (sht31[i].read()) {
//       t = sht31[i].getTemperature();
//       h = sht31[i].getHumidity();
//     }

//     //Llegim Vout dels sensors de pressio
//     long sum = 0;
//     for (int k = 0; k < N_MUESTRAS; k++) {
//       sum += analogRead(pinVolt[i]);
//       delayMicroseconds(10);
//     }
//     float mean = sum / float(N_MUESTRAS);
//     float v = mean * (vRef / resolADC);
//     voltSuave[i] = 0.9f * voltSuave[i] + 0.1f * v;

//     //Es crea un objecte del tipus
//     snprintf(objName, sizeof(objName), "Sensor%u", i + 1);
//     JsonObject sensorObj = doc.createNestedObject(objName);

//     //Assignem cada valor corresponent o NULL en cas de fallida
//     if (!isnan(t)) sensorObj["T"] = t;
//     else              sensorObj["T"] = nullptr;

//     if (!isnan(h)) sensorObj["H"] = h;
//     else              sensorObj["H"] = nullptr;

//     sensorObj["V"] = voltSuave[i];
//   }

//   //Enviament per BLE
//   char buffer[1024];
//   size_t len = serializeJson(doc, buffer);
//   pTxCharacteristic->setValue((uint8_t*)buffer, len);
//   pTxCharacteristic->notify();

//   //Depurem
//   Serial.println(buffer);

//   delay(2000);
// }

#include <Arduino.h>
#include <Wire.h>
#include <SHT31.h>
#include <ArduinoJson.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define TCAADDR 0x70
const uint8_t NUM_SENSORS = 8;

SHT31 sht31[NUM_SENSORS] = {
  SHT31(0x45), SHT31(0x45), SHT31(0x45), SHT31(0x45),
  SHT31(0x45), SHT31(0x45), SHT31(0x45), SHT31(0x45)
};

const int pinVolt[NUM_SENSORS] = {36, 39, 34, 35, 32, 33, 25, 26};
float voltSuave[NUM_SENSORS] = {0.0f};
const int N_MUESTRAS = 5;
const float vRef = 3.3f;
const int resolADC = 4095;

#define SERVICE_UUID   "6c8dfa24-87a0-41b4-a47c-f1674f1974c7"
#define CHAR_UUID_RX   "941e2b96-2189-4482-92ef-8abdca2412b7"
#define CHAR_UUID_TX   "8053f0ba-2459-4622-9838-a4f5d2b55e61"
BLECharacteristic *pTxCharacteristic;

void tcaselect(uint8_t ch) {
  if (ch > 7) return;
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << ch);
  Wire.endTransmission();
}

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);
  Wire.setClock(400000);
  analogReadResolution(12);

  for (uint8_t ch = 0; ch < NUM_SENSORS; ch++) {
    tcaselect(ch);
    delay(50);
    sht31[ch].begin();
  }

  BLEDevice::init("ESP32-SensorsEmili");
  BLEServer *pServer = BLEDevice::createServer();
  BLEService *pService = pServer->createService(SERVICE_UUID);
  pService->createCharacteristic(CHAR_UUID_RX, BLECharacteristic::PROPERTY_WRITE);
  pTxCharacteristic = pService->createCharacteristic(CHAR_UUID_TX, BLECharacteristic::PROPERTY_NOTIFY);
  pTxCharacteristic->addDescriptor(new BLE2902());
  pService->start();
  pServer->getAdvertising()->start();
  Serial.println("BLE iniciat");
}

void loop() {
  StaticJsonDocument<2048> doc;
  JsonObject tempGroup = doc.createNestedObject("Temp");
  JsonObject pressGroup = doc.createNestedObject("Press");
  char sensorID[4];  // Ex: "s1", "s2", ...

  for (uint8_t i = 0; i < NUM_SENSORS; i++) {
    snprintf(sensorID, sizeof(sensorID), "s%u", i + 1);

    tcaselect(i);
    delay(20);

    // --- LECTURA TEMP/HUM ---
    float temp = NAN, hum = NAN;
    if (sht31[i].read()) {
      temp = sht31[i].getTemperature();
      hum = sht31[i].getHumidity();
    }
    JsonObject tObj = tempGroup.createNestedObject(sensorID);
    if (!isnan(temp)) tObj["T"] = temp;
    else              tObj["T"] = "null";

    if (!isnan(hum))  tObj["H"] = hum;
    else              tObj["H"] = "null";;

    // --- LECTURA VOLTATGE ---
    long suma = 0;
    for (int k = 0; k < N_MUESTRAS; k++) {
      suma += analogRead(pinVolt[i]);
      delayMicroseconds(10);
    }
    float mitjana = suma / float(N_MUESTRAS);
    float volt = mitjana * (vRef / resolADC);
    voltSuave[i] = 0.9f * voltSuave[i] + 0.1f * volt;

    JsonObject vObj = pressGroup.createNestedObject(sensorID);
    vObj["V"] = voltSuave[i];
  }

  // --- ENVIAMENT BLE ---
  char buffer[1024];
  size_t len = serializeJson(doc, buffer);
  pTxCharacteristic->setValue((uint8_t*)buffer, len);
  pTxCharacteristic->notify();

  Serial.println(buffer);
  delay(2000);
}









