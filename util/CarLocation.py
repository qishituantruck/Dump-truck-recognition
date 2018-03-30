
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
def getproperplatenum(res_set):
    propernum=''
    dividenumscore=res_set[0][1]
    e2enumscore=res_set[0][5]
    if dividenumscore>e2enumscore:
        propernum=res_set[0][0]
    else:
        propernum=res_set[0][4]
    return propernum