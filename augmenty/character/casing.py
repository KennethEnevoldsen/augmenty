import random
from functools import partial
from typing import Iterator, Callable

import spacy
from spacy.language import Language
from spacy.training import Example

from ..augment_utilities import make_text_from_orth


@spacy.registry.augmenters("random_casing.v1")
def create_random_casing_augmenter(
    level: float,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Create an augment that randomly changes the casing of the document.

    Args:
        level (float): The percentage of character that will have its casing changed.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.

    Example:
        >>> import augmenty
        >>> from spacy.lang.en import English
        >>> nlp = English()
        >>> random_casing_augmenter = augmenty.load("random_casing.v1", level=0.1)
        >>> texts = ["A sample text"]
        >>> list(augmenty.texts(texts, random_casing_augmenter, nlp))
        ["A saMple texT"]
    """
    return partial(random_casing_augmenter, level=level)


def random_casing_augmenter(
    nlp: Language, example: Example, level: float
) -> Iterator[Example]:
    def __casing(c):
        if random.random() < level:
            return c.lower() if random.random() < 0.5 else c.upper()
        return c

    example_dict = example.to_dict()
    example_dict["token_annotation"]["ORTH"] = ["".join(__casing(c) for c in t.text) for t in example.y]
    text = make_text_from_orth(example_dict)
    doc = nlp.make_doc(text)
    yield Example.from_dict(doc, example_dict)
