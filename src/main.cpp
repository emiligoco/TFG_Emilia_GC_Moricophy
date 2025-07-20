
#include <Arduino.h>
#include <Wire.h>
#include <SHT31.h>
#include <ArduinoJson.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

//Definim els servidors BLE
#define SERVICE_UUID   "6c8dfa24-87a0-41b4-a47c-f1674f1974c7"
#define CHAR_UUID_RX   "941e2b96-2189-4482-92ef-8abdca2412b7"
#define CHAR_UUID_TX   "8053f0ba-2459-4622-9838-a4f5d2b55e61"
BLECharacteristic *pTxCharacteristic;

//Definim les direccions corresponents 
#define TCAADDR 0x70
const uint8_t NUM_SENSORS = 8;

SHT31 sht31[NUM_SENSORS] = {
  SHT31(0x45), SHT31(0x45), SHT31(0x45), SHT31(0x45),
  SHT31(0x45), SHT31(0x45), SHT31(0x45), SHT31(0x45)
};


//Definim els pins ADC del ESP32 per llegir els valors dels sensors de pressió
const int pinVolt[NUM_SENSORS] = {36, 39, 34, 35, 32, 33, 25, 26};
float voltSuave[NUM_SENSORS] = {0.0f};
const int mostres = 5;
const float vRef = 3.3f;
const int resolADC = 4095;


//Funció: selecciona quin canal del mux s'està usant per activar el sensor correponent
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

  //Inicialitzame cada sensor de temp a través del mux
  for (uint8_t ch = 0; ch < NUM_SENSORS; ch++) {
    tcaselect(ch);
    delay(50);
    sht31[ch].begin();
  }

  //Configuració dispositiu BLE
  BLEDevice::init("ESP32-SensorsEmili");
  BLEServer *pServer = BLEDevice::createServer();
  BLEService *pService = pServer->createService(SERVICE_UUID);
  pService->createCharacteristic(CHAR_UUID_RX, 
                                 BLECharacteristic::PROPERTY_WRITE);
  pTxCharacteristic = pService->createCharacteristic(CHAR_UUID_TX, 
                                                     BLECharacteristic::PROPERTY_NOTIFY);
  pTxCharacteristic->addDescriptor(new BLE2902());
  pService->start();
  pServer->getAdvertising()->start();
  Serial.println("BLE iniciat");
}

void loop() {
  //Creació JSON amb dos grup (temp i press)
  StaticJsonDocument<2048> doc;
  JsonObject tempGroup = doc.createNestedObject("Temp");
  JsonObject pressGroup = doc.createNestedObject("Press");
  char sensorID[4];  

  //Per cada sensor de l'1 al 8 de cada grup genera el nom
  for (uint8_t i = 0; i < NUM_SENSORS; i++) {
    snprintf(sensorID, sizeof(sensorID), "s%u", i + 1);

    tcaselect(i);
    delay(20);

    //Lectura Temperatura i Humitat
    float temp = NAN, hum = NAN;
    if (sht31[i].read()) {
      temp = sht31[i].getTemperature();
      hum = sht31[i].getHumidity();
    }
    //Afegeix al JSON els valors de temp i humi
    JsonObject tObj = tempGroup.createNestedObject(sensorID);
    if (!isnan(temp)) tObj["T"] = temp;
    else              tObj["T"] = "null";

    if (!isnan(hum))  tObj["H"] = hum;
    else              tObj["H"] = "null";;

    //Lectura Vout
    long suma = 0;
    for (int k = 0; k < mostres; k++) {
      suma += analogRead(pinVolt[i]);
      delayMicroseconds(10);
    }
    //Llegeix les 5 mostres de cada sensor i aplica el filtratge
    float mitjana = suma / float(mostres);
    float volt = mitjana * (vRef / resolADC);
    voltSuave[i] = 0.9f * voltSuave[i] + 0.1f * volt;
    //Afegeix al JSON els valors de Vout
    JsonObject vObj = pressGroup.createNestedObject(sensorID);
    vObj["V"] = voltSuave[i];
  }

  //Enviem BLE
  char buffer[1024];
  size_t len = serializeJson(doc, buffer);
  pTxCharacteristic->setValue((uint8_t*)buffer, len);
  pTxCharacteristic->notify();

  Serial.println(buffer);
  delay(2000);
}
















