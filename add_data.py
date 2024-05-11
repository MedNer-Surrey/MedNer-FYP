import pymongo
import time
import json

myclient = pymongo.MongoClient("mongodb+srv://admin:RXEOifMvCaD6HJHB@nerdata.2hcvguh.mongodb.net/")
mydb = myclient["NERData"]
mycl = mydb["simple"]

def get_data():
    with open('./annotations.json', 'r') as f:
        data = json.load(f)
    train_data = {'classes': data['classes'], 'annotations' : []}
    print(len(data['annotations']))
    for annot in data['annotations']:
        temp_data = {}
        t = time.localtime()
        temp_data['date'] = time.strftime("%d/%m/%Y %H:%M:%S", t)
        temp_data['text'] = annot[0]
        temp_data['entities'] = []
        for ent in annot[1]['entities']:
            start = ent[0]
            end = ent[1]
            label = ent[2].upper()
            temp_data['entities'].append((start,end,label))
        train_data['annotations'].append(temp_data)
    return train_data

data = get_data()
for obj in data['annotations']:
    mycl.update_one({}, {"$set": {"annotations": obj}})