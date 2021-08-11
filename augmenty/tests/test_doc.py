import augmenty

from spacy.lang.en import English

import pytest


@pytest.fixture()
def nlp():
    nlp = English()
    return nlp


def test_create_spongebob_augmenter(nlp):
    spongebob_augmenter = augmenty.load("spongebob.v1", level=1)
    texts = ["A sample text"]
    aug_text = "A SaMpLe tExT"

    aug_texts = list(augmenty.texts(texts, spongebob_augmenter, nlp))
    assert aug_texts[0] == aug_text


def test_create_upper_case_augmenter(nlp):
    spongebob_augmenter = augmenty.load("upper_case.v1", level=1)
    texts = ["A sample text"]
    aug_text = "A SAMPLE TEXT"

    aug_texts = list(augmenty.texts(texts, spongebob_augmenter, nlp))
    assert aug_texts[0] == aug_text
