import cv2
import numpy as np
from pathlib import Path

def is_rectangle_like(img, area_ratio_threshold=0.9, debug=False):
    # mask: immagine binaria 0/255 con zona di interesse in bianco
    mask_rosso = np.all(img == [0, 0, 255], axis=2).astype(np.uint8) * 255
    mask = cv2.bitwise_not(mask_rosso)

    # 1. Trova contorni
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
