from src.Parser_datset_json import DatasetParser
#window[0] = x orizzontale punto in alto a sinistra ,window[1] y verticale punto in alto a sinistra,window[2] larghezza,window[3] altezza
def simmetria_check(data,id):
    asse_simmetria_glob_x=data.get_dimensions(id)[1]/2
    bbox=data.imgidtoann(id)
    tolleranza=100
    results=[]
    results.append(simmetria_finestre_x(bbox,tolleranza))
    results.append(simmetria_finestre_y(bbox,tolleranza))
    results.append(simmetria_balconi_x(bbox,tolleranza))
    results.append(simmetria_balconi_y(bbox,tolleranza))
    results.append(simmetria_porta_finestra_x(bbox,tolleranza))
    results.append(simmetria_porta_finestra_y(bbox,tolleranza))
    if simmetria_finestre_x(bbox,tolleranza)==1 and simmetria_balconi_x(bbox,tolleranza)==1 and simmetria_porta_finestra_x(bbox,tolleranza):
        results.append(simmetria_assoluta_x(asse_simmetria_glob_x,bbox,tolleranza))
    else: results.append(0)
    return(results)

def simmetria_finestre_x(bbox,tolleranza):
    if bbox.get("Windows") is None:
        return 0
    left_bound=min(x[0] for x in bbox.get("Windows"))
    riga_max = max(bbox.get("Windows"), key=lambda x: x[0])
    right_bound=riga_max[0]+riga_max[2]
    asse_simmetria_x=int((left_bound+right_bound)/2)
    matches=0
    finestre=[]
    for window in bbox.get("Windows"):
        if window[0]<asse_simmetria_x and window[0] + window [2] > asse_simmetria_x:
            continue
        finestre.append(window)
    finestre_sx = [(fx, fy,lar,lun) for (fx, fy,lar,lun) in finestre if fx < asse_simmetria_x]
    for (fx,fy,lar,lun) in finestre_sx:
        x_speculare= (asse_simmetria_x*2)-(fx+lar)
        for (fx2,fy2,lar2,lun2) in finestre:
            if abs(fx2 - x_speculare) <= tolleranza and abs(fy2 - fy) <= tolleranza:
                matches+=1
    if matches==len(finestre_sx) and matches==len(finestre)-len(finestre_sx):
        return(1)
    return(0)

def simmetria_finestre_y(bbox,tolleranza):
    if bbox.get("Windows") is None:
        return 0
    high_bound=min(y[1] for y in bbox.get("Windows"))
    riga_min = max(bbox.get("Windows"), key=lambda x: x[1])
    low_bound=riga_min[1]+riga_min[3]
    asse_simmetria_y=int((high_bound+low_bound)/2)
    matches=0
    finestre=[]
    for window in bbox.get("Windows"):
        if window[1]<asse_simmetria_y and window[1] + window [3] > asse_simmetria_y:
            continue
        finestre.append(window)
    finestre_up = [(fx, fy,lar,lun) for (fx, fy,lar,lun) in finestre if fy < asse_simmetria_y]
    for (fx,fy,lar,lun) in finestre_up:
        y_speculare= (asse_simmetria_y*2)-(fy+lun)
        for (fx2,fy2,lar2,lun2) in finestre:
            if abs(fy2 - y_speculare) <= tolleranza and abs(fx2 - fx) <= tolleranza:
                matches+=1
    if matches==len(finestre_up)and matches==len(finestre)-len(finestre_up):
        return(1)
    return(0)

def simmetria_balconi_x(bbox,tolleranza):
    if bbox.get("Balconies") is None:
        return 0
    left_bound=min(x[0] for x in bbox.get("Balconies"))
    riga_max = max(bbox.get("Balconies"), key=lambda x: x[0])
    right_bound=riga_max[0]+riga_max[2]
    asse_simmetria_x=int((left_bound+right_bound)/2)
    matches=0
    balconi=[]
    for bal in bbox.get("Balconies"):
        if bal[0]<asse_simmetria_x and bal[0] + bal [2] > asse_simmetria_x:
            continue
        balconi.append(bal)
    balconi_sx = [(fx, fy,lar,lun) for (fx, fy,lar,lun) in balconi if fx < asse_simmetria_x]
    for (fx,fy,lar,lun) in balconi_sx:
        x_speculare= (asse_simmetria_x*2)-(fx+lar)
        for (fx2,fy2,lar2,lun2) in balconi:
            if abs(fx2 - x_speculare) <= tolleranza and abs(fy2 - fy) <= tolleranza:
                matches+=1
    if matches==len(balconi_sx)and matches==len(balconi)-len(balconi_sx):
        return(1)
    return(0)

def simmetria_balconi_y(bbox,tolleranza):
    tolleranza+=100
    if bbox.get("Balconies") is None:
        return 0
    high_bound=min(y[1] for y in bbox.get("Balconies"))
    riga_min = max(bbox.get("Balconies"), key=lambda x: x[1])
    low_bound=riga_min[1]+riga_min[3]
    asse_simmetria_y=int((high_bound+low_bound)/2)
    matches=0
    balconi=[]
    altezza_normalizzata=min(y[3] for y in bbox.get("Balconies"))
    for bal in bbox.get("Balconies"):
        if bal[1]<asse_simmetria_y and bal[1] + bal [3] > asse_simmetria_y:
            continue
        bal[1]=(bal[1]+(bal[1]+bal[3]))/2
        bal[1]-=altezza_normalizzata/2
        balconi.append(bal)
    balconi_up = [(fx, fy,lar,altezza_normalizzata) for (fx, fy,lar,altezza_normalizzata) in balconi if fy < asse_simmetria_y]
    for (fx,fy,lar,altezza_normalizzata) in balconi_up:
        y_speculare= (asse_simmetria_y*2)-(fy+altezza_normalizzata)
        for (fx2,fy2,lar2,lun2) in balconi:
            if abs(fy2 - y_speculare) <= tolleranza and abs(fx2 - fx) <= tolleranza:
                matches+=1
    if matches==len(balconi_up)and matches==len(balconi)-len(balconi_up):
        return(1)
    return(0)

