import pytest
from spacy.lang.da import Danish
from spacy.language import Language
from spacy.tokens import Doc

import augmenty
from augmenty.lang.da import (
    create_da_historical_noun_casing_augmenter_v1,
    create_da_æøå_replace_augmenter_v1,
)


@pytest.fixture()
def nlp() -> Language:
    nlp = Danish()
    return nlp


def test_create_da_æøå_replace_augmenter(nlp: Language):
    text = "æøå"
    aug_text = "aeoeaa"

    aug = create_da_æøå_replace_augmenter_v1(level=1)
    doc = nlp(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp)  # type: ignore
    assert next(docs).text == aug_text  # type: ignore


def test_create_da_historical_noun_casing_augmenter(nlp: Language):
    tokens = ["Jeg", "ejer", "en", "hund"]
    pos = ["PRON", "VERB", "DET", "NOUN"]
    spaces = [True, True, True, False]
    solution = "Jeg ejer en Hund"

    doc = Doc(nlp.vocab, words=tokens, pos=pos, spaces=spaces)

    aug = create_da_historical_noun_casing_augmenter_v1(level=1)
    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp)

    assert next(docs).text == solution  # type: ignore
