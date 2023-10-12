import spacy

def main():
    nlp = spacy.load("output/model-best")
    text = "Antiretroviral therapy (ART) is recommended for all HIV-infected\
individuals to reduce the risk of disease progression.\nART also is recommended \
for HIV-infected individuals for the prevention of transmission of HIV.\nPatients \
starting ART should be willing and able to commit to treatment and understand the\
benefits and risks of therapy and the importance of adherence. Patients may choose\
to postpone therapy, and providers, on a case-by-case basis, may elect to defer\
therapy on the basis of clinical and/or psychosocial factors. HIV is a disease."
    doc = nlp(text)
    colors = {"PATHOGEN": "#F67DE3", "MEDICINE": "#7DF6D9", "MEDICALCONDITION":"#FFFFFF"}
    options = {"colors": colors} 
    data = spacy.displacy.render(doc, style="ent", options= options, jupyter=False)
    with open("data.html", "w") as file:
        file.write(data)

if __name__ == "__main__":
    main()