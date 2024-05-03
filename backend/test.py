from huggingface_hub import hf_hub_download, snapshot_download
from huggingface_hub import HfApi
import spacy

hf_api_key = "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"
api = HfApi(token = hf_api_key)
snap_simple = api.snapshot_download(repo_id="pavlopt/simple", local_dir="./models/simple")
print(str(snap_simple))
simple = spacy.load("models/simple/model-best")