
# Definició de zones anatòmiques mitjançant mides_rectangles.py

Aquest document explica com es defineixen les zones anatòmiques del coll monitoritzades mitjançant el script `mides_rectangles.py`.

Aquest script serveix per seleccionar visualment les coordenades de cada zona del collaret (com per exemple la barbeta, l’occipital, etc.) on es superposaran les dades dels sensors a la interfície web.

## Funcionament del codi

L’script `mides_rectangles.py` mostra una finestra amb la imatge base del collaret (`collar.png`). L’usuari ha de fer dos clics sobre la imatge per marcar les cantonades oposades d’un rectangle que representa una zona anatòmica.

Per cada rectangle, el codi imprimeix les coordenades corresponents al terminal, en el format següent:

```
Clic 1: (x1, y1)
Clic 2: (x2, y2)
→ Rectangle: [x1, y1, x2, y2]
```

Aquestes coordenades s’utilitzen després dins el fitxer `web.py` per definir les zones del mapa de calor i pressió.

## Exemple d’ús

```bash
python mides_rectangles.py
```

1. Apareix la imatge del collaret.
2. Fas dos clics per definir una zona (per exemple, la barbeta).
3. Apuntes les coordenades que imprimeix el terminal.
4. Repeteixes el procés per totes les zones d’interès.
5. Introdueixes aquestes coordenades a les variables `zones_temp` o `zones_press` del fitxer `web.py`.

## Utilitat

Aquest procés permet fer una associació visual i anatòmica precisa entre els sensors físics i les representacions digitals mostrades a la interfície gràfica.

