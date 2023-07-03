import random
from functools import partial
from typing import Callable, Iterator

import spacy
from spacy.language import Language
from spacy.training import Example


def upper_casing_augmenter_v1(
    nlp: Language,
    example: Example,
    *,
    level: float,
) -> Iterator[Example]:
    if random.random() >= level:
        yield example
    else:
        example_dict = example.to_dict()
        doc = nlp.make_doc(example.text.upper())
        example_dict["token_annotation"]["ORTH"] = [
            t.text.upper() for t in example.reference
        ]
        yield example.from_dict(doc, example_dict)


@spacy.registry.augmenters("upper_case_v1")
def create_upper_casing_augmenter_v1(
    level: float,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Create an augmenter that converts documents to uppercase.

    Args:
        level (float): The percentage of examples that will be augmented.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.

    Example:
        >>> import augmenty
        >>> import spacy
        >>> nlp = spacy.blank("en")
        >>> upper_case_augmenter = augmenty.load("upper_case_v1", level=0.1)
        >>> texts = ["A sample text"]
        >>> list(augmenty.texts(texts, upper_case_augmenter, nlp))
        ["A SAMPLE TEXT"]
    """
    return partial(upper_casing_augmenter_v1, level=level)


def spongebob_augmenter_v1(
    nlp: Language,
    example: Example,
    *,
    level: float,
) -> Iterator[Example]:
    if random.random() >= level:
        yield example
    else:
        chars = [c.lower() if i % 2 else c.upper() for i, c in enumerate(example.text)]
        example_dict = example.to_dict()
        doc = nlp.make_doc("".join(chars))
        example_dict["token_annotation"]["ORTH"] = [
            doc.text[t.idx : t.idx + len(t.text)] for t in example.y
        ]
        yield example.from_dict(doc, example_dict)


@spacy.registry.augmenters("spongebob_v1")
def create_spongebob_augmenter_v1(
    level: float,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Create an augmneter that converts documents to SpOnGeBoB casing.

    Args:
        level (float): The percentage of examples that will be augmented.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.

    Example:
        >>> import augmenty
        >>> import spacy
        >>> nlp = spacy.blank("en")
        >>> spongebob_augmenter = augmenty.load("spongebob_v1", level=1)
        >>> texts = ["A sample text"]
        >>> list(augmenty.texts(texts, spongebob_augmenter, nlp))
        ["A SaMpLe tExT"]
    """
    return partial(spongebob_augmenter_v1, level=level)
