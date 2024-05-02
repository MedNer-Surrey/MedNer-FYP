# MedNer FYP

This repository is responsible for holding all of the stages of the Ner development.

## Requirements

PYTHON 3.8.3 x64

CUDA 1.16

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
docker-compose up 
```

## TODO

Integrate [prodigy](https://prodi.gy/) with app

base.py - backend
```python
#TODO Create thread that queries mongodb check to see if updated = True and if yes redownload models and load them
```

check_data.py - cron
```python
#CHECK HOW TO REPLACE MODELS OR SOMETHING
```

Integrate cron into docker-compose