"""Utility functions for the package."""

from typing import Callable, Dict, Iterable, Iterator, List

import catalogue  # type: ignore
import spacy  # type: ignore
import thinc  # type: ignore
from spacy.language import Language  # type: ignore
from spacy.tokens import Doc  # type: ignore
from spacy.training import Example  # type: ignore


class registry(thinc.registry):
    keyboards = catalogue.create("augmenty", "keyboards", entry_points=True)


def docs(
    docs: Iterable[Doc],  # type: ignore
    augmenter: Callable[[Language, Example], Iterator[Example]],  # type: ignore
    nlp: Language,
) -> Iterator[Doc]:  # type: ignore
    """Augments an iterable of spaCy Doc.

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
    texts: Iterable[str],  # type: ignore
    augmenter: Callable[[Language, Example], Iterator[Example]],  # type: ignore
    nlp: Language,
) -> Iterable[str]:  # type: ignore
    """Augments an list of texts.

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

    def __gen() -> Iterable[Doc]: # type: ignore
        for text in texts:
            yield nlp(text)

    for doc in docs(__gen(), augmenter=augmenter, nlp=nlp):
        yield doc.text


def augmenters() -> Dict[str, Callable]:  # type: ignore
    """A utility function to get an overview of all augmenters.

    Returns:
        Dict[str, Callable]: Dictionary of all augmenters

    Example:
    >>> augmenters = augmenty.augmenters()
    >>> "upper_case_v1" in augmenters
    True
    """
    return spacy.registry.augmenters.get_all() # type: ignore


def load(augmenter: str, **kwargs) -> Callable:  # type: ignore
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
        List[str]]: List of all keyboards

    Example:
    >>> keyboards = augmenty.keyboards()
    """
    return list(registry.keyboards.get_all().keys())


def meta() -> Dict[str, dict]:  # type: ignore
    """Returns a a dictionary containing metadata for each augmenter.

    Returns:
        Dict[str, dict]: A dictionary of meta data

    Example:
    >>> metadata = augmenty.meta()
    >>> metadata["token_swap_v1"]
    """
    import json
    import os
    import pathlib

    p = pathlib.Path(__file__).parent.resolve()
    p = os.path.join(p, "meta.json")  # type: ignore
    with open(p) as f:  # type: ignore
        r = json.load(f)
    return r
