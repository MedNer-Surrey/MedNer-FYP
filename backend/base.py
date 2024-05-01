from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import spacy
from ast import literal_eval
from huggingface_hub import HfApi


app = Flask(__name__)
cors = CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
hf_api_key = "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"
hf_api = HfApi(token = hf_api_key)
snap_simple = hf_api.snapshot_download(repo_id="pavlopt/simple", local_dir="./models/simple")
snap_mes = hf_api.snapshot_download(repo_id="pavlopt/mes", local_dir="./models/mes")
snap_maccrobat = hf_api.snapshot_download(repo_id="pavlopt/maccrobat", local_dir="./models/maccrobat")


maccrobat = spacy.load("./models/maccrobat/model-best")
mes = spacy.load("./models/mes/model-best")
simple = spacy.load("./models/simple/model-best")
colors = {"AGE": "#870A30", "SEX": "#43B0F1", "DISEASE_DISORDER" : "#B1D8B7", "HISTORY" : "#EC8FD0", "DETAILED_DESCRIPTION" : "#a8e6cf", "CLINICAL_EVENT" : "#dcedc1", "NONBIOLOGICAL_LOCATION" : "#ffaaa5", "DIAGNOSTIC_PROCEDURE" : "#ff71ce", "LAB_VALUE" : "705446", "SIGN_SYMPTOM" : "#05ffa1", "THERAPEUTIC_PROCEDURE" : "#b967ff", "MEDICATION" : "#fffb96", "DOSAGE" : "#493267", "SEVERITY" : "#9e379f", "BIOLOGICAL_STRUCTURE" : "#e86af0", "ADMINISTRATION" : "#7bb3ff", "DATE" : "#d64d4d", "DISTANCE" : "#eb8c00", "COREFERENCE" : "#755f62", "AREA" : "#3c8da0", "DURATION" : "#efefef", "TIME" : "#c1c1c1", "OUTCOME" : "#883d65", "OTHER_EVENT" : "#b892a7", "QUANTITATIVE_CONCEPT" : "#a06e6a", "QUALITATIVE_CONCEPT" : "	#d1ab69", "OTHER_ENTITY" : "#c38370", "OCCUPATION" : "#b58a78", "ACTIVITY" : "#a2caf2", "SHAPE" : "#eeb67e", "TEXTURE" : "#a7f2a4", "FAMILY_HISTORY" : "#eeb67e", "PERSONAL_BACKGROUND" : "#f44d4d", "FREQUENCY" : "#57f028", "SUBJECT" : "#18eec8", "BIOLOGICAL_ATTRIBUTE" : "#483696", "VOLUME" : "#f6eeed", "COLOR" : "#074e67", "HEIGHT" : "#581f51", "WEIGHT" : "#dd9933", "MASS" : "#133337"}
options = {"ents": ['AGE', 'SEX', 'DISEASE_DISORDER', 'HISTORY', 'DETAILED_DESCRIPTION', 'CLINICAL_EVENT', 'NONBIOLOGICAL_LOCATION', 'DIAGNOSTIC_PROCEDURE', 'LAB_VALUE', 'SIGN_SYMPTOM', 'THERAPEUTIC_PROCEDURE', 'MEDICATION', 'DOSAGE', 'SEVERITY', 'BIOLOGICAL_STRUCTURE', 'ADMINISTRATION', 'DATE', 'DISTANCE', 'COREFERENCE', 'AREA', 'DURATION', 'TIME', 'OUTCOME', 'OTHER_EVENT', 'QUANTITATIVE_CONCEPT', 'QUALITATIVE_CONCEPT', 'OTHER_ENTITY', 'OCCUPATION', 'ACTIVITY', 'SHAPE', 'TEXTURE', 'FAMILY_HISTORY', 'PERSONAL_BACKGROUND', 'FREQUENCY', 'SUBJECT', 'BIOLOGICAL_ATTRIBUTE', 'VOLUME', 'COLOR', 'HEIGHT', 'WEIGHT', 'MASS'],
               "colors": colors}

@app.route('/api/apply', methods=['GET','POST'])
@cross_origin(supports_credentials=True, origin='*')
def my_profile():
    data = literal_eval(request.data.decode())
    nlp = globals()[data[0]['model']]
    text = data[0]['text']
    doc = nlp(text)
    return doc.to_json()

@app.route('/api/', methods=['GET','POST'])
@cross_origin(supports_credentials=True, origin='*')
def welcome():
    return render_template('index.html')