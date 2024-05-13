# MedNER FYP

MedNER is an application developed in order to improve medical data processing systems. It integrates NER models in an automated and simple way with a React app.
It is my Final Year Project and it is inspired in the Epsom Hospital's needs.

## Requirements

### Training a model

PYTHON 3.8.3 x64

CUDA 1.18

### Running the application

Docker

Git

## Train a model

```bash
python -m venv .env
source .env/bin/activate
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm
python3 -m spacy init fill-config base_config.cfg config.cfg
python3 -m spacy train config.cfg --output ./output --paths.train ./data/training_data.spacy --paths.dev ./data/training_data.spacy --gpu-id 0

```

## Before running the app

### Linux/MacOS

/src/App.js (Line 21) change url to 'http://0.0.0.0:3000/api/apply'

### Windows

/src/App.js (Line 21) change url to 'http://127.0.0.1:3000/api/apply'

## Commands to run the application

```bash
git clone https://github.com/MedNer-Surrey/MedNer-FYP.git
cd MedNer-FYP
```

```bash
docker build -f Dockerfile.api -t backend . 
docker build -f Dockerfile.client -t client .
docker build -f Dockerfile.cron -t cron .
docker build -f Dockerfile.anot -t annotator . --platform linux/amd64
docker-compose up 
```

## ACCESS

Do not use localhost due to CORS exceptions

### Linux/MacOS

To use the app without errors access: http://0.0.0.0:3000/

### Windows

To use the app without errors access: http://127.0.0.1:3000/

## Code breakdown

/backend/base.py - Imports the models from huggingface and handles POST requests (Flask)

/src/App.js - Main page

/cron/check_data.py - Responsible for updating models if there is new data in MongoDB and uploading them to [Hugging Face](https://huggingface.co/pavlopt)

/ner-annotator - NER annotator application

