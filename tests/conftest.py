import pytest
import spacy
from spacy.language import Language
from spacy.training import Example

from .books import BOOKS


# pipelines
@pytest.fixture
def nlp_en() -> Language:
    return spacy.blank("en")


@pytest.fixture
def nlp_da() -> Language:
    return spacy.blank("da")


@pytest.fixture(scope="session")
def nlp_en_md() -> Language:
    return spacy.load("en_core_web_md")


@pytest.fixture(scope="session")
def books_w_annotations(nlp_en_md: Language) -> list:
    docs = nlp_en_md.pipe(BOOKS)
    return [Example(doc, doc) for doc in docs]


@pytest.fixture
def books_without_annotations(nlp_en: Language) -> list:
    docs = nlp_en.pipe(BOOKS)
    return [Example(doc, doc) for doc in docs]
