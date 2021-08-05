import spacy
import augmenty

from spacy.lang.da import Danish
from spacy.lang.en import English


import pytest


@pytest.fixture()
def nlp():
    nlp = English()
    return nlp


def test_create_random_casing_augmenter(nlp):
    text = "some of the cases here should not be lowercased. there is naturally a chance that it might not end up that way, but it should be very very very rare."

    aug = spacy.registry.augmenters.get("random_casing.v1")(level=1)
    doc = nlp(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp)
    assert next(docs).text != text


def test_create_char_replace_random_augmenter(nlp):
    text = "The augmented version of this should not be the same"

    aug = spacy.registry.augmenters.get("char_replace_random.v1")(level=1)
    doc = nlp(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp)
    assert next(docs).text != text


def test_create_char_replace_augmenter(nlp):
    aug = spacy.registry.augmenters.get("char_replace.v1")(
        level=1, replace={"b": ["p"], "q": ["a", "b"]}
    )

    doc = nlp("The augmented version of this should be the same")
    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp)
    assert next(docs).text == "The augmented version of this should pe the same"

    doc = nlp("q w")
    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp)
    doc = next(docs)
    assert doc[0].text in ["a", "b"]
    assert doc[1].text == "w"


def test_create_keystroke_error_augmenter():
    text = "q"

    nlp = Danish()
    aug = spacy.registry.augmenters.get("keystroke_error.v1")(
        level=1, keyboard="da_qwerty.v1"
    )
    doc = nlp(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp)
    assert next(docs).text in "12wsa"


def test_create_char_swap_augmenter(nlp):
    aug = spacy.registry.augmenters.get("char_swap.v1")(level=1)
    doc = nlp("qw")
    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp)
    assert next(docs).text == "wq"


def test_create_spacing_augmenter(nlp):
    aug = spacy.registry.augmenters.get("remove_spacing.v1")(level=1)
    doc = nlp("a sentence.")
    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp)
    assert next(docs).text == "asentence."
