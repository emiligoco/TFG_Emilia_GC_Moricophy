import streamlit as st
import time
import json
from PIL import Image, ImageDraw

IMAGE_PATH = "src/collar.png"
DADES_FILE = "dades.json"

#Coordenades de zones per calor
zones_temp = {
    "barbeta_calor": (932, 368, 1193, 443),
    "maxilar_dret": (737, 319, 866, 490),
    "maxilar_esquerre_posterior": (898, 202, 996, 286),
    "maxilar_esquerre_anterior": (1005, 235, 1086, 305),
    "occipital_inf_dret": (370, 345, 520, 424),
    "occipital_sup_dret": (322, 165, 542, 308),
    "occipital_inf_esq": (688, 167, 793, 284),
    "occipital_sup_esq": (600, 295, 723, 370),
}

#Coordenades de zones per pressió
zones_press = {
    "barbeta_dreta": (982, 392, 1124, 444),
    "barbeta_esquerra": (1116, 367, 1213, 413),
    "maxilar_dret": (737, 319, 866, 490),
    "maxilar_esquerre": (950, 192, 1094, 324),
    "occipital_inf_dret": (359, 280, 523, 398),
    "occipital_sup_dret": (373, 78, 552, 181),
    "occipital_inf_esq": (688, 167, 793, 284),
    "occipital_mig": (558, 264, 685, 359),
}

#Relació sensors de temp amb les zones
sensor_temp_to_zone = {
    "s1": "occipital_inf_dret",
    "s2": "occipital_sup_dret",
    "s3": "barbeta_calor",  
    "s4": "maxilar_dret",
    "s5": "occipital_sup_esq",
    "s6": "occipital_inf_esq",
    "s7": "maxilar_esquerre_posterior",  
    "s8": "maxilar_esquerre_anterior",   
}

#Relació sensors de press amb les zones
sensor_press_to_zone = {
    "s1": "occipital_mig",
    "s2": "occipital_inf_esq",
    "s3": "maxilar_esquerre",
    "s4": "barbeta_dreta",
    "s5": "barbeta_esquerra",
    "s6": "maxilar_dret",
    "s7": "occipital_sup_dret",
    "s8": "occipital_inf_dret",
}

sensor_zone_labels = {
    "S1T": "Occipital inferior dret",
    "S2T": "Occipital superior dret",
    "S3T": "Barbeta calor",
    "S4T": "Maxil·lar dret",
    "S5T": "Occipital superior esquerre",
    "S6T": "Occipital inferior esquerre",
    "S7T": "Maxil·lar esquerre posterior calor",
    "S8T": "Maxil·lar esquerre anterior calor",
    "S1P": "Occipital mig",
    "S2P": "Occipital inferior esquerre",
    "S3P": "Maxil·lar esquerre",
    "S4P": "Barbeta dreta pressio",
    "S5P": "Barbeta esquerra pressio",
    "S6P": "Maxil·lar dret",
    "S7P": "Occipital superior dret",
    "S8P": "Occipital inferior dret",
}

#Conversió text a float
def parse_float(value):
    try:
        return float(value)
    except:
        return None

#Classificació del risc segons el Vout
def classify_pressure(v):
    if v < 0.05:
        return "SENSE PRESSIÓ"
    elif v < 0.20:
        return "BAIXA"
    elif v < 0.55:
        return "MODERADA"
    elif v < 0.85:
        return "POSIBLE LESIÓ"
    elif v < 1.20:
        return "LESIÓ"
    else:
        return "LESIÓ CRÍTICA"

#Conversió de V a pes (kg)
def volt_to_pes(v):
    return round(0.7224 * (v ** 2) + 0.2238 * v + 0.0192, 3) 

#Es dibuixen el rectangles de calor sobre la imatge
def draw_temp_overlay(data, mapping, zones):
    base = Image.open(IMAGE_PATH).convert("RGBA")
    overlay = Image.new("RGBA", base.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    for sid, zone in mapping.items():
        box = zones.get(zone)
        if not box:
            continue

        obj = data.get(sid, {})
        temp = parse_float(obj.get("T"))

        if temp is None:
            color = (0, 255, 0, 120)  
        elif temp <= 32:
            color = (0, 255, 0, 120)
        elif temp <=34:
            color = (255, 165, 0, 120)
        else:
            color = (255, 0, 0, 120)

        draw.rectangle(box, fill=color)

    return Image.alpha_composite(base, overlay)

#Es dibuixen els rectangles de pressió sobre la imatge
def draw_press_overlay(data, mapping, zones):
    base = Image.open(IMAGE_PATH).convert("RGBA")
    overlay = Image.new("RGBA", base.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    for sid, zone in mapping.items():
        box = zones.get(zone)
        if not box:
            continue

        obj = data.get(sid, {})
        v = parse_float(obj.get("V"))

        if v is None:
            color = (0, 255, 0, 120)  
        elif v < 0.20:
            color = (0, 255, 0, 120)
        elif v <= 0.55:
            color = (255, 165, 0, 120)
        else:
            color = (255, 0, 0, 120)

        draw.rectangle(box, fill=color)

    return Image.alpha_composite(base, overlay)

#Streamlit Web
st.set_page_config(layout="centered")
st.title("Monitorització del collarí")

#Creació de les dues columnes per mostras les dues imatges
col1, col2 = st.columns(2)
col1.subheader("Mapa de calor")
col2.subheader("Mapa de pressió")
img_col1 = col1.empty()
img_col2 = col2.empty()
#Area per mostrar la taula
table_area = st.empty()

#Llegir i mostrar les dades cada 2"
while True:
    try:
        with open(DADES_FILE, "r") as f:
            raw = json.load(f)
        #Convertim les dades en un format unificat per tipus de sensor
        data = {}
        for s, vals in raw.get("Temp", {}).items():
            data[s] = {"T": vals["T"], "H": vals["H"], "V": 0.0}
        for s, vals in raw.get("Press", {}).items():
            if s in data:
                data[s]["V"] = vals["V"]
            else:
                data[s] = {"T": None, "H": None, "V": vals["V"]}
    except Exception:
        data = {}

    #Generem les imatges amb superposició de les dades
    img_temp = draw_temp_overlay(data, sensor_temp_to_zone, zones_temp)
    img_press = draw_press_overlay(data, sensor_press_to_zone, zones_press)

    #Es msotren les imatges a la interfície
    img_col1.image(img_temp, use_container_width=True)
    img_col2.image(img_press, use_container_width=True)

    #Diccionari per organitzar les dades per zona
    zona_map = {}
    for sid, obj in data.items():
        sidT = sid.upper() + "T"
        sidP = sid.upper() + "P"
        if sidT in sensor_zone_labels:
            zona = sensor_zone_labels[sidT]
            zona_map.setdefault(zona, {})["T"] = obj
        if sidP in sensor_zone_labels:
            zona = sensor_zone_labels[sidP]
            zona_map.setdefault(zona, {})["P"] = obj

    #Convertim les dades en una taula per visualitzar
    table = []
    for zona, vals in zona_map.items():
        row = {"Zona": zona}
        if "T" in vals:
            row.update({
                "Temp (ºC)": parse_float(vals["T"]["T"]),
                "Hum (%)": parse_float(vals["T"]["H"])
        })
        if "P" in vals:
            pes = volt_to_pes(vals["P"]["V"])
            zona_risc = classify_pressure(vals["P"]["V"])
            row.update({
                "Pes (kg)": pes,
                "Risc": zona_risc
            })
        table.append(row)

    #Es msotra la taula a streamlit
    table_area.dataframe(table, hide_index=True)
    time.sleep(2)
