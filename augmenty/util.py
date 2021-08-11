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


def docs(
    docs: Iterable[Doc],
    augmenter: Callable[[Language, Example], Iterator[Example]],
    nlp: Language,
) -> Iterator[Doc]:
    """Augments an iterable of spaCy Doc

    Args:
        docs (Iterable[Doc]): A iterable of spaCy Docs
        augmenter (Callable[[Language, Example], Iterator[Example]]): An augmenter
        nlp (Language): A spaCy language pipeline.

    Return:
        Iterator[Doc]: An iterator of the augmented Docs.

    Yields:
        Doc: The augmented Docs.

    Example:
        >>> from spacy.tokens import Doc
        >>> from spacy.lang.en import English
        >>> nlp = English()
        >>> docs = [Doc(words=["Fine", "by", "me"])]
        >>> augmenter = augmenty.load("upper_case.v1", level=1)
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
    augmenter: Callable[[Language, Example], Iterator[Example]],
    nlp: Language,
) -> Iterable[str]:
    """Augments an list of texts

    Args:
        texts (Iterable[str]): A iterable of strings
        augmenter (Callable[[Language, Example], Iterator[Example]]): An augmenter
        nlp (Language): A spaCy language pipeline.

    Return:
        Iterator[str]: An iterator of the augmented texts.

    Yields:
        str: The augmented text.

    """
    if isinstance(texts, str):
        texts = [texts]

    def __gen() -> Iterable[Doc]:
        for text in texts:
            yield nlp(text)

    for doc in docs(__gen(), augmenter=augmenter, nlp=nlp):
        yield doc.text


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


def load(augmenter=str, **kwargs) -> Callable:
    """A utility functionload an augmenter

    Returns:
        Dict[str, Callable]: Dictionary of all augmenters

    Example:
    >>> from spacy.lang.en import English
    >>> nlp = English()
    >>> upper_case_augmenter = augmenty.load("upper_case.v1", level = 1)
    >>> texts = ["hello there!"]
    >>> list(augmenty.texts(texts, upper_case_augmenter, nlp))
    ["HELLO THERE!"]
    """
    aug = spacy.registry.augmenters.get(augmenter)
    return aug(**kwargs)


def keyboards() -> List[str]:
    """A utility function to get an overview of all keyboards

    Returns:
        List[str]]: List of all keyboards

    Example:
    >>> keyboards = augmenty.keyboards()
    """
    return list(registry.keyboards.get_all().keys())


def meta() -> Dict[str, dict]:
    """Returns a a dictionary containing metadata for each augmenter.

    Returns:
        Dict[str, dict]: A dictionary of meta data

    Example:
    >>> metadata = augmenty.meta()
    >>> metadata["token_swap.v1"]
    """
    import json
    import pathlib
    import os

    p = pathlib.Path(__file__).parent.resolve()
    p = os.path.join(p, "meta.json")
    with open(p) as f:
        r = json.load(f)
    return r
