import json
from pathlib import Path
from collections import defaultdict
#percorso file json
BASE_DIR = Path(__file__).resolve().parent
json_path = BASE_DIR / "data" / "_annotations.coco.json"

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

images = data["images"]
annotations = data["annotations"]
categories = data["categories"]
# pulizia images 
images_parsed = {img["id"]: img for img in images}
for i in images_parsed:
    del images_parsed[i]["license"]
    del images_parsed[i]["date_captured"]
    images_parsed[i]["file_name"]=images_parsed[i]["extra"]["name"]
    del images_parsed[i]["extra"]
#id classe -> nome classe
cat = {cat["id"]: cat["name"] for cat in categories}

def imgnametoann(file_name):
    """
    Prende in input il file_name (stringa) e ritorna
    tutte le bbox relative a quell'immagine in formato [x, y, w, h].
    """
    # 1) trova l'id dell'immagine a partire dal file_name
    image_id = None
    for img_id, img_info in images_parsed.items():
        if img_info["file_name"] == file_name:
            image_id = img_id
            break

    if image_id is None:
        # nessuna immagine con quel nome
        return []

    # 2) raccogli tutte le bbox delle annotazioni con quel image_id relative ad ogni tipo di bbox
    bboxes = defaultdict(list)
    for ann in annotations:
        if ann["image_id"] == image_id:
            bboxes[cat[ann["category_id"]]].append(ann["bbox"])
    return bboxes

def imgidtoann(id):
    """
    Prende in input l'id della foto e ritorna
    tutte le bbox relative a quell'immagine in formato [x, y, w, h].
    """
    #raccogli tutte le bbox delle annotazioni con quel image_id relative ad ogni tipo di bbox
    bboxes = defaultdict(list)
    for ann in annotations:
        if ann["image_id"] == id:
            bboxes[cat[ann["category_id"]]].append(ann["bbox"])
    return bboxes

def info():
    #semplicemente stampa la lista dei nomi delle immagini con i relativi id per facilitare la ricerca in imgnametoann se dovesse servire
    for info in list(images_parsed):
        print("id: ",images_parsed[info]["id"]," file_name: ", images_parsed[info]["file_name"])
#info()
#esempi di print per testare le funzioni
print(imgidtoann(2))
#print(imgnametoann("IMG5417.jpeg")) 
#print(imgidtoann(3)["Windows"]) #ritorna tutte le bbox delle finestre nell'immagine con id 3
#print(imgnametoann("IMG5417.jpeg")["window_door"]) #ritorna tutte le bbox delle porte finestre nell'immagine "IMG5417.jpeg" 
#print(imgidtoann(1)["street_art"]) #test streetart presente
#print(imgidtoann(3)["street_art"]) #test streetart non presente