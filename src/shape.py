import cv2
import numpy as np
from pathlib import Path


def sky_mask_not_sky(image_path, debug=False):
    # 1. Leggi immagine
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Immagine non trovata")

    # 2. Converti in HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 3. Range di cielo (da tarare sul tuo dataset)
    #   - H: circa azzurro/blu chiaro
    #   - S: almeno un po' saturo
    #   - V: abbastanza chiaro
    lower_sky = np.array([85, 20, 120], dtype=np.uint8)
    upper_sky = np.array([140, 255, 255], dtype=np.uint8)
    mask_sky = cv2.inRange(hsv, lower_sky, upper_sky)
    #lower_cloud = np.array([0,   0,  180])   # H qualsiasi, S molto bassa, V alta
    #upper_cloud = np.array([179, 40, 255])
    #mask_cloud = cv2.inRange(hsv, lower_cloud, upper_cloud) 

    #mask_sky = cv2.bitwise_or(blue_mask, mask_cloud)

# pulizia: togli rumore piccolo
    kernel = np.ones((5, 5), np.uint8)
    mask_sky = cv2.morphologyEx(mask_sky, cv2.MORPH_OPEN, kernel, iterations=1)
    mask_sky = cv2.morphologyEx(mask_sky, cv2.MORPH_CLOSE, kernel, iterations=1)
    h, w = mask_sky.shape
# tieni solo la parte alta come cielo (es. sopra il 60% dell'immagine)
    row_cut = int(0.5 * h)
    mask_sky[row_cut:h, :] = 0


    # 6. Maschera NON cielo (quello che ti serve)
    not_sky_mask = cv2.bitwise_not(mask_sky)
    kernel_big = np.ones((35, 35), np.uint8)
    building = cv2.morphologyEx(not_sky_mask, cv2.MORPH_CLOSE, kernel_big, iterations=2)

    if debug:
        #cv2.imwrite("debug_sky.png", blue_mask)
        #cv2.imwrite("debug_clouds.png", mask_cloud)
        cv2.imwrite("debug_sky_all.png", mask_sky)

    return building

def is_rectangle_like(mask, area_ratio_threshold=0.9, debug=False):
    # mask: immagine binaria 0/255 con zona di interesse in bianco

    # 1. Trova contorni
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return False, 0.0, 0, None

    # 2. Prendi il contorno con area massima
    cnt = max(contours, key=cv2.contourArea)

    contour_area = cv2.contourArea(cnt)
    x, y, w, h = cv2.boundingRect(cnt)  # rettangolo allineato agli assi
    rect_area = w * h if w > 0 and h > 0 else 1

    # 3. Rectangularity (extent)
    area_ratio = contour_area / rect_area  # in [0, 1] in genere [web:49][web:54]

    # 4. Controllo numero vertici (opzionale ma utile)
    epsilon = 0.01 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)  # poligono approssimato [web:44][web:55]
    num_vertices = len(approx)

    is_rect_like = (area_ratio >= area_ratio_threshold) and (3 <= num_vertices <= 6)

    debug_img = None
    if debug:
        debug_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(debug_img, [cnt], -1, (0, 255, 0), 2)
        cv2.rectangle(debug_img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imwrite("debug_mask_rect.png", debug_img)

    return is_rect_like, area_ratio, num_vertices, debug_img


# Esempio d'uso
if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent
    path =  "C:/Users/marco/OneDrive/Desktop/tesi_github/data/dataset_preprocessato_a_mano/IMG_8148.jpg"
    test = sky_mask_not_sky(path,debug=True)
    is_rect, score, verts,img = is_rectangle_like(test, area_ratio_threshold=0.9, debug=True)
    print("Simile a rettangolo:", is_rect)
    print("Score (area_ratio):", score)
    print("vertici :",verts)
