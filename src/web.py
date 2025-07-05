# import asyncio
# import json
# from bleak import BleakClient, BleakScanner

# SERVICE_UUID = "6c8dfa24-87a0-41b4-a47c-f1674f1974c7"
# CHAR_UUID_TX = "8053f0ba-2459-4622-9838-a4f5d2b55e61"

# def classify_pressure(volt):
#     if volt < 0.05:
#         return "SENSE PRESSIÓ"
#     elif volt < 0.20:
#         return "BAIXA"
#     elif volt < 0.55:
#         return "MODERADA"
#     elif volt < 0.85:
#         return "POSIBLE LESIÓ"
#     elif volt < 1.20:
#         return "LESIÓ"
#     else:
#         return "LESIÓ CRÍTICA"

# def calculate_weight(volt):
#     return 0.7224 * volt ** 2 + 0.2238 * volt + 0.0192

# async def main():
#     print("Escanejant BLE…")
#     devices = await BleakScanner.discover()
#     addr = next((d.address for d in devices
#                  if d.name and "ESP32-SensorsEmili" in d.name),
#                 None)
#     if not addr:
#         print("No trobat dispositiu ESP32-SensorsEmili")
#         return

#     print(f"Connectant a {addr}…")
#     async with BleakClient(addr) as client:
#         await client.start_notify(CHAR_UUID_TX, notification_handler)
#         print("Connectat. Esperant dades…\n")
#         while True:
#             await asyncio.sleep(1)

# def notification_handler(sender, data: bytearray):
#     try:
#         payload = json.loads(data.decode('utf-8'))
#     except json.JSONDecodeError:
#         print("JSON invàlid:", data)
#         return

#     temp_data = payload.get("Temp", {})
#     press_data = payload.get("Press", {})

#     print("=== Sensors Temperatura i Humitat ===")
#     for i in range(1, 9):
#         key = f"s{i}"
#         t_data = temp_data.get(key, {})
#         t = t_data.get("T")
#         h = t_data.get("H")

#         print(f"S{i}T:")
#         print(f"  - Temp       : {t} °C")
#         print(f"  - Humitat    : {h} %")

#     print("\n=== Sensors Pressió ===")
#     for i in range(1, 9):
#         key = f"s{i}"
#         p_data = press_data.get(key, {})
#         v = p_data.get("V")
#         pes = calculate_weight(v) if v is not None else None
#         zona = classify_pressure(v) if v is not None else "N/A"

#         print(f"S{i}P:")
#         print(f"  - Pes estimat: {pes:.3f} kg" if pes is not None else "  - Pes estimat: N/A")
#         print(f"  - Zona risc  : {zona}")
#     print()

# if __name__ == "__main__":
#     asyncio.run(main())


# import asyncio
# import json
# import threading
# import random
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# from matplotlib.colors import LinearSegmentedColormap
# import numpy as np
# from PIL import Image, ImageDraw
# from bleak import BleakClient, BleakScanner

# # === CONFIGURACIÓ GENERAL ===
# SIMULACIO = True  # ⚠️ Posa a False quan vulguis dades reals via BLE
# IMAGE_PATH = "src/collar.png"  # Assegura't que la ruta és correcta

# SERVICE_UUID = "6c8dfa24-87a0-41b4-a47c-f1674f1974c7"
# CHAR_UUID_TX = "8053f0ba-2459-4622-9838-a4f5d2b55e61"

# base_image = Image.open(IMAGE_PATH).convert("RGBA")

# # === ZONES DEFINIDES SOBRE EL COLLAR ===
# zones = {
#     "barbeta": [(1020, 398, 1162, 411)],
#     "maxilar_dret": [(785, 371, 934, 482)],
#     "maxilar_esquerre": [(934, 232, 1067, 335)],
#     "occipital_inf_dret": [(357, 364, 490, 448)],
#     "occipital_sup_dret": [(351, 237, 508, 340)],
#     "occipital_inf_esq": [(606, 346, 722, 427)],
#     "occipital_sup_esq": [(658, 121, 766, 256)],
#     "occipital_mig": [(528, 240, 646, 306)],
# }

# # === MAPA DE SENSORS A ZONES ===
# temp_sensor_to_zone = {
#     "s1": "occipital_inf_dret", "s2": "occipital_sup_dret", "s3": "barbeta", "s4": "maxilar_dret",
#     "s5": "occipital_sup_esq", "s6": "occipital_inf_esq", "s7": "maxilar_esquerre", "s8": "maxilar_esquerre"
# }
# press_sensor_to_zone = {
#     "s1": "occipital_mig", "s2": "occipital_inf_esq", "s3": "maxilar_esquerre", "s4": "barbeta",
#     "s5": "barbeta", "s6": "maxilar_dret", "s7": "occipital_sup_dret", "s8": "occipital_inf_dret"
# }

# latest_temp_data = {}
# latest_press_data = {}

# # === FUNCIONS DE VISUALITZACIÓ ===
# def value_to_color(value):
#     r = int(255 * value)
#     g = int(255 * (1 - value))
#     return (r, g, 0, 120)

