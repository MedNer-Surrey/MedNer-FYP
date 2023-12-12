import spacy

def main():
    nlp = spacy.load("output/model-best")
    file=open("test.txt","r")
    text = file.read()
    doc = nlp(text)
    colors = {"PERSON": "#870A30", "ORGANIZATION": "#43B0F1", "LOCATION" : "#B1D8B7", "VACCINE-RELATED" : "#EC8FD0", "DISEASE" : "#a8e6cf", "DRUG" : "#dcedc1", "SYMPTOM" : "#ffaaa5"}
    options = {"ents": ['PERSON', 'ORGANIZATION', 'LOCATION', 'VACCINE-RELATED', 'DISEASE', 'DRUG', 'SYMPTOM'],
               "colors": colors}
    data = spacy.displacy.render(doc, options=options, style="ent", jupyter=False)
    with open("data.html", "w") as file:
        file.write(data)

if __name__ == "__main__":
    main()