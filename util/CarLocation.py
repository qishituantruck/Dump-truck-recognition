

def getCarLoc(result):
    carnum=0
    carLocList=[]
    if len(result)==0:
        return  0,carLocList
    for item in result:
        if item["label"]=="car":
            carnum+=1
            dict={}
            dict["topleft"]=(item["topleft"]["x"],item["topleft"]["y"])
            dict["bottomright"] = (item["bottomright"]["x"], item["bottomright"]["y"])
            carLocList.append(dict)
    return carnum,carLocList