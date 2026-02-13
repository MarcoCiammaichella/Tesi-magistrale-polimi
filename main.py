import json
from pathlib import Path
import glob
import os
import cv2
from src.Parser_datset_json import DatasetParser
from src.window_ratio import WindowToFacadeRatio,vertical_horizontal_lines
from src.shape import is_rectangle_like
from src.colors import get_dominant_colors

# --- CONFIGURAZIONE PERCORSI ---
BASE_DIR = Path(__file__).resolve().parent
json_path = BASE_DIR / "data" / "_annotations.coco.json"
folder = BASE_DIR / "data" / "dataset_preprocessato_a_mano"
data=DatasetParser(json_path)
patterns = ["*.jpg", "*.jpeg", "*.png"]
image_paths = []
test=WindowToFacadeRatio(data,7)
test2=vertical_horizontal_lines(data,2)

def get_image_paths():
    patterns = ["*.jpg", "*.jpeg", "*.png"]
    image_paths = []
    for p in patterns:
        image_paths.extend(glob.glob(os.path.join(folder, p)))
    return image_paths

# --- JOB 1: RICONOSCIMENTO FORMA ---
def job_shapes():
    print("--- AVVIO ANALISI FORME ---")

    # Inizializza il parser solo se serve
    # data = DatasetParser(json_path)

    image_paths = get_image_paths()

    if not image_paths:
        print("Nessuna immagine trovata.")
        return

    for path in image_paths:
        # 1. Carica l'immagine dal percorso
        img_originale = cv2.imread(path)

        # Controllo di sicurezza: se l'immagine è corrotta o il percorso è sbagliato
        if img_originale is None:
            print(f"Errore: Impossibile caricare {path}")
            continue

        # 2. Chiama la funzione UNA sola volta
        # La funzione restituisce 4 valori, dobbiamo prenderli tutti
        is_rect, score, verts, debug_img = is_rectangle_like(img_originale, area_ratio_threshold=0.9)

        # 3. Stampa i risultati
        print(f"\nFile: {os.path.basename(path)}")
        print(f" -> È un rettangolo? {is_rect}")
        print(f" -> Punteggio (Ratio): {score:.2f}")  # Arrotondamento a 2 decimali
        print(f" -> Numero vertici: {verts}")

# --- JOB 2: RICONOSCIMENTO COLORI ---
def job_colors():
    print("--- AVVIO ANALISI COLORI ---")

    image_paths = get_image_paths()

    if not image_paths:
        print(f"Nessuna immagine trovata in: {folder}")
        return

    for path in image_paths:
        print(f"\nAnalisi file: {os.path.basename(path)}")
        try:
            palette = get_dominant_colors(path, k=3)

            print("Top 3 Colori dominanti:")
            for item in palette:
                # Stampa del colore, percentuale e codice RGB
                print(f"  -> {item['percentage']}% : {item['name']} ({item['hex']})")

        except Exception as e:
            print(f"Errore su questa immagine: {e}")

if __name__ == "__main__":
    # riconoscmento forme
    job_shapes()

    #riconoscimento colori
    job_colors()