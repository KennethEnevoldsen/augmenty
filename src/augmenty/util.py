"""Utility functions for the package."""

from typing import Any, Callable, Dict, Iterable, Iterator, List

import catalogue
import spacy
import thinc
from spacy.language import Language
from spacy.tokens import Doc
from spacy.training import Example

Augmenter = Callable[[Language, Example], Iterator[Example]]


class registry(thinc.registry):
    keyboards = catalogue.create("augmenty", "keyboards", entry_points=True)


def docs(
    docs: Iterable[Doc],
    augmenter: Augmenter,
    nlp: Language,
) -> Iterator[Doc]:
    """Augments an iterable of spaCy Doc.

    Args:
        docs: A iterable of spaCy Docs
        augmenter: An augmenter
        nlp: A spaCy language pipeline.

    Return:
        An iterator of the augmented Docs.

    Yields:
        Doc: The augmented Docs.

    Example:
        >>> from spacy.tokens import Doc
        >>> from spacy.lang.en import English
        >>> nlp = English()
        >>> docs = [Doc(words=["Fine", "by", "me"])]
        >>> augmenter = augmenty.load("upper_case_v1", level=1)
        >>> augmented_docs = augmenty.docs(docs, augmenter, nlp)
    """
    if isinstance(docs, Doc):
        docs = [docs]
    for doc in docs:
        example = Example(doc, doc)
        examples = augmenter(nlp, example)
        for e in examples:
            yield e.y


def texts(
    texts: Iterable[str],
    augmenter: Augmenter,
    nlp: Language,
) -> Iterable[str]:
    """Augments an list of texts.

    Args:
        texts: A iterable of strings
        augmenter: An augmenter
        nlp: A spaCy language pipeline.

    Return:
        An iterator of the augmented texts.

    Yields:
        The augmented text.
    """
    if isinstance(texts, str):
        texts = [texts]

    def __gen() -> Iterable[Doc]:  # type: ignore
        for text in texts:
            yield nlp(text)

    for doc in docs(__gen(), augmenter=augmenter, nlp=nlp):
        yield doc.text


def augmenters() -> Dict[str, Augmenter]:
    """A utility function to get an overview of all augmenters.

    Returns:
        Dictionary of all augmenters

    Example:
    >>> augmenters = augmenty.augmenters()
    >>> "upper_case_v1" in augmenters
    True
    """
    return spacy.registry.augmenters.get_all()  # type: ignore


def load(augmenter: str, **kwargs: Any) -> Augmenter:
    """A utility functionload an augmenter.

    Returns:
        Dictionary of all augmenters

    Example:
    >>> from spacy.lang.en import English
    >>> nlp = English()
    >>> upper_case_augmenter = augmenty.load("upper_case_v1", level = 1)
    >>> texts = ["hello there!"]
    >>> list(augmenty.texts(texts, upper_case_augmenter, nlp))
    ["HELLO THERE!"]
    """
    aug = spacy.registry.augmenters.get(augmenter)  # type: ignore
    return aug(**kwargs)


def keyboards() -> List[str]:  # type: ignore
    """A utility function to get an overview of all keyboards.

    Returns:
        List of all keyboards

    Example:
    >>> keyboards = augmenty.keyboards()
    """
    return list(registry.keyboards.get_all().keys())


def meta() -> Dict[str, dict]:
    """Returns a a dictionary containing metadata for each augmenter.

    Returns:
        A dictionary of meta data

    Example:
    >>> metadata = augmenty.meta()
    >>> metadata["token_swap_v1"]
    """
    import json
    import os
    import pathlib

    p = pathlib.Path(__file__).parent.resolve()
    p = p / "meta.json"
    with p.open() as f:
        r = json.load(f)
    return r
