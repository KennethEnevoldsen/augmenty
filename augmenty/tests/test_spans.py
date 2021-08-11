import spacy
from spacy.tokens import Doc
from spacy.lang.en import English

import augmenty

import pytest


@pytest.fixture()
def nlp():
    nlp = spacy.load("en_core_web_sm")
    return nlp


def test_create_ent_replace(nlp):
    nlp_ = English()
    doc = Doc(
        nlp_.vocab,
        words=[
            "Augmenty",
            "is",
            "a",
            "wonderful",
            "tool",
            "for",
            "augmentation",
            ".",
        ],
        spaces=[True] * 6 + [False] * 2,
        ents=["B-ORG"] + ["O"] * 7,
    )

    ent_augmenter = augmenty.load(
        "ents_replace.v1", level=1.00, ent_dict={"ORG": [["SpaCy"]]}
    )

    docs = list(augmenty.docs([doc], augmenter=ent_augmenter, nlp=nlp_))

    assert docs[0].text == "SpaCy is a wonderful tool for augmentation."

    ent_augmenter = augmenty.load(
        "ents_replace.v1", level=1.00, ent_dict={"ORG": [["The SpaCy Universe"]]}
    )

    docs = list(augmenty.docs([doc], augmenter=ent_augmenter, nlp=nlp_))

    assert docs[0].text == "The SpaCy Universe is a wonderful tool for augmentation."

    ent_augmenter = augmenty.load(
        "ents_replace.v1",
        level=1.00,
        ent_dict={"PERSON": [["Kenneth"], ["Lasse", "Hansen"]]},
    )

    doc = nlp("My name is Jack.")
    docs = list(augmenty.docs([doc], augmenter=ent_augmenter, nlp=nlp))

    assert docs[0].text != "My name is Jack."


def test_create_per_replace(nlp):
    doc = Doc(
        nlp.vocab,
        words=["My", "name", "is", "Kenneth", "Enevoldsen"],
        spaces=[True, True, True, True, False],
        ents=["O", "O", "O", "B-PERSON", "I-PERSON"],
    )
    names = {"firstname": ["Lasse"], "lastname": ["Hansen"]}

    patterns = [
        ["firstname"],
        ["firstname", "lastname"],
        ["firstname", "firstname", "lastname"],
    ]
    expected = [
        "My name is Lasse",
        "My name is Lasse Hansen",
        "My name is Lasse Lasse Hansen",
    ]

    for p, e in zip(patterns, expected):

        per_augmenter = augmenty.load(
            "per_replace.v1",
            level=1.00,
            names=names,
            patterns=[p],
        )

        docs = list(augmenty.docs([doc], augmenter=per_augmenter, nlp=nlp))

        assert docs[0].text == e

    per_augmenter = augmenty.load(
                "per_replace.v1",
                level=1.00,
                names={"firstname": ["Charles", "Jens"], "lastname": ["Kirkegaard", "Andersen"]},
                patterns=[p],
            )
    text = "My name is Charlie."
    doc = nlp(text)
    docs = list(augmenty.docs([doc], augmenter=per_augmenter, nlp=nlp))
    assert docs[0] != text


def test_create_ent_format_augmenter(nlp):
    abbreviate = lambda token: token.text[0] + "."

    augmenter = augmenty.load(
        "ents_format.v1",
        reordering=[-1, None],
        formatter=[None, abbreviate],
        level=1.00,
    )
    texts = ["my name is Kenneth Enevoldsen"]
    aug_text = "my name is Enevoldsen K."

    aug_texts = list(augmenty.texts(texts, augmenter, nlp))
    assert aug_texts[0] == aug_text
