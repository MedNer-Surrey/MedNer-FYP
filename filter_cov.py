import json
import spacy
from spacy.tokens import DocBin
from spacy.util import filter_spans
from tqdm import tqdm
import csv
from ast import literal_eval
import re

APOSTROPHE_ESCAPE = re.compile(r"(?<!u) ' (?![.}:,\s])")

def see_data():
    train_data = {'classes': [], 'annotations': []}
    with open('./data/MES-CoV-train-origin.csv', encoding="utf8") as f:
        data = f.readlines()
        for row in data:
            row = row.strip().split("\t")
            if " \' "in row[2]:
                print(row[2])
                row[2] = row[2].replace("\"\"", "\'")
                row[2] = row[2].replace(" \' ", " \\' ")
                row[2] = row[2][2:-2]
                print("Hey {}".format(row[2]))
                array = literal_eval(APOSTROPHE_ESCAPE.sub(r"\'", row[2]))
            else:
                array = literal_eval(row[2])
            if isinstance(array, str):
                print("wtf")
                array = array.replace(" \' ", " \\' ")
                array = literal_eval(array)
            print("array {}".format(array))
            if isinstance(array, dict):
                print(array["type"])
            else:
                for entity in array:
                    print(entity)
                    print(entity["type"])


def get_data():
    train_data = {'classes': [], 'annotations': []}
    with open('./data/MES-CoV-train-origin.csv', encoding="utf8") as f:
        data = f.readlines()
    for line in data:
        line = line.strip().split("\t")
        temp_data = {}
        temp_data['text'] = line[1].replace(" ' ", "'")
        temp_data['entities'] = []

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
    print(train_data['classes'])
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

    doc_bin.to_disk("./data/mes-data.spacy")

def main():
    data = get_data()
    # nlp = spacy.blank("en")
    # doc_bin = DocBin()
    # filter_data(data, nlp, doc_bin)
    # hey = get_data()

if __name__ == "__main__":
    main()