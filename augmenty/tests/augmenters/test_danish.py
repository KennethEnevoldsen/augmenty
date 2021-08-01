from dacy.augmenters.danish import create_æøå_augmenter

from spacy.lang.da import Danish
from spacy.training import Example


def test_create_æøå_augmenter():
    aug = create_æøå_augmenter(doc_level=1, char_level=1)
    nlp = Danish()
    doc = nlp("æøå")
    example = Example(doc, doc)
    examples = aug(nlp, example)
    example_aug = next(examples)
    assert example_aug.x.text == "aeoeaa"