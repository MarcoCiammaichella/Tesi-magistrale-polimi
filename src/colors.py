import cv2
import numpy as np
from sklearn.cluster import KMeans

# Mappa dei colori
COLOR_MAP = {
    "Nero": (0, 0, 0), "Bianco": (255, 255, 255), "Grigio Scuro": (169, 169, 169),
    "Grigio": (128, 128, 128), "Rosso": (255, 0, 0), "Rosso Scuro": (139, 0, 0),
    "Verde": (0, 128, 0), "Verde Chiaro": (144, 238, 144), "Blu": (0, 0, 255),
    "Blu Navy": (0, 0, 128), "Azzurro": (135, 206, 235), "Giallo": (255, 255, 0),
    "Arancione": (255, 165, 0), "Viola": (128, 0, 128), "Rosa": (255, 192, 203),
    "Marrone": (165, 42, 42), "Beige": (245, 245, 220), "Oro": (255, 215, 0),
    "Crema": (255, 253, 208), "Marrone Scuro": (101, 67, 33), "Sabbia": (194, 178, 128)
}

#Mappa i colori che trova nell'immagine in base al dizionario definito sopra.
def get_color_name(requested_rgb):
    min_distance = float('inf')
    closest_name = "Unknown"
    r_c, g_c, b_c = requested_rgb
    for name, (r, g, b) in COLOR_MAP.items():
        distance = ((r_c - r) ** 2 + (g_c - g) ** 2 + (b_c - b) ** 2) ** 0.5
        if distance < min_distance:
            min_distance = distance
            closest_name = name
    return closest_name

def rgb_to_hex(color):
    return "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])

#Restituisce i k colori dominanti ordinati per percentuale di presenza.
def get_dominant_colors(image_path, k=3):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Ridimensionamento
    height, width, _ = img.shape
    new_width = 600
    if width > new_width:
        ratio = height / width
        new_height = int(new_width * ratio)
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    pixels = img.reshape(-1, 3)

    # Esecuzione di K-Means
    kmeans = KMeans(n_clusters=k, n_init=10)
    kmeans.fit(pixels)

    # Conta quante volte appare ogni etichetta, quanti pixel per ogni colore
    # labels_ contiene l'indice del cluster per ogni pixel
    unique_labels, counts = np.unique(kmeans.labels_, return_counts=True)

    # Ordina i conteggi in ordine decrescente (dal più frequente al meno frequente)
    # argsort restituisce gli indici che ordinerebbero l'array. [::-1] li inverte per decrescere.
    sorted_indices = np.argsort(counts)[::-1]

    total_pixels = pixels.shape[0]
    results = []

    # Prendiamo solo i primi 3 risultati (o k se k<3)
    top_n = min(3, len(sorted_indices))

    for i in range(top_n):
        index = sorted_indices[i]

        # Recuperiamo il colore dominante e il conteggio corrispondente
        center = kmeans.cluster_centers_[index]
        count = counts[index]

        # Calcolo percentuale
        percentage = (count / total_pixels) * 100

        color_rgb = tuple(center.round(0).astype(int))
        hex_val = rgb_to_hex(color_rgb)
        name_val = get_color_name(color_rgb)

        results.append({
            "name": name_val,
            "hex": hex_val,
            "rgb": color_rgb,
            "percentage": round(percentage, 1)  # Arrotondiamo a 1 decimale
        })

    return results