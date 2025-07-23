
# Monitorització de factors de risc cutanis en pacients amb collarets ortopèdics Philadelphia

## Objectiu del projecte

Aquest projecte de Treball Final de Grau consisteix en el disseny i la implementació d’un sistema **portable i intel·ligent** per monitoritzar en temps real **la pressió, la temperatura i la humitat** en pacients que utilitzen colls ortopèdics Philadelphia, amb la finalitat de prevenir l’aparició de lesions cutànies per pressió.

## Components del sistema

- Sensors de **pressió FlexiForce A401**
- Sensors **digitals de temperatura i humitat SHT31**
- **Microcontrolador ESP32** amb comunicació **Bluetooth Low Energy**
- **Multiplexor I2C TCA9548A**
- Sistema de **visualització web en temps real** amb mapes de calor i pressió

## Estructura del repositori

```
├── main.cpp              # Codi firmware ESP32: adquisició i enviament de dades
├── ble.py                # Script Python per rebre dades via BLE i desar-les
├── web.py                # Interfície web en Streamlit per visualització de dades
├── calibraciopresio.txt  # Calibratge sensors de pressió
├── probatemp.txt         # Test sensors SHT31
├── mides_rectangles.py   # Utilitat per definir zones visuals del collaret
├── dades.json            # Fitxer generat automàticament amb dades dels sensors
├── collar.png            # Imatge base del collaret per visualització
└── README.md             # Aquest document
```

## Requisits d’instal·lació

### Software

- [Arduino IDE](https://www.arduino.cc/en/software)
- Llibreries Arduino:
  - `SHT31.h`
  - `Wire.h`
  - `BLEDevice.h`
  - `ArduinoJson.h`

- [Python 3](https://www.python.org/)
- Paquets Python:
  ```bash
  pip install bleak streamlit pillow matplotlib
  ```

### Hardware

- ESP32-WROOM-32 Dev Kit
- 8x SHT31 (Sensirion)
- 8x FlexiForce A401
- Multiplexor I2C TCA9548A
- Bateria LiPo 3.7V
- Collaret ortopèdic Philadelphia

---

## Manual d’usuari

1. **Col·loca** el collaret amb els sensors integrats sobre el pacient.
2. **Connecta** cada sensor de la zona anatòmica, al connector correponent (veure docX de la carpeta Docs)
3. **Connecta** el sistema mitjançant USB per carregar el programa al microcontrolador.
4. Executa el codi de l’ESP32 (`main.cpp`) per començar a llegir les dades.
5. Al teu ordinador:
   - Llença `ble.py` per rebre les dades per BLE. Si s'ha connectat, desconnectar l'USB i treballar en remot.
   - Llença `web.py` per obrir la visualització web. Per llençar aquest script, al terminal s'ha d'escriure:
     ```bash
     streamlit run web.py
     ```
6. Observa les dades en temps real: zones en verd, taronja o vermell segons risc.

---

## Exemple de sortida

```
'main.cpp'
BLE iniciat
{"Temp": {"s1":{ "T": 30.45, "H": 56.4 },"s2":{ "T": 30.98, "H": 57.1 },...},"Press": {"s1":{ "V": 0.298 },"s2":{ "V": 0.329 },...}

'ble.py'
Escanejant dispositius BLE...
Connectant amb C3:7A:2B:XX:XX:XX...
Connectat! Esperant dades...
Dades rebudes i desades
Dades rebudes i desades
Dades rebudes i desades
...

```

---

## Manual d’instal·lació

### Firmware ESP32
1. Connecta l’ESP32 via USB.
2. Obre `main.cpp` a l’IDE d’Arduino.
3. Carrega les llibreries necessàries.
4. Puja el codi al dispositiu.

### Rebre dades
```bash
python3 ble.py
```

### Visualitzar dades en temps real
```bash
streamlit run web.py
```

---

## Autora

**Emilia Gómez Colomer**  
Grau en Enginyeria Biomèdica  
Universitat de Girona

---

## Llicència

Aquest projecte es distribueix sota la llicència MIT.