def simmetria_porta_finestra_x(bbox,tolleranza):
    if bbox.get("window_door") is None:
        return 0
    left_bound=min(x[0] for x in bbox.get("window_door"))
    riga_max = max(bbox.get("window_door"), key=lambda x: x[0])
    right_bound=riga_max[0]+riga_max[2]
    asse_simmetria_x=int((left_bound+right_bound)/2)
    matches=0
    porta_finestra=[]
    for port_fin in bbox.get("window_door"):
        if port_fin[0]<asse_simmetria_x and port_fin[0] + port_fin [2] > asse_simmetria_x:
            continue
        porta_finestra.append(port_fin)
    porta_finestra_sx = [(fx, fy,lar,lun) for (fx, fy,lar,lun) in porta_finestra if fx < asse_simmetria_x]
    for (fx,fy,lar,lun) in porta_finestra_sx:
        x_speculare= (asse_simmetria_x*2)-(fx+lar)
        for (fx2,fy2,lar2,lun2) in porta_finestra:
            if abs(fx2 - x_speculare) <= tolleranza and abs(fy2 - fy) <= tolleranza:
                matches+=1
    if matches==len(porta_finestra_sx)and matches==len(porta_finestra)-len(porta_finestra_sx):
        return(1)
    return(0)

def simmetria_porta_finestra_y(bbox,tolleranza):
    if bbox.get("window_door") is None:
        return 0
    high_bound=min(y[1] for y in bbox.get("window_door"))
    riga_min = max(bbox.get("window_door"), key=lambda x: x[1])
    low_bound=riga_min[1]+riga_min[3]
    asse_simmetria_y=int((high_bound+low_bound)/2)
    matches=0
    porta_finestra=[]
    for port_fin in bbox.get("window_door"):
        if port_fin[1]<asse_simmetria_y and port_fin[1] + port_fin [3] > asse_simmetria_y:
            continue
        porta_finestra.append(port_fin)
    porta_finestra_up = [(fx, fy,lar,lun) for (fx, fy,lar,lun) in porta_finestra if fy < asse_simmetria_y]
    for (fx,fy,lar,lun) in porta_finestra_up:
        y_speculare= (asse_simmetria_y*2)-(fy+lun)
        for (fx2,fy2,lar2,lun2) in porta_finestra:
            if abs(fy2 - y_speculare) <= tolleranza and abs(fx2 - fx) <= tolleranza:
                matches+=1
    if matches==len(porta_finestra_up)and matches==len(porta_finestra)-len(porta_finestra_up):
        return(1)
    return(0)

def simmetria_assoluta_x(asse,bbox,tolleranza):
    matchesw=0
    matchesb=0
    matcheswd=0
    finestre=[]
    balconi=[]
    porta_finestra=[]
    for window in bbox.get("Windows"):
        if window[0]<asse and window[0] + window [2] > asse:
            continue
        finestre.append(window)
    finestre_sx = [(fx, fy,lar,lun) for (fx, fy,lar,lun) in finestre if fx < asse]
    for (fx,fy,lar,lun) in finestre_sx:
        x_speculare= (asse*2)-(fx+lar)
        for (fx2,fy2,lar2,lun2) in finestre:
            if abs(fx2 - x_speculare) <= tolleranza and abs(fy2 - fy) <= tolleranza:
                matchesw+=1
    if matchesw!=len(finestre_sx) or matchesw!=len(finestre)-len(finestre_sx):
        return(0)
    for bal in bbox.get("Balconies"):
        if bal[0]<asse and bal[0] + bal [2] > asse:
            continue
        balconi.append(bal)
    balconi_sx = [(fx, fy,lar,lun) for (fx, fy,lar,lun) in balconi if fx < asse]
    for (fx,fy,lar,lun) in balconi_sx:
        x_speculare= (asse*2)-(fx+lar)
        for (fx2,fy2,lar2,lun2) in balconi:
            if abs(fx2 - x_speculare) <= tolleranza and abs(fy2 - fy) <= tolleranza:
                matchesb+=1
    if matchesb!=len(balconi_sx) or matchesb!=len(balconi)-len(balconi_sx):
        return(0)
    for port_fin in bbox.get("window_door"):
        if port_fin[0]<asse and port_fin[0] + port_fin [2] > asse:
            continue
        porta_finestra.append(port_fin)
    porta_finestra_sx = [(fx, fy,lar,lun) for (fx, fy,lar,lun) in porta_finestra if fx < asse]
    for (fx,fy,lar,lun) in porta_finestra_sx:
        x_speculare= (asse*2)-(fx+lar)
        for (fx2,fy2,lar2,lun2) in porta_finestra:
            if abs(fx2 - x_speculare) <= tolleranza and abs(fy2 - fy) <= tolleranza:
                matcheswd+=1
    if matcheswd!=len(porta_finestra_sx) or matcheswd!=len(porta_finestra)-len(porta_finestra_sx):
        return(0)
    return(1)