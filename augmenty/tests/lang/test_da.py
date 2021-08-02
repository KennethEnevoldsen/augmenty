from augmenty.lang.da import create_æøå_replace_augmenter
from augmenty.lang.da import create_da_historical_noun_casing_augmenter

from augmenty import augment_docs

from spacy.lang.da import Danish
from spacy.tokens import Doc

import pytest

@pytest.fixture()
def nlp():
    nlp = Danish()
    return nlp


def test_create_da_æøå_replace_augmenter(nlp):
    text = "æøå"
    aug_text = "aeoeaa"

    aug = create_æøå_replace_augmenter(level=1)
    doc = nlp(text)

    docs = augment_docs([doc], augmenter=aug, nlp=nlp)
    assert next(docs).x.text == aug_text

def test_create_da_historical_noun_casing_augmenter(nlp):
    tokens = ["Jeg", "ejer", "en", "hund"]
    pos = ["PRON", "VERB", "DET", "NOUN"]
    solution =  "Jeg ejer en Hund"

    doc = Doc(nlp.vocab, words=tokens, pos=pos)

    aug = create_da_historical_noun_casing_augmenter()
    docs = augment_docs([doc], augmenter=aug, nlp=nlp)

    assert next(docs).text == solution
