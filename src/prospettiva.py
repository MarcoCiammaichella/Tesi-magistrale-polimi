import cv2
import numpy as np
import matplotlib.pyplot as plt

def Correggi_prospettiva(path_img, out_width=None, out_height=None):
    img = cv2.imread(path_img)
    if img is None:
        raise ValueError("Immagine non trovata")
    h, w = img.shape[:2]
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 1) selezione punti
    plt.imshow(img_rgb)
    plt.title("Clicca 4 punti sul piano (in ordine logico)")
    pts = plt.ginput(4,timeout=-1)
    plt.close()

    src = np.float32(pts)

    # se vuoi ancora che quei 4 punti siano i corner di un rettangolo di riferimento
    if out_width is None or out_height is None:
        # scegli dimensioni proporzionali alla distanza tra i punti cliccati
        w_est = np.linalg.norm(src[0] - src[1])
        h_est = np.linalg.norm(src[0] - src[3])
        out_width = int(w_est)
        out_height = int(h_est)

    dst = np.float32([
        [0, 0],
        [out_width - 1, 0],
        [out_width - 1, out_height - 1],
        [0, out_height - 1]
    ])

    # 2) omografia piano -> rettangolo
    M = cv2.getPerspectiveTransform(src, dst)

    # 3) applica M ai 4 angoli DELL'IMMAGINE INTERA
    corners = np.float32([[0, 0],
                          [w - 1, 0],
                          [w - 1, h - 1],
                          [0, h - 1]]).reshape(-1, 1, 2)
    warped_corners = cv2.perspectiveTransform(corners, M).reshape(-1, 2)

    x_min, y_min = warped_corners.min(axis=0)
    x_max, y_max = warped_corners.max(axis=0)

    new_w = int(np.ceil(x_max - x_min))
    new_h = int(np.ceil(y_max - y_min))

    # 4) traslazione per evitare coordinate negative
    T = np.array([[1, 0, -x_min],
                  [0, 1, -y_min],
                  [0, 0, 1]], dtype=np.float32)

    H = T @ M

    warped_full = cv2.warpPerspective(img, H, (new_w, new_h))
    return warped_full

def seleziona_poligono(img_bgr, window_name="Seleziona poligono"):
    img = img_bgr.copy()
    preview = img.copy()

    points = []   # lista di vertici cliccati, nell'ordine
    radius = 3

    def redraw():
        nonlocal preview
        preview = img.copy()
        # disegna poligono corrente
        for i, p in enumerate(points):
            cv2.circle(preview, p, radius, (0, 0, 255), -1)
            if i > 0:
                cv2.line(preview, points[i-1], p, (0, 255, 0), 2)

    def mouse_cb(event, x, y, flags, param):
        nonlocal img, preview, points
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))
            redraw()

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window_name, mouse_cb)

    while True:
        cv2.imshow(window_name, preview)
        key = cv2.waitKey(30) & 0xFF

        if key == 13:  # ENTER
            break
        elif key == 8:  # BACKSPACE
            if points:
                points.pop()
                redraw()
        elif key == 27:  # ESC
            points = []
            break

    cv2.destroyWindow(window_name)

    if len(points) < 3:
        raise RuntimeError("Servono almeno 3 punti per un poligono")

    pts = np.array(points, dtype=np.int32)
    return pts

def Maschera_poligono(img_bgr):
    pts = seleziona_poligono(img_bgr)

    h, w = img_bgr.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.fillPoly(mask, [pts], 1)

    x1 = np.min(pts[:, 0])
    x2 = np.max(pts[:, 0])
    y1 = np.min(pts[:, 1])
    y2 = np.max(pts[:, 1])

    img_crop = img_bgr[y1:y2, x1:x2]
    mask_crop = mask[y1:y2, x1:x2]

    red_bg = np.zeros_like(img_crop)
    red_bg[:] = (0, 0, 255)

    mask3 = mask_crop[:, :, None]
    out = img_crop * mask3 + red_bg * (1 - mask3)

    return out

if __name__ == "__main__":
    path =  "C:/Users/marco/OneDrive/Desktop/dataset palazzi/IMG_8148.jpg"
    warped=Correggi_prospettiva(path)
    test=Maschera_poligono(warped)
    cv2.imwrite("test.png", test)
    cv2.imwrite("warped.png", warped)