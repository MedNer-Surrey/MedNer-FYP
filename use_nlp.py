import spacy

def main():
    nlp = spacy.load("output/model-best")
    file=open("test.txt","r")
    text = file.read()
    doc = nlp(text)
    colors = {"PATHOGEN": "#870A30", "MEDICINE": "#43B0F1", "MEDICALCONDITION":"#B1D8B7"}
    options = {"ents" : ["PATHOGEN", "MEDICINE", "MEDICALCONDITION"] ,"colors": colors} 
    data = spacy.displacy.render(doc, style="ent", options= options, jupyter=False)
    with open("data.html", "w") as file:
        file.write(data)

if __name__ == "__main__":
    main()