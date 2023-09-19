from typing import Callable

import pytest
from spacy.language import Language
from spacy.tokens import Doc

import augmenty

from .fixtures import nlp_en, nlp_en_md  # noqa


@pytest.fixture
def doc(nlp_en: Language) -> Doc:  # noqa
    doc = Doc(
        nlp_en.vocab,
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
    return doc


@pytest.fixture
def ent_augmenter():
    ent_augmenter = augmenty.load(
        "ents_replace_v1",  # type: ignore
        level=1.00,
        ent_dict={"ORG": [["SpaCy"]]},
    )
    return ent_augmenter


@pytest.mark.parametrize(
    "nlp",
    [
        pytest.lazy_fixture("nlp_en"),
        pytest.lazy_fixture("nlp_en_md"),
    ],
)
def test_ent_replace_with_span_annotations(
    doc: Doc,
    ent_augmenter: Callable,
    nlp: Language,
):
    # add span annotations
    positive_noun_chunks = [doc[3:5]]
    is_augmenty = [doc[0:1]]
    doc.spans["positive_noun_chunks"] = positive_noun_chunks
    doc.spans["is_augmenty"] = is_augmenty

    docs = list(augmenty.docs([doc], augmenter=ent_augmenter, nlp=nlp))

    # Check spans
    doc_pos_noun_chunks = docs[0].spans["positive_noun_chunks"]
    assert doc_pos_noun_chunks[0].text == "wonderful tool", "the span is not maintained"

    doc_is_augmenty = docs[0].spans["is_augmenty"]
    assert doc_is_augmenty[0].text == "SpaCy", "the span is not maintained"


@pytest.mark.parametrize(
    "nlp",
    [
        pytest.lazy_fixture("nlp_en"),
        pytest.lazy_fixture("nlp_en_md"),
    ],
)
def test_ent_replace_with_cats_annotations(
    doc: Doc,
    ent_augmenter: Callable,
    nlp: Language,
):
    # add doc annotations
    doc.cats["is_positive"] = 1

    # augment
    docs = list(augmenty.docs([doc], augmenter=ent_augmenter, nlp=nlp))

    assert docs[0].cats["is_positive"] == 1.0, "the document category is not maintained"


def test_create_ent_replace(nlp_en_md, nlp_en):  # noqa F811
    doc = Doc(
        nlp_en.vocab,
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
        "ents_replace_v1",
        level=1.00,
        ent_dict={"ORG": [["SpaCy"]]},
    )

    docs = list(augmenty.docs([doc], augmenter=ent_augmenter, nlp=nlp_en))

    assert docs[0].text == "SpaCy is a wonderful tool for augmentation."

    ent_augmenter = augmenty.load(
        "ents_replace_v1",
        level=1.00,
        ent_dict={"ORG": [["The SpaCy Universe"]]},
    )

    docs = list(augmenty.docs([doc], augmenter=ent_augmenter, nlp=nlp_en))

    assert docs[0].text == "The SpaCy Universe is a wonderful tool for augmentation."

    ent_augmenter = augmenty.load(
        "ents_replace_v1",
        level=1.00,
        ent_dict={"PERSON": [["Kenneth"], ["Lasse", "Hansen"]]},
    )

    doc = nlp_en_md("My name is Jack.")
    docs = list(augmenty.docs([doc], augmenter=ent_augmenter, nlp=nlp_en_md))

    assert docs[0].text != "My name is Jack."


def test_create_per_replace(nlp_en, nlp_en_md):  # noqa F811
    doc = Doc(
        nlp_en.vocab,
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
            "per_replace_v1",
            level=1.00,
            names=names,
            patterns=[p],
        )

        docs = list(augmenty.docs([doc], augmenter=per_augmenter, nlp=nlp_en))

        assert docs[0].text == e

    per_augmenter = augmenty.load(
        "per_replace_v1",
        level=1.00,
        names={
            "firstname": ["Charles", "Jens"],
            "lastname": ["Kirkegaard", "Andersen"],
        },
        patterns=[p],
    )
    text = "My name is Charlie."
    doc = nlp_en_md(text)
    docs = list(augmenty.docs([doc], augmenter=per_augmenter, nlp=nlp_en_md))
    assert docs[0] != text


def test_create_ent_format_augmenter(nlp_en_md):  # noqa F811
    abbreviate = lambda token: token.text[0] + "."  # noqa: E731

    augmenter = augmenty.load(
        "ents_format_v1",
        reordering=[-1, None],
        formatter=[None, abbreviate],
        level=1.00,
    )
    texts = ["my name is Kenneth Enevoldsen"]
    aug_text = "my name is Enevoldsen K."

    aug_texts = list(augmenty.texts(texts, augmenter, nlp_en_md))
    assert aug_texts[0] == aug_text
