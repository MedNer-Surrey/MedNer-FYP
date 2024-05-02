import pymongo
import json
from tqdm import tqdm
import time
from ast import literal_eval
import re

def get_data_maccro():
    train_data = {'classes': [], 'annotations': []}
    with open('./data/train_maccrobat.json', 'r') as f:
        data = json.load(f)
    for line in data:
        temp_data = {}
        temp_data['text'] = line['sentence']
        temp_data['entities'] = []
        t = time.localtime()
        temp_data['date'] = time.strftime("%d/%m/%Y %H:%M:%S", t)
        if line["entity_mentions"]:
            for entity in line["entity_mentions"]:
                start = len((line['sentence'].split(entity['text']))[0])
                end = start + len(entity["text"])
                label = entity['entity_type'].upper()
                temp_data['entities'].append((start,end,label))
                if entity["entity_type"].upper() not in train_data['classes']:
                    train_data['classes'].append(entity["entity_type"].upper())
        train_data['annotations'].append(temp_data)

    return train_data

def get_data_simple():
    with open('./data/samples.json', 'r') as f:
        data = json.load(f)
    train_data = {'classes': ['MEDICINE', 'MEDICALCONDITION', 'PATHOGEN'], 'annotations' : []}
    for text in data['examples']:
        temp_data = {}
        temp_data['text'] = text['content']
        temp_data['entities'] = []
        t = time.localtime()
        temp_data['date'] = time.strftime("%d/%m/%Y %H:%M:%S", t)
        for ann in text['annotations']:
            start = ann['start']
            end = ann['end']
            label = ann['tag_name'].upper()
            temp_data['entities'].append((start,end,label))
        train_data['annotations'].append(temp_data)
    return train_data

def get_data():
    train_data = {'classes': [], 'annotations': []}
    APOSTROPHE_ESCAPE = re.compile(r"(?<!u) ' (?![.}:,\s])")
    with open('./data/MES-CoV-train-origin.csv', encoding="utf8") as f:
        data = f.readlines()
    for line in data:
        line = line.strip().split("\t")
        temp_data = {}
        temp_data['text'] = line[1].replace(" ' ", "'")
        temp_data['entities'] = []
        t = time.localtime()
        temp_data['date'] = time.strftime("%d/%m/%Y %H:%M:%S", t)
        if " \' "in line[2]:
            line[2] = line[2].replace("\"\"", "\'")
            line[2] = line[2].replace(" \' ", " \\' ")
            line[2] = line[2][2:-2]
            array = literal_eval(APOSTROPHE_ESCAPE.sub(r"\'", line[2]))
        else:
            array = literal_eval(line[2])
        if isinstance(array, str):
            array = array.replace(" \' ", " \\' ")
            array = literal_eval(array)
        if isinstance(array, dict):
            start = len((line[1].split(array['value'].replace(" ' ", "'")))[0])
            end = start + len(array["value"].replace(" ' ", "'"))
            label = array['type'].upper()
            temp_data['entities'].append((start,end,label))
            if array["type"].upper() not in train_data['classes']:
                train_data['classes'].append(array["type"].upper())
        else:
            for entity in array:
                start = len((line[1].split(entity['value'].replace(" ' ", "'")))[0])
                end = start + len(entity["value"].replace(" ' ", "'"))
                label = entity['type'].upper()
                temp_data['entities'].append((start,end,label))
                if entity["type"].upper() not in train_data['classes']:
                    train_data['classes'].append(entity["type"].upper())
        train_data['annotations'].append(temp_data)
    return train_data

def main():
    myclient = pymongo.MongoClient("mongodb+srv://admin:RXEOifMvCaD6HJHB@nerdata.2hcvguh.mongodb.net/")
    mydb = myclient["NERData"]
    mycl = mydb["mes"]
    data = [get_data()]
    mycl.insert_many(data)
    
if __name__ == "__main__":
    main()