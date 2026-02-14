import cv2
import numpy as np
from sklearn.cluster import KMeans

# Mappa dei colori
COLOR_MAP = {
    # --- BIANCHI E CHIARI (Fondamentali per intonaci e luci) ---
    "Bianco Assoluto": (255, 255, 255),
    "Panna": (255, 253, 208),
    "Avorio": (255, 255, 240),
    "Bianco Antico": (250, 235, 215),
    "Beige Chiaro": (245, 245, 220),
    "Perla": (234, 230, 202),
    "Ghiaccio": (240, 248, 255),

    # --- GRIGI E NERI (Asfalto, Cemento, Ombre, Tetti) ---
    "Nero": (0, 0, 0),
    "Nero Carbone": (20, 20, 20),
    "Grigio Antracite": (41, 49, 51),  # Molto comune per infissi moderni
    "Grigio Scuro": (105, 105, 105),
    "Grigio Cemento": (128, 128, 128),
    "Grigio Argento": (192, 192, 192),
    "Grigio Perla": (211, 211, 211),
    "Grigio Ardesia (Bluastro)": (112, 128, 144), # Tetti, asfalto bagnato
    "Grigio Topo": (100, 107, 99),
    "Tortora": (176, 166, 149), # Colore RE dell'architettura moderna

    # --- MARRONI E TERRE (Mattoni, Legno, Terreno) ---
    "Marrone Scuro": (101, 67, 33),
    "Cioccolato": (139, 69, 19),
    "Marrone": (165, 42, 42),
    "Terra di Siena": (160, 82, 45), # Classico italiano
    "Ruggine": (183, 65, 14),
    "Mattone": (178, 34, 34),       # Fondamentale per le facciate
    "Terracotta": (226, 114, 91),
    "Bronzo": (205, 127, 50),
    "Sabbia": (194, 178, 128),
    "Kaki": (240, 230, 140),
    "Cammello": (193, 154, 107),

    # --- ROSSI E ROSA ---
    "Rosso": (255, 0, 0),
    "Rosso Scuro": (139, 0, 0),
    "Bordeaux": (128, 0, 32),
    "Rosso Veneziano": (200, 8, 21),
    "Corallo": (255, 127, 80),
    "Rosa": (255, 192, 203),
    "Rosa Antico": (212, 115, 129), # Facciate storiche
    "Fucsia": (255, 0, 255),
    "Pesca": (255, 218, 185),

    # --- GIALLE E ARANCIONI ---
    "Arancione": (255, 165, 0),
    "Arancio Scuro": (255, 140, 0),
    "Giallo": (255, 255, 0),
    "Oro": (255, 215, 0),
    "Ocra": (204, 119, 34),       # Facciate Milano/Roma
    "Giallo Napoli": (247, 232, 159),
    "Senape": (255, 219, 88),

    # --- VERDI (Vegetazione) ---
    "Verde": (0, 128, 0),
    "Verde Scuro (Foresta)": (34, 139, 34),
    "Verde Pino": (1, 121, 111),
    "Verde Prato": (124, 252, 0),
    "Verde Oliva": (128, 128, 0),
    "Verde Militare": (85, 107, 47),
    "Verde Acqua": (102, 205, 170),
    "Verde Smeraldo": (80, 200, 120),
    "Verde Salvia": (158, 169, 147), # Molto comune negli infissi

    # --- BLU E CIELO ---
    "Blu": (0, 0, 255),
    "Blu Notte": (25, 25, 112),
    "Blu Navy": (0, 0, 128),
    "Blu Reale": (65, 105, 225),
    "Zaffiro": (15, 82, 186),
    "Azzurro": (135, 206, 235),
    "Celeste": (178, 255, 255),
    "Turchese": (64, 224, 208),
    "Ciano": (0, 255, 255),
    "Petrolio": (0, 95, 106),
    "Indaco": (75, 0, 130),

    # --- VIOLA ---
    "Viola": (128, 0, 128),
    "Lilla": (200, 162, 200),
    "Lavanda": (230, 230, 250),
    "Melanzana": (153, 17, 153)
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
def get_dominant_colors(img, k=3):
    #img = cv2.imread(image_path)
    #if img is None:
    #    raise FileNotFoundError(f"Image not found: {image_path}")

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
        percentage = (count / total_pixels) 

        color_rgb = tuple(center.round(0).astype(int))
        hex_val = rgb_to_hex(color_rgb)
        name_val = get_color_name(color_rgb)

        results.append(round(percentage, 1))  # Arrotondiamo a 1 decimale)
    
    return (results[0]+0.25*results[1])
