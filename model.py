import pandas as pnd
import spacy

def get_data():
    raw_data = pnd.read_csv('./data/samples.csv', index_col=0)
    small_data = raw_data.head()
    return small_data

def main():
    data = get_data()
    nlp = spacy.load('en_core_web_sm')

if __name__ == "__main__":
    main()