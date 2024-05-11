from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import spacy
from ast import literal_eval
from huggingface_hub import HfApi
import pymongo
import time
import threading

#Flask
app = Flask(__name__)
cors = CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
#MongoDB
myclient = pymongo.MongoClient("mongodb+srv://admin:RXEOifMvCaD6HJHB@nerdata.2hcvguh.mongodb.net/")
mydb = myclient["NERData"]
mycl = mydb["check"]
#Huggingface
hf_api_key = "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"
hf_api = HfApi(token = hf_api_key)
snap_simple = hf_api.snapshot_download(repo_id="pavlopt/simple", local_dir="./models/simple")
snap_mes = hf_api.snapshot_download(repo_id="pavlopt/mes", local_dir="./models/mes")
snap_maccrobat = hf_api.snapshot_download(repo_id="pavlopt/maccrobat", local_dir="./models/maccrobat")


maccrobat = spacy.load("./models/maccrobat/model-best")
mes = spacy.load("./models/mes/model-best")
simple = spacy.load("./models/simple/model-best")

def check_updated(maccrobat, mes, simple):
    operation = mycl.find({}, {"_id":0})
    updated = list(operation)[0]["updated"]
    if updated == True:
        print("Update detected...")
        snap_simple = hf_api.snapshot_download(repo_id="pavlopt/simple", local_dir="./models/simple")
        snap_mes = hf_api.snapshot_download(repo_id="pavlopt/mes", local_dir="./models/mes")
        snap_maccrobat = hf_api.snapshot_download(repo_id="pavlopt/maccrobat", local_dir="./models/maccrobat")
        maccrobat = spacy.load("./models/maccrobat/model-best")
        mes = spacy.load("./models/mes/model-best")
        simple = spacy.load("./models/simple/model-best")
    mycl.update_many({}, { "$set": {"updated": False}})
    time.sleep(30)

x = threading.Thread(target=check_updated, args=(maccrobat,mes,simple,))
x.start()

@app.route('/api/apply', methods=['GET','POST'])
@cross_origin(supports_credentials=True, origin='*')
def my_profile():
    data = literal_eval(request.data.decode())
    nlp = globals()[data[0]['model']]
    text = data[0]['text']
    doc = nlp(text)
    return doc.to_json()