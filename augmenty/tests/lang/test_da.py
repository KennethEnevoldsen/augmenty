from augmenty.lang.da import create_da_æøå_replace_augmenter
from augmenty.lang.da import create_da_historical_noun_casing_augmenter

import augmenty

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

    aug = create_da_æøå_replace_augmenter(level=1)
    doc = nlp(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp)
    assert next(docs).text == aug_text


def test_create_da_historical_noun_casing_augmenter(nlp):
    tokens = ["Jeg", "ejer", "en", "hund"]
    pos = ["PRON", "VERB", "DET", "NOUN"]
    spaces = [True, True, True, False]
    solution = "Jeg ejer en Hund"

    doc = Doc(nlp.vocab, words=tokens, pos=pos, spaces = spaces)

    aug = create_da_historical_noun_casing_augmenter(level=1)
    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp)

    assert next(docs).text == solution
