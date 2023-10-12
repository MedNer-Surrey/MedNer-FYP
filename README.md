# MedNer-FYP

Commands to run locally:


python -m venv .env

source .env/bin/activate

pip install -U pip setuptools wheel

pip install -U spacy

python -m spacy download en_core_web_sm

python3 -m spacy init fill-config base_config.cfg config.cfg

python3 -m spacy train config.cfg --output ./output --paths.train ./data/training_data.spacy --paths.dev ./data/training_data.spacy --gpu-id 0