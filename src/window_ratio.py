def WindowToFacadeRatio(data,id):
    dimensions=data.get_dimensions(id)
    bbox=data.imgidtoann(id)
    area=0
    if bbox.get("Windows") is not None:
        for window in bbox.get("Windows"):
            area+=(window[2]*window[3])
    if bbox.get("window_door") is not None:
        for window_door in bbox.get("window_door"):
            area+=(window_door[2]*window[3])
    tot_dimension=dimensions[0]*dimensions[1]
    ratio =area/tot_dimension
    return ratio

def vertical_horizontal_lines(data,id):
    bbox=data.imgidtoann(id)
    i=0
    if bbox.get("Balconies") is None:
        return 0
    for balconies in bbox.get("Balconies"):
        i+=1
    if i < 2:
        return 0
    else:
        return 1 

def negozi(data,id):
    bbox=data.imgidtoann(id)
    if bbox.get("Shop") is None:
        return 0
    else :
        return 1

def street_art(data,id):
    bbox=data.imgidtoann(id)
    if bbox.get("street_art") is None:
        return 0
    else :
        return 1