# def draw_overlay(data_map, mapping):
#     overlay = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
#     draw = ImageDraw.Draw(overlay)
#     zone_vals = {z: [] for z in zones}

#     for sensor, val in data_map.items():
#         zona = mapping.get(sensor)
#         if zona:
#             zone_vals[zona].append(val)

#     for zona, valors in zone_vals.items():
#         if valors:
#             mitjana = sum(valors) / len(valors)
#             color = value_to_color(mitjana)
#             for box in zones[zona]:
#                 draw.rectangle(box, fill=color)

#     return Image.alpha_composite(base_image, overlay)

# # === FIGURA MATPLOTLIB ===
# fig = plt.figure(figsize=(12, 10))
# gs = fig.add_gridspec(3, 2, height_ratios=[8, 0.5, 0.5])

# ax1 = fig.add_subplot(gs[0, 0])
# ax2 = fig.add_subplot(gs[0, 1])
# ax3 = fig.add_subplot(gs[1, 0])
# ax4 = fig.add_subplot(gs[1, 1])

# ax1.set_title("Temperatura i Humitat")
# ax2.set_title("Pressió")
# for ax in [ax1, ax2, ax3, ax4]:
#     ax.axis("off")

# im1 = ax1.imshow(base_image)
# im2 = ax2.imshow(base_image)

# def setup_legends():
#     cmap = LinearSegmentedColormap.from_list("heat", [(0, 1, 0), (1, 0, 0)])
#     gradient = np.linspace(0, 1, 256).reshape(1, -1)
#     ax3.imshow(gradient, aspect='auto', cmap=cmap)
#     ax3.set_xticks([0, 255])
#     ax3.set_xticklabels(['Baixa', 'Alta'], fontsize=10)
#     ax3.set_yticks([])

#     ax4.imshow(gradient, aspect='auto', cmap=cmap)
#     ax4.set_xticks([0, 255])
#     ax4.set_xticklabels(['Baixa', 'Alta'], fontsize=10)
#     ax4.set_yticks([])

# setup_legends()

# # === ACTUALITZACIÓ DELS GRÀFICS ===
# def update_plot(frame):
#     global latest_temp_data, latest_press_data

#     if SIMULACIO:
#         latest_temp_data = {f"s{i}": random.uniform(0, 1) for i in range(1, 9)}
#         latest_press_data = {f"s{i}": random.uniform(0, 1) for i in range(1, 9)}

#     t_img = draw_overlay(latest_temp_data, temp_sensor_to_zone)
#     p_img = draw_overlay(latest_press_data, press_sensor_to_zone)
#     im1.set_data(t_img)
#     im2.set_data(p_img)
#     return [im1, im2]

# # === BLE CALLBACK ===
# def notification_handler(sender, data: bytearray):
#     global latest_temp_data, latest_press_data
#     try:
#         payload = json.loads(data.decode('utf-8'))
#     except Exception:
#         return

#     temp_data = {}
#     press_data = {}

#     for s, val in payload.get("Temp", {}).items():
#         t, h = val.get("T"), val.get("H")
#         if isinstance(t, (float, int)) and isinstance(h, (float, int)):
#             nt = min(max((t - 20) / 20, 0), 1)
#             nh = min(max(h / 100, 0), 1)
#             temp_data[s] = 0.5 * nt + 0.5 * nh

#     for s, val in payload.get("Press", {}).items():
#         v = val.get("V")
#         if isinstance(v, (float, int)):
#             press_data[s] = min(max(v / 1.5, 0), 1)

#     latest_temp_data = temp_data
#     latest_press_data = press_data

# # === BLE CONNECTION LOOP ===
# async def run_ble():
#     print("Buscant dispositiu BLE...")
#     devices = await BleakScanner.discover()
#     addr = next((d.address for d in devices if d.name and "ESP32-SensorsEmili" in d.name), None)
#     if not addr:
#         print("No trobat")
#         return

#     async with BleakClient(addr) as client:
#         await client.start_notify(CHAR_UUID_TX, notification_handler)
#         print("Connectat a ESP32-SensorsEmili")
#         while True:
#             await asyncio.sleep(1)

# def start_ble_thread():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(run_ble())

# # === EXECUCIÓ PRINCIPAL ===
# if __name__ == "__main__":
#     if not SIMULACIO:
#         threading.Thread(target=start_ble_thread, daemon=True).start()

#     ani = FuncAnimation(fig, update_plot, interval=2000)
#     plt.tight_layout()
#     plt.show()


# import matplotlib.pyplot as plt
# from PIL import Image

# image_path = "src/collar.png"
# img = Image.open(image_path)

# clicks = []

# def onclick(event):
#     if event.xdata and event.ydata:
#         x, y = int(event.xdata), int(event.ydata)
#         clicks.append((x, y))
#         print(f"Clic {len(clicks)}: ({x}, {y})")
#         if len(clicks) == 2:
#             (x1, y1), (x2, y2) = clicks
#             print(f"→ Rectangle: [{x1}, {y1}, {x2}, {y2}]\n")
#             clicks.clear()  # esperem el següent parell de clics

