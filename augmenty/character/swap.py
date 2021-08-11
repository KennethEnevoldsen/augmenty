"""
Augmenters for swapping characters
"""


from typing import Callable, Dict, Iterator

from functools import partial
import random

import spacy
from spacy.language import Language
from spacy.training import Example

from ..augment_utilities import make_text_from_orth


@spacy.registry.augmenters("char_swap.v1")
def create_char_swap_augmenter(
    level: float,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter that swaps two neighbouring characters in a token with a given probability.

    Args:
        level (float): probability to replace a character.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.

    Example:
        >>> import augmenty
        >>> from spacy.lang.en import English
        >>> nlp = English()
        >>> char_swap_augmenter = augmenty.load("char_swap.v1", level=0.1)
        >>> texts = ["A sample text"]
        >>> list(augmenty.texts(texts, char_swap_augmenter, nlp))
        ["A smaple txet"]
    """
    return partial(char_swap_augmenter, level=level)


def char_swap_augmenter(nlp: Language, example: Example, level) -> Iterator[Example]:
    def __replace(t):
        for i, c in enumerate(t.text[:-1]):
            if random.random() < level:
                return t.text[:i] + t.text[i + 1] + c + t.text[i + 2 :]
        return t.text

    example_dict = example.to_dict()
    example_dict["token_annotation"]["ORTH"] = [__replace(t) for t in example.reference]
    text = make_text_from_orth(example_dict)
    doc = nlp.make_doc(text)
    yield example.from_dict(doc, example_dict)
