import random

import augmenty
from augmenty.doc import create_paragraph_subset_augmenter_v1
from spacy.language import Language
from spacy.tokens import Doc, Span


def test_create_spongebob_augmenter(nlp_en: Language):
    spongebob_augmenter = augmenty.load("spongebob_v1", level=1)
    texts = ["A sample text"]
    aug_text = "A SaMpLe tExT"

    aug_texts = list(augmenty.texts(texts, spongebob_augmenter, nlp_en))
    assert aug_texts[0] == aug_text  # type: ignore


def test_create_upper_case_augmenter(nlp_en: Language):
    spongebob_augmenter = augmenty.load("upper_case_v1", level=1)
    texts = ["A sample text"]
    aug_text = "A SAMPLE TEXT"

    aug_texts = list(augmenty.texts(texts, spongebob_augmenter, nlp_en))
    assert aug_texts[0] == aug_text  # type: ignore


def test_paragraph_subset_augmenter(nlp_en: Language):
    text = (
        "My name is Kenneth Enevoldsen. "
        + "Augmenty is a wonderful tool for augmentation. "
        + "It have tons of different augmenters. Augmenty is developed using spaCy."
    )
    doc = nlp_en(text)
    doc.set_ents(
        [
            Span(doc, 3, 5, label="person"),
            Span(doc, 6, 7, label="ORG"),
            Span(doc, 21, 22, label="ORG"),
        ],
    )

    for t in doc:
        t.is_sent_start = True if t.text == "." else False  # noqa

    p_subset_aug = augmenty.load(
        "paragraph_subset_augmenter_v1",
        min_paragraph=1,
        max_paragraph=1.00,
    )
    aug_docs = list(augmenty.docs([doc], p_subset_aug, nlp_en))
    assert aug_docs[0].text  # type: ignore

    # with sentencizer
    nlp_en.add_pipe("sentencizer")
    aug_texts = list(augmenty.texts([text], p_subset_aug, nlp_en))
    assert aug_texts[0]  # type: ignore

    # full length
    p_subset_aug = augmenty.load(
        "paragraph_subset_augmenter_v1",
        min_paragraph=1.0,
        max_paragraph=1.0,
    )
    aug_docs = list(augmenty.docs([doc], p_subset_aug, nlp_en))
    assert aug_docs[0].text == text  # type: ignore

    # zero length
    p_subset_aug = augmenty.load(
        "paragraph_subset_augmenter_v1",
        min_paragraph=0.0,
        max_paragraph=0.0,
    )
    aug_docs = list(augmenty.docs([doc], p_subset_aug, nlp_en))
    assert aug_docs[0].text == ""  # type: ignore


def test_paragraph_subset_augmenter_issue_when_ent_at_sentence_bound(nlp_en: Language):
    """
    There were issues with the augmenter when the entity was at the sentence boundery.

    Where it e.g. would return "I am John Heinz", even though the entity was "John" and "Heinz" with a sentence boundery in between.
    """
    p_subset_aug = create_paragraph_subset_augmenter_v1(
        min_paragraph=1,
        max_paragraph=0.50,
    )

    doc = Doc(
        nlp_en.vocab,
        words=["I", "am", "John", "Heinz", "is", "happy", "."],
        ents=["O", "O", "B-PER", "B-PER", "O", "O", "O"],
        sent_starts=[True, False, False, True, False, False, False],
    )
    random.seed(1)
    aug_docs = list(augmenty.docs([doc], p_subset_aug, nlp_en))
    doc = aug_docs[0]
    assert doc.text == "I am John " or doc.text == "Heinz is happy . "

    doc = Doc(
        nlp_en.vocab,
        words=["I", "am", "John", "Doe", "Heinz", "is", "happy", "."],
        ents=["O", "O", "B-PER", "I-PER", "B-PER", "O", "O", "O"],
        sent_starts=[True, False, False, False, True, False, False, False],
    )
    random.seed(42)
    aug_docs = list(augmenty.docs([doc], p_subset_aug, nlp_en))
    doc = aug_docs[0]
    assert doc.text == "I am John Doe " or doc.text == "Heinz is happy . "
