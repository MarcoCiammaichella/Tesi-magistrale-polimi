import json
from pathlib import Path
from src.Parser_datset_json import DatasetParser

BASE_DIR = Path(__file__).resolve().parent
json_path = BASE_DIR / "data" / "_annotations.coco.json"

data=DatasetParser(json_path)

#esempi di print per testare le funzioni
#print(data.imgidtoann(2))
#print(data.imgnametoann("IMG5417.jpeg")) 
#print(data.imgidtoann(3)["Windows"]) #ritorna tutte le bbox delle finestre nell'immagine con id 3
#print(data.imgnametoann("IMG5417.jpeg")["window_door"]) #ritorna tutte le bbox delle porte finestre nell'immagine "IMG5417.jpeg" 
#print(data.imgidtoann(1)["street_art"]) #test streetart presente
#print(data.imgidtoann(3)["street_art"]) #test streetart non presente
