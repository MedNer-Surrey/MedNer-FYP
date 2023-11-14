import json
import spacy
from spacy.tokens import DocBin
from spacy.util import filter_spans
from tqdm import tqdm

def see_data():
    train_data = {'classes': [], 'annotations': []}
    with open('./data/train_maccrobat.json', 'r') as f:
        data = json.load(f)
    for line in data:
        for entity in line["entity_mentions"]:
            if entity["entity_type"].upper() not in train_data['classes']:
                train_data['classes'].append(entity["entity_type"].upper())
    return train_data['classes']

def get_data():
    train_data = {'classes': [], 'annotations': []}
    with open('./data/train_maccrobat.json', 'r') as f:
        data = json.load(f)
    for line in data:
        temp_data = {}
        temp_data['text'] = line['sentence']
        temp_data['entities'] = []
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

def filter_data(data, nlp, doc_bin):
    for tr_ex in tqdm(data['annotations']):
        text = tr_ex['text']
        labels = tr_ex['entities']
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in labels:
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is None:
                print(start, end, label)
                print("Skipping")
            else:
                print("Span {}".format(span))
                ents.append(span)
        filtered_ents = filter_spans(ents)
        doc.ents = filtered_ents
        doc_bin.add(doc)

    doc_bin.to_disk("./data/maccro_train_data.spacy")

def main():
#    data = get_data()
 #   nlp = spacy.blank("en")
  #  doc_bin = DocBin()
   # filter_data(data, nlp, doc_bin)
    print(len(see_data()))
    for classe in see_data():
        print(classe)

if __name__ == "__main__":
    main()