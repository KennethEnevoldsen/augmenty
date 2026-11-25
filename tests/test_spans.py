from collections.abc import Callable

import pytest
from spacy.language import Language
from spacy.tokens import Doc, Span
from spacy.training import Example

import augmenty


@pytest.fixture
def doc(nlp_en: Language) -> Doc:
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
def ent_augmenter() -> Callable:
    ent_augmenter = augmenty.load(
        "ents_replace_v1",
        level=1.00,
        ent_dict={"ORG": [["SpaCy"]]},
    )
    return ent_augmenter


def test_ent_replace_with_span_annotations(
    doc: Doc,
    ent_augmenter: Callable,
    nlp_en: Language,
):
    # add span annotations
    positive_noun_chunks = [doc[3:5]]
    is_augmenty = [doc[0:1]]
    doc.spans["positive_noun_chunks"] = positive_noun_chunks
    doc.spans["is_augmenty"] = is_augmenty

    docs = list(augmenty.docs([doc], augmenter=ent_augmenter, nlp=nlp_en))

    # Check spans
    doc_pos_noun_chunks = docs[0].spans["positive_noun_chunks"]
    assert doc_pos_noun_chunks[0].text == "wonderful tool", "the span is not maintained"

    doc_is_augmenty = docs[0].spans["is_augmenty"]
    assert doc_is_augmenty[0].text == "SpaCy", "the span is not maintained"


def test_ent_replace_with_cats_annotations(
    doc: Doc,
    ent_augmenter: Callable,
    nlp_en: Language,
):
    # add doc annotations
    doc.cats["is_positive"] = 1

    # augment
    docs = list(augmenty.docs([doc], augmenter=ent_augmenter, nlp=nlp_en))

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

    for p, e in zip(patterns, expected, strict=False):
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


@pytest.fixture
def doc_with_links(nlp_en: Language) -> Doc:
    doc = Doc(
        nlp_en.vocab,
        words=["Kenneth", "Enevoldsen", "made", "Augmenty", "."],
        spaces=[True, True, True, False, False],
    )
    doc.ents = [
        Span(doc, 0, 2, "PER", kb_id="Q1"),
        Span(doc, 3, 4, "ORG", kb_id="Q2"),
    ]
    return doc


def test_ent_replace_with_links(nlp_en: Language, doc_with_links: Doc):
    """Replaced entities drop their link, other links are kept (#219)."""
    aug = augmenty.load("ents_replace_v1", level=1, ent_dict={"PER": [["Jo"]]})
    (example,) = aug(nlp_en, Example(doc_with_links, doc_with_links))

    assert example.y.text == "Jo made Augmenty."
    assert [(e.text, e.kb_id_) for e in example.y.ents] == [
        ("Jo", ""),
        ("Augmenty", "Q2"),
    ]


def test_ent_format_with_links(nlp_en: Language, doc_with_links: Doc):
    """Formatted entities keep their link (#219)."""
    aug = augmenty.load(
        "ents_format_v1",
        level=1,
        reordering=[-1, None],
        formatter=[None, lambda t: t.text[0] + "."],
        ent_types=["PER"],
    )
    (example,) = aug(nlp_en, Example(doc_with_links, doc_with_links))

    assert example.y.text == "Enevoldsen K. made Augmenty."
    assert [(e.text, e.kb_id_) for e in example.y.ents] == [
        ("Enevoldsen K.", "Q1"),
        ("Augmenty", "Q2"),
    ]


def test_ent_format_with_span_annotations(nlp_en: Language):
    """Span annotations are moved along when a formatted entity changes length."""
    doc = Doc(
        nlp_en.vocab,
        words=["Kenneth", "Enevoldsen", "made", "Augmenty", "."],
        spaces=[True, True, True, False, False],
        ents=["B-PER", "I-PER", "O", "B-ORG", "O"],
    )
    doc.spans["person"] = [doc[0:2]]
    doc.spans["tool"] = [doc[3:4]]

    aug = augmenty.load(
        "ents_format_v1",
        level=1,
        reordering=[-1, None],
        formatter=[None, lambda t: t.text[0] + "."],
        ent_types=["PER"],
    )
    (augmented,) = augmenty.docs([doc], augmenter=aug, nlp=nlp_en)

    assert augmented.text == "Enevoldsen K. made Augmenty."
    assert augmented.spans["person"][0].text == "Enevoldsen K."
    assert augmented.spans["tool"][0].text == "Augmenty"