# fig, ax = plt.subplots(figsize=(10, 8))
# ax.imshow(img)
# ax.set_title("Fes DOS CLICS per zona (SE + ID)")
# cid = fig.canvas.mpl_connect('button_press_event', onclick)
# plt.show()


import streamlit as st
import time
import json
from PIL import Image, ImageDraw

# === CONFIG ===
IMAGE_PATH = "src/collar.png"
DADES_FILE = "dades.json"

zones_temp = {
    "barbeta": (932, 368, 1193, 443),
    "maxilar_dret": (737, 319, 866, 490),
    "maxilar_esquerre": (950, 192, 1094, 324),
    "occipital_inf_dret": (370, 345, 520, 424),
    "occipital_sup_dret": (322, 165, 542, 308),
    "occipital_inf_esq": (688, 167, 793, 284),
    "occipital_sup_esq": (600, 295, 723, 370),
}

zones_press = {
    "barbeta": (932, 368, 1193, 443),
    "maxilar_dret": (737, 319, 866, 490),
    "maxilar_esquerre": (950, 192, 1094, 324),
    "occipital_inf_dret": (359, 280, 523, 398),
    "occipital_sup_dret": (373, 78, 552, 181),
    "occipital_inf_esq": (688, 167, 793, 284),
    "occipital_mig": (558, 264, 685, 359),
}

sensor_temp_to_zone = {
    "s1": "occipital_inf_dret",
    "s2": "occipital_sup_dret",
    "s3": "barbeta",
    "s4": "maxilar_dret",
    "s5": "occipital_sup_esq",
    "s6": "occipital_inf_esq",
    "s7": "maxilar_esquerre",
    "s8": "maxilar_esquerre",
}

sensor_press_to_zone = {
    "s1": "occipital_mig",
    "s2": "occipital_inf_esq",
    "s3": "maxilar_esquerre",
    "s4": "barbeta",
    "s5": "barbeta",
    "s6": "maxilar_dret",
    "s7": "occipital_sup_dret",
    "s8": "occipital_inf_dret",
}

sensor_zone_labels = {
    "S1T": "Occipital inferior dret",
    "S2T": "Occipital superior dret",
    "S3T": "Barbeta",
    "S4T": "Maxil·lar dret",
    "S5T": "Occipital superior esquerre",
    "S6T": "Occipital inferior esquerre",
    "S7T": "Maxil·lar esquerre",
    "S8T": "Maxil·lar esquerre",
    "S1P": "Occipital mig",
    "S2P": "Occipital inferior esquerre",
    "S3P": "Maxil·lar esquerre",
    "S4P": "Barbeta",
    "S5P": "Barbeta",
    "S6P": "Maxil·lar dret",
    "S7P": "Occipital superior dret",
    "S8P": "Occipital inferior dret",
}

# === FUNCIONS ===
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
        return "CRÍTICA"

def volt_to_pes(v):
    return round(0.7224 * (v ** 2) + 0.2238 * v + 0.0192, 3)

def value_to_color(value):
    r = int(255 * value)
    g = int(255 * (1 - value))
    return (r, g, 0, 120)

def draw_overlay(data, mapping, zones):
    base = Image.open(IMAGE_PATH).convert("RGBA")
    overlay = Image.new("RGBA", base.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    for sid, obj in data.items():
        zone = mapping.get(sid)
        if not zone: continue
        box = zones.get(zone)
        if not box: continue
        v = obj["V"]
        norm = min(max(v / 1.5, 0.0), 1.0)
        color = value_to_color(norm)
        draw.rectangle(box, fill=color)
    return Image.alpha_composite(base, overlay)

# === STREAMLIT ===
st.set_page_config(layout="centered")
st.title("Monitorització intel·ligent del collarí")

col1, col2 = st.columns(2)
col1.subheader("Mapa de calor (Temp/Humitat)")
col2.subheader("Mapa de pressió")

img_col1 = col1.empty()
img_col2 = col2.empty()

table_area = st.empty()

while True:
    try:
        with open(DADES_FILE, "r") as f:
            raw = json.load(f)
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

    img_temp = draw_overlay(data, sensor_temp_to_zone, zones_temp)
    img_press = draw_overlay(data, sensor_press_to_zone, zones_press)

    img_col1.image(img_temp, use_container_width=True)
    img_col2.image(img_press, use_container_width=True)

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

    table = []
    for zona, vals in zona_map.items():
        row = {"Zona": zona}
        if "T" in vals:
            row.update({
                "Temp (ºC)": vals["T"]["T"],
                "Hum (%)": vals["T"]["H"]
            })
        if "P" in vals:
            pes = volt_to_pes(vals["P"]["V"])
            zona_risc = classify_pressure(vals["P"]["V"])
            row.update({
                "Pes (kg)": pes,
                "Risc": zona_risc
            })
        table.append(row)

    table_area.dataframe(table, hide_index=True)
    time.sleep(2)

