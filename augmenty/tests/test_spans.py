import spacy
from spacy.tokens import Doc
from spacy.lang.en import English

import augmenty

import pytest


@pytest.fixture()
def nlp():
    nlp = spacy.load("en_core_web_sm")
    nlp = English()
    return nlp


def test_create_ent_replace(nlp):
    for nlp_ in [English(), nlp]:  # with and without a parser
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

        assert (
            docs[0].text == "The SpaCy Universe is a wonderful tool for augmentation."
        )
