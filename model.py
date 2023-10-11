import pandas as pnd
import spacy
from spacy import displacy

def get_data():
    raw_data = pnd.read_csv('./data/samples.csv', index_col=0)
    small_data = raw_data.head()
    return small_data

def main():
    data = get_data()
    text = "What video sharing service did Steve Chen, Chad Hurley, and Jawed Karim create in 2005?"
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    data = displacy.render(doc, style="ent", jupyter=False)
    with open("data.html", "w") as file:
        file.write(data)


if __name__ == "__main__":
    main()