import random
from functools import partial
from typing import Callable, Iterator

import spacy
from spacy.language import Language
from spacy.training import Example

from ..augment_utilities import make_text_from_orth


def random_casing_augmenter_v1(
    nlp: Language,
    example: Example,
    level: float,
) -> Iterator[Example]:
    def __casing(c):
        if random.random() < level:
            return c.lower() if random.random() < 0.5 else c.upper()
        return c

    example_dict = example.to_dict()
    example_dict["token_annotation"]["ORTH"] = [
        "".join(__casing(c) for c in t.text) for t in example.y
    ]
    text = make_text_from_orth(example_dict)
    doc = nlp.make_doc(text)
    yield Example.from_dict(doc, example_dict)


@spacy.registry.augmenters("random_casing_v1")
def create_random_casing_augmenter_v1(
    level: float,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Create an augment that randomly changes the casing of the document.

    Args:
        level (float): The percentage of character that will have its casing changed.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.

    Example:
        >>> import augmenty
        >>> from spacy
        >>> nlp = spacy.blank("en")
        >>> random_casing_augmenter = augmenty.load("random_casing_v1", level=0.1)
        >>> texts = ["A sample text"]
        >>> list(augmenty.texts(texts, random_casing_augmenter, nlp))
        ["A saMple texT"]
    """
    return partial(random_casing_augmenter_v1, level=level)
