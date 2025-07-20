
import matplotlib.pyplot as plt
from PIL import Image

#Obrim la imatge
image_path = "src/collar.png"
img = Image.open(image_path)

#Llista buida per guardar les coordenades
clicks = []


def onclick(event):
    if event.xdata and event.ydata:
        x, y = int(event.xdata), int(event.ydata)
        clicks.append((x, y))
        print(f"Clic {len(clicks)}: ({x}, {y})")
        #Si es fan dos clics, es mostra el rectangle definist per els dos punts
        if len(clicks) == 2:
            (x1, y1), (x2, y2) = clicks
            print(f"→ Rectangle: [{x1}, {y1}, {x2}, {y2}]\n")
            clicks.clear()  

#Es crea la finestra amb la imatge
fig, ax = plt.subplots(figsize=(10, 8))
ax.imshow(img)
ax.set_title("Fer dos clics per crear el rectangle")
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()