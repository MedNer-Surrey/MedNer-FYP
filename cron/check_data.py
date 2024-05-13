import pymongo
import time
from datetime import datetime
from huggingface_hub import HfApi
import spacy
import random
from spacy.training import Example
from spacy.tokens import Doc, DocBin
from spacy.util import filter_spans
from tqdm import tqdm
import os
import shutil

myclient = pymongo.MongoClient("mongodb+srv://admin:RXEOifMvCaD6HJHB@nerdata.2hcvguh.mongodb.net/")
mydb = myclient["NERData"]
mycl = mydb["check"]
hf_api_key = "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"
hf_api = HfApi(token = hf_api_key)

#
snap_simple = hf_api.snapshot_download(repo_id="pavlopt/simple", local_dir="./models/simple")
snap_mes = hf_api.snapshot_download(repo_id="pavlopt/mes", local_dir="./models/mes")
snap_maccrobat = hf_api.snapshot_download(repo_id="pavlopt/maccrobat", local_dir="./models/maccrobat")

#Check data function
def check_new(collection, array):
    coll = mydb[collection]
    operation = coll.find({}, {"_id":0})
    data = list(operation)
    annotations = data[0]["annotations"]
    for annot in annotations:
        annot_date = datetime.strptime(annot['date'], '%d/%m/%Y %H:%M:%S')
        if last_check < annot_date:
            array.append({"text": annot['text'], "entities": annot["entities"]})
        elif last_check > annot_date:
            pass
        else:
            pass

def filter_entities(data, nlp):
    final_data = []
    for tr_ex in tqdm(data['annotations']):
        text = tr_ex["text"]
        labels = tr_ex["entities"]
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in labels:
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is not None:
                ents.append((start, end, label))
        tr_ex["entities"] = ents
        final_data.append({"text": tr_ex['text'], "entities": tr_ex["entities"]})
    return final_data

def filter_data(data, nlp):
    final_data = []
    for tr_ex in tqdm(data['annotations']):
        text = tr_ex['text']
        labels = tr_ex['entities']
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in labels:
            span = doc.char_span(start, end, label=label)
            if span is not None:
                ents.append(span)
        filtered_ents = filter_spans(ents)
        doc.ents = filtered_ents
        final_data.append(doc)
    return final_data

#Update function
def update_model(data_array, nlp):
    examples = []
    for object in tqdm(data_array):
        doc = nlp(object.text)
        entities = object.ents
        if len(entities) != 0:
            example = Example.from_dict(doc, {"entities": entities})
            examples.append(example)

    n_iter = 20
    data = []
    optimizer = nlp.create_optimizer()
    for i in range(n_iter):
        losses = {}
        random.shuffle(data)
        for example in data:
            nlp.update([example], sgd=optimizer, losses=losses,drop=0.01)

while True:
    print("Starting check...")
    #NEW DATE
    updated = []
    dic = {}
    t = time.localtime()
    dic['last_check'] = time.strftime("%d/%m/%Y %H:%M:%S", t)
    print("New update_time {}".format(dic['last_check']))
    #LAST DATE
    operation = list(mycl.find({}, {"_id":0}))
    last_check = operation[0]["last_check"]
    dic['updated'] = operation[0]["updated"]
    last_check = datetime.strptime(last_check, "%d/%m/%Y %H:%M:%S")
    #GET NEW DATA
    new_maccro_data = []
    new_mes_data = []
    new_simple_data = []

    check_new("maccro", new_maccro_data)
    check_new("mes", new_mes_data)
    check_new("simple", new_simple_data)
    #TRAIN MODELS if there is new data
    #STILL NEED TO UPLOAD THE MODELS
    if new_maccro_data:
        nlp = spacy.load("./models/maccrobat/model-best")
        new_maccro_data = filter_data({"annotations": new_maccro_data}, nlp)
        update_model(new_maccro_data, nlp)
        nlp.to_disk('./models/maccrobat_updated/')
        shutil.rmtree("./models/maccrobat/model-best")
        os.rename("./models/maccrobat_updated", "./models/model-best")
        shutil.move("./models/model-best", "./models/maccrobat")
        hf_api.upload_folder(folder_path="./models/maccrobat/model-best",repo_id="pavlopt/maccrobat")

    if new_mes_data:
        nlp = spacy.load("./models/mes/model-best")
        new_mes_data = filter_data({"annotations": new_mes_data}, nlp)
        update_model(new_mes_data, nlp)
        nlp.to_disk('./models/mes_updated/')
        shutil.rmtree("./models/mes/model-best")
        os.rename("./models/mes_updated", "./models/model-best")
        shutil.move("./models/model-best", "./models/mes/")
        hf_api.upload_folder(folder_path="./models/mes/model-best",repo_id="pavlopt/mes")

    if new_simple_data:
        nlp = spacy.load("./models/simple/model-best")
        new_simple_data = filter_data({"annotations": new_simple_data}, nlp)
        update_model(new_simple_data, nlp)
        nlp.to_disk('./models/simple_updated/')
        shutil.rmtree("./models/simple/model-best")
        os.rename("./models/simple_updated", "./models/model-best")
        shutil.move("./models/model-best", "./models/simple")
        hf_api.upload_folder(folder_path="./models/simple/model-best",repo_id="pavlopt/simple")


    #AFTER TRAINING SAVE updated INSIDE CHECK COLLECTION
    operation = list(mycl.find({}, {"_id":0}))
    dic['updated'] = operation[0]["updated"]
    if new_maccro_data or new_mes_data or new_simple_data:
        dic['updated'] = True
    updated.append(dic)
    mycl.update_one({}, {"$set": {"last_check": dic['last_check'], "updated": dic['updated']}})
    time.sleep(30)
    print("Check complete...")