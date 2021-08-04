"""Utility functions used for augmentation."""

from spacy.language import Language
from spacy.training import Example

from spacy.tokens import Doc

import random

from typing import Callable, Iterable, Iterator, List


def combine(
    augmenters: Iterable[Callable[[Language, Example], Iterator[Example]]]
) -> Callable[[Language, Example], Iterator[Example]]:
    """Combines a series og spaCy style augmenters.

    Args:
        augmenters (Iterable[Callable[[Language, Example], Iterator[Example]]]): An list of spaCy augmenters.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The combined augmenter
    """

    def apply_multiple_augmenters(nlp: Language, example: Example):
        examples = [example]
        for aug in augmenters:
            examples = [e for example in examples for e in aug(nlp, example)]
        for e in examples:
            yield e

    return apply_multiple_augmenters


def set_doc_level(
    augmenter: Callable[[Language, Example], Iterator[Example]],
    level: float,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Set the document level at which the tokenizer should be

    Args:
        augmenter (Callable[[Language, Example], Iterator[Example]]): A spaCy augmenters which you only want to apply to a certain percentage of docs
        level (float): The percentage of docs the which should be augmented.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The combined augmenter
    """

    def __augment(nlp: Language, example: Example):
        if random.random() > level:
            yield example
        else:
            for e in augmenter(nlp, example):
                yield e

    return __augment


def yield_original(
    augmenter: Callable[[Language, Example], Iterator[Example]]
) -> Callable[[Language, Example], Iterator[Example]]:
    """Wraps and augmented such that it yields both the original and augmented example.

    Args:
        augmenter (Callable[[Language, Example], Iterator[Example]]): A spaCy augmenters.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter, which now yields both the original and augmented example.
    """

    def __augment(nlp: Language, example: Example):
        for e in augmenter(nlp, example):
            yield e
        yield example

    return __augment


def make_text_from_orth(example_dict: dict) -> str:
    """
    Reconstructs the text based on ORTH and SPACY from an Example turned to dict
    """
    text = ""
    for orth, spacy in zip(
        example_dict["token_annotation"]["ORTH"],
        example_dict["token_annotation"]["SPACY"],
    ):
        text += orth
        if spacy:
            text += " "
    return text
