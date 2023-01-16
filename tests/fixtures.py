import pytest
import spacy
from dacy.datasets import dane
from spacy.training import Example

from .books import BOOKS


# pipelines
@pytest.fixture()
def nlp_en():
    return spacy.blank("en")


@pytest.fixture()
def nlp_da():
    return spacy.blank("da")


@pytest.fixture()
def nlp_en_md():
    return spacy.load("en_core_web_md")


@pytest.fixture()
def dane_test(nlp_da):
    return dane(splits=["test"])(nlp_da)


@pytest.fixture()
def books_w_annotations(nlp_en_md):
    docs = nlp_en_md.pipe(BOOKS)
    return [Example(doc, doc) for doc in docs]


@pytest.fixture()
def books_without_annotations(nlp_en):
    docs = nlp_en.pipe(BOOKS)
    return [Example(doc, doc) for doc in docs]
