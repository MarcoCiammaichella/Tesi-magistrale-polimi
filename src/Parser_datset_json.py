import json
from pathlib import Path
from collections import defaultdict
class DatasetParser:
    def __init__(self,json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        images = data["images"]
        self.annotations = data["annotations"]
        categories = data["categories"]
        # pulizia images 
        images_parsed = {img["id"]: img for img in images}
        for i in images_parsed:
            del images_parsed[i]["license"]
            del images_parsed[i]["date_captured"]
            images_parsed[i]["file_name"]=images_parsed[i]["extra"]["name"]
            del images_parsed[i]["extra"]
        #id classe -> nome classe
        self.cat = {cat["id"]: cat["name"] for cat in categories}
        self.images_parsed = images_parsed

    def imgnametoann(self,file_name):
        """
        Prende in input il file_name (stringa) e ritorna
        tutte le bbox relative a quell'immagine in formato [x, y, w, h].
        """
        # 1) trova l'id dell'immagine a partire dal file_name
        image_id = None
        for img_id, img_info in self.images_parsed.items():
            if img_info["file_name"] == file_name:
                image_id = img_id
                break

        if image_id is None:
            # nessuna immagine con quel nome
            return []

        # 2) raccogli tutte le bbox delle annotazioni con quel image_id relative ad ogni tipo di bbox
        bboxes = defaultdict(list)
        for ann in self.annotations:
            if ann["image_id"] == image_id:
                bboxes[self.cat[ann["category_id"]]].append(ann["bbox"])
        return bboxes

    def imgidtoann(self,id):
        """
        Prende in input l'id della foto e ritorna
        tutte le bbox relative a quell'immagine in formato [x, y, w, h].
        """
        #raccogli tutte le bbox delle annotazioni con quel image_id relative ad ogni tipo di bbox
        bboxes = defaultdict(list)
        for ann in self.annotations:
            if ann["image_id"] == id:
                bboxes[self.cat[ann["category_id"]]].append(ann["bbox"])
        return bboxes

    def info(self):
        #semplicemente stampa la lista dei nomi delle immagini con i relativi id per facilitare la ricerca in imgnametoann se dovesse servire
        for info in list(self.images_parsed):
            print("id: ",self.images_parsed[info]["id"]," file_name: ",self.images_parsed[info]["file_name"])

    def get_dimensions(self,id):
        i=self.images_parsed.get(id)
        height = i["height"]
        width = i["width"]
        return(height,width)
    def getnamefromid(self,id):
        return(self.images_parsed[id]["file_name"])