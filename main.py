import json
from pathlib import Path
import glob
import os
from src.Parser_datset_json import DatasetParser
from src.simmetria import simmetria_check
from src.shape import sky_mask_not_sky,is_rectangle_like

BASE_DIR = Path(__file__).resolve().parent
json_path = BASE_DIR / "data" / "_annotations.coco.json"
folder = BASE_DIR / "data" / "dataset_preprocessato_a_mano"
data=DatasetParser(json_path)
patterns = ["*.jpg", "*.jpeg", "*.png"]
image_paths = []
for p in patterns:
    image_paths.extend(glob.glob(os.path.join(folder, p)))
for path in image_paths:
    mask=sky_mask_not_sky(path)
    is_rect, score, verts,img = is_rectangle_like(mask, area_ratio_threshold=0.9)
    print(path, " :")
    print("Simile a rettangolo:", is_rect)

    

#for i in range(len(data.images_parsed)):
    #print(data.getnamefromid(i),simmetria_check(data,i))
    
#esempi di print per testare le funzioni
#print(data.imgidtoann(2))
#print(data.imgnametoann("IMG5417.jpeg")) 
#print(data.imgidtoann(3)["Windows"]) #ritorna tutte le bbox delle finestre nell'immagine con id 3
#print(data.imgnametoann("IMG5417.jpeg")) #ritorna tutte le bbox delle porte finestre nell'immagine "IMG5417.jpeg" 
#print(data.imgidtoann(1)["street_art"]) #test streetart presente
#print(data.imgidtoann(3)["street_art"]) #test streetart non presente
#print(data.info())