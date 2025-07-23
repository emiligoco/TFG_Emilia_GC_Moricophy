
# Validació inicial dels sensors: proves sobre protoboard

Aquest document recull totes les proves experimentals preliminars realitzades per validar el funcionament dels sensors individualment i conjuntament abans d'integrar el sistema final. Totes aquestes proves es van fer sobre protoboard, per assegurar la compatibilitat electrònica i funcional dels components. Les trobareu a la carpeta `test`.

---

## Prova 1: Validació sensors SHT31 (`probatemp.txt`)

### Objectiu
Verificar el funcionament de dos sensors de temperatura i humitat **SHT31** (DFRobot) a través d’un **multiplexor I2C TCA9548A**.

### Requisits
- 2 mòduls SHT31 de DFRobot  
  Ref: [DFRobot SEN0331](https://www.dfrobot.com/product-2013.html)
- 1 multiplexor I2C TCA9548A  
  Ref: [TCA9548A Datasheet - Texas Instruments](https://www.ti.com/lit/ds/symlink/tca9548a.pdf)
- Microcontrolador ESP32
- Protoboard i cables jumper

### Connexions
- Cada SHT31 es connecta a el canal 2 i el canal 6 del multiplexor.
- El TCA9548A es connecta al bus I2C de l’ESP32 (SDA, SCL).
- Alimentació: 3.3V i GND per a tots els components.

### Execució
- Copia el contingut de `probatemp.txt` dins del fitxer  `main.cpp` i puja’l a l’ESP32.
- Obre el monitor sèrie.

### Resultats obtinguts

```
SHT31 en canal 2 detectat
SHT31 en canal 6 detectat
Sensor 2 - Temperatura: 30.98 °C
Sensor 2 - Humitat: 56.4 %
Sensor 6 - Temperatura: 27.03 °C
Sensor 6 - Humitat: 58.1 %
```

> Això valida la comunicació I2C múltiple mitjançant el multiplexor.

---

## Prova 2: Calibratge i validació sensors FlexiForce A401 (`calibraciopresio.txt`)

### Objectiu
Verificar la lectura de voltatge dels sensors de pressió FlexiForce A401 a través del seu circuit de condicionament analògic.

### Requisits
- Sensor FlexiForce A401  
  Ref: [Tekscan A401 Datasheet](https://www.tekscan.com/products-solutions/flexiforce-sensors/a401)
- Amplificador operatiu MCP6004
- Resistència de retroalimentació (Rf = 300kohms) i Vref negativa 
- ESP32 (entrades ADC)
- Font d’alimentació i multímetre
- Protoboard

### Connexió
- Rs (sensor) connectat a l'entrada inversora del op-amp.
- Rf i Vref negativa (aprox. -1.25V generada per la font d'alimentació externa).
- Vout connectat a una entrada ADC de l'ESP32 (veure linia del codi `pinSensor[8]`)
- Opcional: Provar diversos sensors en paral·lel (fins a 8 canals).

### Execució
- Copia `calibraciopresio.txt` dins del fitxer  `main.cpp`i carrega’l a l’ESP32.
- Obre el monitor sèrie.

### Resultats

```
Sensor canal 1 → Vout suau: 0.298 V
Sensor canal 1 → Vout suau: 0.329 V
```

> Quan s’aplica pes (ex: 200 g), el voltatge augmenta. Sense càrrega, el voltatge es manté baix. Filtrat exponencial aplicat al codi.

---

## Prova 3: Validació conjunta de sensors (`provaconjunta.cpp`)

### Objectiu
Verificar que els sensors de pressió i temperatura funcionen **simultàniament** amb l’ESP32, preparats per la integració al sistema final.

### Muntatge
- Connectar 2 sensors SHT31 a dos canals del TCA9548A.
- Connectar 2 sensors FlexiForce amb el seu circuit a dos canals ADC.
- Tots els components sobre protoboard.

### Execució
- Càrrega del codi `provaconjunta.cpp` a l’ESP32.
- Observar el port sèrie.

### Resultats

```
Temp canal 0  T: 30.52 °C  H: 56.4 %
Press canal 1 V: 0.042 V
Temp canal 1  T: 30.45 °C  H: 56.4 %
Press canal 2 V: 0.019 V
```

> Es confirma que el sistema pot llegir sensors múltiples i preparar les dades per ser transmeses via BLE (següent etapa).

---

Aquestes proves han estat essencials per validar individualment el hardware i garantir que el firmware final (`main.cpp`) funcioni correctament quan tot el sistema estigui integrat.
