
# Assignació de sensors a zones anatòmiques i connexions a la PCB

Aquest document descriu on s'ha col·locat cada sensor al collaret Philadelphia, quin connector de la PCB utilitza, i com es relaciona amb la numeració al codi.

## Sensors de temperatura i humitat (SHT31)

| Zona anatòmica              | Sensor | Multiplexor canal | Connector PCB |
|----------------------------|--------|--------------------|----------------|
| Occipital inferior dret     | S1T    | Canal 0            | P21            |
| Occipital superior dret     | S2T    | Canal 1            | P22            |
| Barbeta (calor central)     | S3T    | Canal 2            | P23            |
| Maxil·lar dret              | S4T    | Canal 3            | P24            |
| Occipital superior esquerre | S5T    | Canal 4            | P25            |
| Occipital inferior esquerre | S6T    | Canal 5            | P26            |
| Maxil·lar esq. posterior    | S7T    | Canal 6            | P27            |
| Maxil·lar esq. anterior     | S8T    | Canal 7            | P28            |

Nota: Els connectors P21–P28 estan etiquetats a la PCB per facilitar la connexió dels sensors SHT31 a través del multiplexor TCA9548A.

## Sensors de pressió (FlexiForce A401)

| Zona anatòmica              | Sensor | Pin ADC ESP32 | Connector PCB |
|----------------------------|--------|----------------|----------------|
| Occipital mig              | S1P    | GPIO 36        | J31            |
| Occipital inf. esquerre    | S2P    | GPIO 39        | J32            |
| Maxil·lar esquerre         | S3P    | GPIO 34        | J33            |
| Barbeta dreta              | S4P    | GPIO 35        | J34            |
| Barbeta esquerra           | S5P    | GPIO 32        | J35            |
| Maxil·lar dret             | S6P    | GPIO 33        | J36            |
| Occipital sup. dret        | S7P    | GPIO 25        | J37            |
| Occipital inf. dret        | S8P    | GPIO 26        | J38            |

Nota: Els connectors J31–J38 corresponen als canals d’entrada analògica del microcontrolador ESP32 i estan numerats a la PCB.


