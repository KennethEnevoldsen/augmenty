"""Tests for handling checking issue 170:

https://github.com/KennethEnevoldsen/augmenty/issues/170.
"""

import pytest
import spacy
from spacy.tokens import Doc, Span

import augmenty


@pytest.fixture
def nlp():
    nlp_ = spacy.blank("en")
    nlp_.add_pipe("sentencizer")
    return nlp_


@pytest.fixture
def example_doc(nlp) -> Doc:
    text = "Joc Pederson and Thairo Estrada (concussion protocol) are each progressing. SS Brandon Crawford"
    doc = nlp(text)
    doc.ents = [
        Span(doc, 0, 2, "pers"),
        Span(doc, 3, 5, "pers"),
        Span(doc, 14, 16, "pers"),
    ]

    # validate example
    assert [t.text for t in doc] == [
        "Joc",
        "Pederson",
        "and",
        "Thairo",
        "Estrada",
        "(",
        "concussion",
        "protocol",
        ")",
        "are",
        "each",
        "progressing",
        ".",
        "SS",
        "Brandon",
        "Crawford",
    ]
    assert [e.text for e in doc.ents] == [
        "Joc Pederson",
        "Thairo Estrada",
        "Brandon Crawford",
    ]
    assert len(list(doc.sents)) == 2
    return doc


def test_entity_with_no_dep(nlp, example_doc: Doc):
    level = 1.0
    docs = [example_doc]
    augmenter = augmenty.load(
        "ents_replace_v1",
        level=level,
        ent_dict={"pers": ["Melvin R. Brown"]},
        replace_consistency=True,
        resolve_dependencies=True,
    )
    aug_doc = list(augmenty.docs(docs, augmenter, nlp))[0]
    assert len(aug_doc.ents) == len(docs[0].ents)
    assert (
        aug_doc.text
        == "Melvin R. Brown and Melvin R. Brown (concussion protocol) are each progressing. SS Melvin R. Brown"
    )
    assert aug_doc[0].text == "Melvin"
