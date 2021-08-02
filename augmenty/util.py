"""Utility functions for the package."""

import thinc
import catalogue

from spacy.language import Language
from spacy.training import Example

from spacy.tokens import Doc
import spacy


from typing import Callable, Dict, Iterable, Iterator, List


class registry(thinc.registry):
    keyboards = catalogue.create("augmenty", "keyboards", entry_points=True)


def augment_docs(
    docs: Iterable[Doc],
    augmenter: Callable[[Language, Example], Iterator[Example]],
    nlp: Language,
) -> Iterable[Doc]:
    """Augments an iterable of spaCy Doc

    Args:
        docs (Iterable[Doc]): A interable of spaCy Docs
        augmenter (Callable[[Language, Example], Iterator[Example]]): An augmenter
        nlp (Language): A spaCy language pipeline

    Yields:
        Iterator[Doc]: An iterator of the augmented Docs.
    """
    for doc in docs:
        example = Example(doc, doc)
        examples = augmenter(nlp, example)
        for e in examples:
            yield e


def augmenters() -> Dict[str, Callable]:
    """A utility function to get an overview of all augmenters

    Returns:
        Dict[str, Callable]: Dictionary of all augmenters

    Example:
    >>> augmenters = augmenty.augmenters()
    >>> "upper_case.v1" in augmenters
    True
    """
    return spacy.registry.augmenters.get_all()


def keyboards() -> List[str]:
    """A utility function to get an overview of all keyboards

    Returns:
        List[str]]: List of all keyboards

    Example:
    >>> keyboards = augmenty.keyboards()
    """
    return list(registry.keyboards.get_all().keys())
