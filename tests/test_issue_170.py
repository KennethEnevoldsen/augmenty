"""Tests for handling checking issue 170:

https://github.com/KennethEnevoldsen/augmenty/issues/170.
"""

import pytest
import spacy
from spacy.tokens import DocBin, Span

import augmenty


@pytest.fixture
def nlp():
    return spacy.blank("en")


@pytest.fixture()
def sentencizer(nlp):
    return nlp.create_pipe("sentencizer")


@pytest.fixture
def docbin_no_dep(nlp) -> DocBin:
    text = "Joc Pederson and Thairo Estrada (concussion protocol) are each progressing. SS Brandon Crawford"
    doc = nlp.make_doc(text)
    doc.ents = [
        Span(doc, 0, 2, "pers"),
        Span(doc, 3, 5, "pers"),
        Span(doc, 14, 16, "pers"),
    ]
    docbin_no_dep_ = DocBin(store_user_data=True, docs=[doc])
    return docbin_no_dep_


def test_smoke_docbin_no_dep(nlp, docbin_no_dep: DocBin):
    doc = list(docbin_no_dep.get_docs(nlp.vocab))[0]
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


def test_smoke_docbin_no_dep_sent(nlp, sentencizer, docbin_no_dep: DocBin):
    doc = list(docbin_no_dep.get_docs(nlp.vocab))[0]
    doc = sentencizer(doc)
    assert len(list(doc.sents)) == 2


def test_augmenty_dependency_bug(nlp, docbin_no_dep: DocBin):
    level = 1.0
    n_repeat = 3
    docs = list(docbin_no_dep.get_docs(nlp.vocab))
    ents_as_str = ["Melvin R. Brown"]
    augmenter = augmenty.load(
        "ents_replace_v1",
        level=level,
        ent_dict={"pers": [[s] for s in ents_as_str]},
        replace_consistency=True,
        resolve_dependencies=True,
    )
    repeated_augmenter = augmenty.repeat(augmenter=augmenter, n=n_repeat)
    augmented_docs = list(augmenty.docs(docs, repeated_augmenter, nlp))
    assert augmented_docs


def test_augmenty_dependency_bug_with_sent(nlp, sentencizer, docbin_no_dep: DocBin):
    level = 1.0
    n_repeat = 3
    docs = list([sentencizer(doc) for doc in docbin_no_dep.get_docs(nlp.vocab)])
    # ents_as_str = ['Mark Folkard', 'Melvin R. Brown', 'Kristiina Mäkelä']
    ents_as_str = ["Melvin R. Brown"]
    augmenter = augmenty.load(
        "ents_replace_v1",
        level=level,
        ent_dict={"pers": [[s] for s in ents_as_str]},
        replace_consistency=True,
        resolve_dependencies=True,
    )
    repeated_augmenter = augmenty.repeat(augmenter=augmenter, n=n_repeat)
    augmented_docs = list(augmenty.docs(docs, repeated_augmenter, nlp))
    assert augmented_docs
