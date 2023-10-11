import json
import spacy
from spacy.tokens import DocBin
from spacy.util import filter_spans
from tqdm import tqdm

def get_data():
    with open('./data/samples.json', 'r') as f:
        data = json.load(f)
    train_data = {'classes': ['MEDICINE', 'MEDICALCONDITION', 'PATHOGEN'], 'annotations' : []}
    for text in data['examples']:
        temp_data = {}
        temp_data['text'] = text['content']
        temp_data['entities'] = []
        for ann in text['annotations']:
            start = ann['start']
            end = ann['end']
            label = ann['tag_name'].upper()
            temp_data['entities'].append((start,end,label))
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

    doc_bin.to_disk("./data/training_data.spacy")


def main():
    data = get_data()
    nlp = spacy.blank("en")
    doc_bin = DocBin()

    filter_data(data, nlp, doc_bin)

    # text = "What video sharing service did Steve Chen, Chad Hurley, and Jawed Karim create in 2005?"
    # nlp = spacy.load('en_core_web_sm')
    # doc = nlp(text)
    # data = displacy.render(doc, style="ent", jupyter=False)
    # with open("data.html", "w") as file:
    #     file.write(data)


if __name__ == "__main__":
    main()