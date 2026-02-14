import json
from pathlib import Path
import glob
import os
import cv2
from src.Parser_datset_json import DatasetParser
from src.simmetria import simmetria_check
from src.prospettiva import Prospettiva
from src.window_ratio import WindowToFacadeRatio,vertical_horizontal_lines,negozi,street_art
from src.shape import is_rectangle_like
from src.colors import get_dominant_colors

# --- CONFIGURAZIONE PERCORSI ---
BASE_DIR = Path(__file__).resolve().parent
json_path = BASE_DIR / "data" / "_annotations.coco.json"
folder = BASE_DIR / "data" / "dataset_ridotto"
data=DatasetParser(json_path)
patterns = ["*.jpg", "*.jpeg", "*.png"]
image_paths = []

def get_image_paths():
    patterns = ["*.jpg", "*.jpeg", "*.png"]
    image_paths = []
    for p in patterns:
        image_paths.extend(glob.glob(os.path.join(folder, p)))
    return image_paths

def b7(id,img_corrected):
    rect=is_rectangle_like(img_corrected)
    simmetria=simmetria_check(data,id)
    wtf=WindowToFacadeRatio(data,id)
    vhl=vertical_horizontal_lines(data,id)
    T=negozi(data,id)
    N=street_art(data,id)
    O=0.5*simmetria+0.5*int(rect)
    C=0.2*vhl+0.8*wtf
    VisR=0.3*O+0.2*C+0.3*T+0.2*N
    return(VisR)
    
def b11(img_corrected):
    rect=is_rectangle_like(img_corrected)
    colors=get_dominant_colors(img_corrected)
    res=0.5*rect+0.5*colors
    return(res)
if __name__ == "__main__":
    print("Inserisci l'id dell'immagine che vuoi analizzare:")
    id=int(input())
    im=data.getnamefromid(id)
    path_img=folder / im
    img_corrected=Prospettiva(path_img)
    res1=b7(id,img_corrected)
    res2=b11(img_corrected)
    b10=((res1+res2)/2)*100
    print(b10)
    # riconoscmento forme
    #job_shapes()

    #riconoscimento colori
    #job_colors()