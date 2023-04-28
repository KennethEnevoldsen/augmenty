"""Utility functions used for augmentation."""

import random
from functools import partial
from typing import Callable, Iterable, Iterator

from spacy.language import Language
from spacy.training import Example


def combine(
    augmenters: Iterable[Callable[[Language, Example], Iterator[Example]]],
) -> Callable[[Language, Example], Iterator[Example]]:
    """Combines a series of spaCy style augmenters.

    Args:
        augmenters: An list of spaCy augmenters.

    Returns:
        The combined augmenter
    """

    def apply_multiple_augmenters(nlp: Language, example: Example):
        examples = [example]
        for aug in augmenters:
            examples = [e for example in examples for e in aug(nlp, example)]
        yield from examples

    return apply_multiple_augmenters


def set_doc_level(
    augmenter: Callable[[Language, Example], Iterator[Example]],
    level: float,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Set the percantage of examples that the augmenter should be applied to.

    Args:
        augmenter: A spaCy augmenters which you only want to apply to a
            certain percentage of docs
        level: The percentage of docs the which should be augmented.

    Returns:
        The combined augmenter
    """

    def __augment(nlp: Language, example: Example):
        if random.random() > level:
            yield example
        else:
            yield from augmenter(nlp, example)

    return __augment


def repeat(
    augmenter: Callable[[Language, Example], Iterator[Example]],
    n: int,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Repeats an augmenter n times over the same example thus increasing the
    sample size.

    Args:
        augmenter: An augmenter.
        n: Number of times the augmenter should be repeated

    Returns:
        The repeated augmenter

    Example:
        >>> augmenter = augmenty.load("char_swap_v1", level=.02)
        >>> repeated_augmenter = augmenty.repeat(augmenter=aug, n=3)
    """

    def __augment(nlp: Language, example: Example):
        for i in range(n):
            yield from augmenter(nlp, example)

    return __augment


def yield_original(
    augmenter: Callable[[Language, Example], Iterator[Example]],
    doc_level: float = 1.0,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Wraps and augmented such that it yields both the original and augmented
    example.

    Args:
        augmenter: A spaCy augmenters.
        doc_level: The percentage of documents the augmenter should be applied to.
            Only yield the original when the original doc is augmented.

    Returns:
        The augmenter, which now yields both the original and augmented example.
    """

    def __augment(nlp: Language, example: Example, level: float):
        if random.random() < level:
            yield from augmenter(nlp, example)
        yield example

    return partial(__augment, level=doc_level)


def make_text_from_orth(example_dict: dict) -> str:
    """Reconstructs the text based on ORTH and SPACY from an Example turned to
    dict."""
    text = ""
    for orth, spacy in zip(
        example_dict["token_annotation"]["ORTH"],
        example_dict["token_annotation"]["SPACY"],
    ):
        text += orth
        if spacy:
            text += " "
    return text
