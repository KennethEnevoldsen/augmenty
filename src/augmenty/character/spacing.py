"""Augmenters for modyfing spacing."""

import random
from functools import partial
from typing import Callable, Iterator

import spacy
from spacy.language import Language
from spacy.training import Example

from ..augment_utilities import make_text_from_orth


def remove_spacing_augmenter_v1(
    nlp: Language,
    example: Example,
    level: float,
) -> Iterator[Example]:
    def __replace(s):
        if random.random() < level and (s is True):
            return False
        return s

    example_dict = example.to_dict()
    example_dict["token_annotation"]["SPACY"] = [
        __replace(s) for s in example_dict["token_annotation"]["SPACY"]
    ]
    text = make_text_from_orth(example_dict)
    doc = nlp.make_doc(text)
    yield example.from_dict(doc, example_dict)


@spacy.registry.augmenters("remove_spacing_v1")
def create_remove_spacing_augmenter_v1(
    level: float,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter that removes spacing with a given probability.

    Args:
        level (float): The probability to remove a space.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.

    Example:
        >>> import augmenty
        >>> import spacy
        >>> nlp = spacy.blank("en")
        >>> remove_spacing_augmenter = augmenty.load("remove_spacing_v1", level=0.5)
        >>> texts = ["A sample text"]
        >>> list(augmenty.texts(texts, remove_spacing_augmenter, nlp))
        ["A sampletext"]
    """
    return partial(remove_spacing_augmenter_v1, level=level)
