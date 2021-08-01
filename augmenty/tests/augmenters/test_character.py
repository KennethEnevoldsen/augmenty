from dacy.augmenters import (
    create_char_swap_augmenter,
    create_spacing_augmenter,
    create_char_random_augmenter,
    create_char_replace_augmenter,
)
from spacy.lang.da import Danish
from spacy.training import Example


def test_create_char_swap_augmenter():
    aug = create_char_swap_augmenter(doc_level=1, char_level=1)
    nlp = Danish()
    doc = nlp("qw")
    example = Example(doc, doc)
    examples = aug(nlp, example)
    example_aug = next(examples)
    assert example_aug.x.text == "wq"


def test_create_spacing_augmenter():
    aug = create_spacing_augmenter(doc_level=1, spacing_level=1)
    nlp = Danish()
    doc = nlp("en sætning.")
    example = Example(doc, doc)
    examples = aug(nlp, example)
    example_aug = next(examples)
    assert example_aug.x.text == "ensætning."


def test_create_char_random_augmenter():
    aug = create_char_random_augmenter(doc_level=1, char_level=1)
    nlp = Danish()
    doc = nlp("en sætning.")
    example = Example(doc, doc)
    examples = aug(nlp, example)
    example_aug = next(examples)
    assert example_aug.x.text != "en sætning."


def test_create_char_replace_augmenter():
    aug = create_char_replace_augmenter(
        doc_level=1, char_level=1, replacement={"q": ["a", "b"]}
    )
    nlp = Danish()
    doc = nlp("q w")
    example = Example(doc, doc)
    examples = aug(nlp, example)
    example_aug = next(examples)
    assert example_aug.x[0].text in ["a", "b"]
    assert example_aug.x[1].text == "w"
