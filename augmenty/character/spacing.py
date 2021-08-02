"""
Augmenters for modyfing spacing
"""

from typing import Callable, Dict, Iterator

from functools import partial
import random

import spacy
from spacy.language import Language
from spacy.training import Example

from ..augment_utilites import make_text_from_orth


@spacy.registry.augmenters("remove_spacing.v1")
def create_spacing_augmenter(
    level: float
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter that removes spacing.

    Args:
        level (float): The probability to remove a space.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.
    """
    return partial(spacing_augmenter, level=level)


def spacing_augmenter(
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


