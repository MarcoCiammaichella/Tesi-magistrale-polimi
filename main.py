import json
from pathlib import Path
import glob
import os
import matplotlib.pyplot as plt
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
    colors, distanza = get_dominant_colors(img_corrected)
    color_var = 0
    if distanza <= 150:
        color_var = 1
    print(distanza)
    rect=is_rectangle_like(img_corrected)
    #print('Is rectangle like?', rect)
    simmetria=simmetria_check(data,id)
    #print('Overall symmetry value for the building:', round(simmetria,0))
    wtf=WindowToFacadeRatio(data,id)
    #print('Windows to facade ratio:', round(wtf*100,2))
    vhl=vertical_horizontal_lines(data,id)
    #print('Vertical and horizontal lines presence:', round(vhl,2))
    T=negozi(data,id)
    #print('Presence of commercial activities:', T)
    N=street_art(data,id)
    #print('Presence of street art:', N)
    O=0.5*simmetria+0.5*int(rect)
    C=0.2*vhl+0.6*wtf+0.2*color_var
    VisR=0.3*O+0.2*C+0.3*T+0.2*N
    #print('VisR value:', round(VisR+100,2))
    return(VisR)
    
def b11(img_corrected):
    rect=is_rectangle_like(img_corrected)
    colors,distanza=get_dominant_colors(img_corrected)
    res=0.5*rect+0.5*colors
    return(res)

def plot_performance_gauge(valore):
    # Configurazione dei limiti e colori (basati sulla tua immagine)
    thresholds = [20, 30, 20, 30]  # Ampiezza delle sezioni: 0-20, 20-50, 50-70, 70-100
    colors = ['#e74c3c', '#f1c40f', '#a2d149', '#5a823f'] # Rosso, Giallo, Verde chiaro, Verde scuro
    labels = ['Low', 'Acceptable', 'Good', 'Excellent']

    fig, ax = plt.subplots(figsize=(10, 2))

    # 1. Disegna le sezioni colorate sullo sfondo
    left = 0
    for i in range(len(thresholds)):
        ax.barh(0, thresholds[i], left=left, color=colors[i], height=0.5)
        # Aggiungi il testo al centro di ogni sezione
        ax.text(left + thresholds[i]/2, 0, labels[i], 
                ha='center', va='center', fontsize=12, fontweight='bold')
        left += thresholds[i]

    # 2. Aggiungi l'indicatore per il valore attuale
    ax.axvline(valore, color='black', linewidth=3)
    ax.plot(valore, 0, 'ko', markersize=10) # Un punto nero per renderlo più visibile

    # 3. Formattazione estetica
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.5, 0.5)
    ax.set_yticks([]) # Rimuove l'asse Y
    ax.set_xticks([0, 20, 50, 70, 100])
    ax.set_title(f"Performance Score: {valore}", pad=20)

    # Rimuovi i bordi del grafico per pulizia
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    print("Inserisci l'id dell'immagine che vuoi analizzare:")
    id=int(input())
    im=data.getnamefromid(id)
    path_img=folder / im
    img_corrected=Prospettiva(path_img)
    res1=b7(id,img_corrected)
    res2=b11(img_corrected)
    b10=((res1+res2)/2)*100
    plot_performance_gauge(b10)
    # riconoscmento forme
    #job_shapes()

    #riconoscimento colori
    #job_colors()
