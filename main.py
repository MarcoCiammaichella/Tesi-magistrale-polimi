import json
from pathlib import Path
import glob
import os
from src.Parser_datset_json import DatasetParser
from src.simmetria import simmetria_check
from src.shape import sky_mask_not_sky, is_rectangle_like
from src.colors import get_dominant_colors, rgb_to_hex

# --- CONFIGURAZIONE PERCORSI ---
BASE_DIR = Path(__file__).resolve().parent
json_path = BASE_DIR / "data" / "_annotations.coco.json"
folder = BASE_DIR / "data" / "dataset_preprocessato_a_mano"

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
    data = DatasetParser(json_path)

    image_paths = get_image_paths()

    for path in image_paths:
        mask = sky_mask_not_sky(path)
        is_rect, score, verts, img = is_rectangle_like(mask, area_ratio_threshold=0.9)
        print(path, " :")
        print("Simile a rettangolo:", is_rect)

    # for i in range(len(data.images_parsed)):
    #     print(data.getnamefromid(i),simmetria_check(data,i))


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
    #riconoscimento colori
    job_colors()

    #riconoscmento forme
    #job_shapes()