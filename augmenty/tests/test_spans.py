from spacy.tokens import Doc
from spacy.lang.en import English

import augmenty

import pytest

@pytest.fixture()
def nlp():
    nlp = English()
    return nlp

def test_create_ent_replace(nlp):
    doc = Doc(words=["Augmenty", "is", "a", "wonderful", "tool", "for", "augmentation", "."],
              spaces = [True]*7+[False],
              ents=["I-ORG"] + ["O"]*7)
    texts = ["Augmenty is a wonderful tool for augmentation."]

    ent_augmenter = augmenty.load("ents_replace.v1", level = 1.00, ent_dict={"ORG": [["SpaCy"]]})

    docs = list(augmenty.docs([doc], augmenter=ent_augmenter, nlp=nlp))
    
    docs[0].text == "SpaCy is a wonderful tool for augmentation."


    ent_augmenter = augmenty.load("ents_replace.v1", level = 1.00, ent_dict={"ORG": [["The SpaCy Universe"]]})

    augmented_texts = list(augmenty.docs([doc], augmenter=ent_augmenter, nlp=nlp))
    
    docs[0].text == "The SpaCy Universe is a wonderful tool for augmentation."
