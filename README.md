# MedNer FYP

This repository is responsible for holding all of the stages of the Ner development.

## Requirements

### Training a model

PYTHON 3.8.3 x64

CUDA 1.18

### Runnin the application

Docker

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

## Docker run 

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

### Linux/MacOS

To use the app without errors access: http://127.0.0.1:3000/