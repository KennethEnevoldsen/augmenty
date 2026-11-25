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


@pytest.fixture(scope="session", params=["annotated", "unannotated"])
def books(request: pytest.FixtureRequest, nlp_en_md: Language) -> list[Example]:
    """The books with and without annotations (POS, dependencies, entities)."""
    nlp = nlp_en_md if request.param == "annotated" else spacy.blank("en")
    return [Example(doc, doc) for doc in nlp.pipe(BOOKS)]
