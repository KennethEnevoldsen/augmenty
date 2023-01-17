import random
from functools import partial
from typing import Callable, Iterator

import spacy
from spacy.language import Language
from spacy.training import Example

from ..augment_utilities import make_text_from_orth


def letter_spacing_augmenter_v1(
    nlp: Language,
    example: Example,
    level: float,
) -> Iterator[Example]:
    def __spacing(t):
        if random.random() < level:
            return " ".join([c for c in t.text])
        return t.text

    example_dict = example.to_dict()
    example_dict["token_annotation"]["ORTH"] = [__spacing(t) for t in example.y]
    text = make_text_from_orth(example_dict)
    doc = nlp.make_doc(text)
    yield example.from_dict(doc, example_dict)


@spacy.registry.augmenters("letter_spacing_augmenter_v1")
def create_letter_spacing_augmenter_v1(
    level: float,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Typically casing is used to add emphasis to words, but letter spacing
    has also been used to add e m p h a s i s  to words (e.g. by Grundtvig;
    Baunvig, Jarvis and Nielbo, 2020). This augmenter randomly adds letter
    spacing emphasis to words. This augmentation which are human readable, but
    which are clearly challenging for systems using a white-space centric
    tokenization.

    Args:
        level (float): The probability add grundtvigian letter spacing emphasis.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.
    """
    return partial(letter_spacing_augmenter_v1, level=level)


def spacing_insertion_augmenter_v1(
    nlp: Language,
    example: Example,
    level: float,
    max_insertions: int,
) -> Iterator[Example]:
    def __spacing(t):
        insertions = 0
        text = []
        for c in t.text[:-1]:  # can't put a space at the end
            text.append(c)
            if random.random() < level and insertions < max_insertions:
                insertions += 1
                text.append(" ")
        text.append(t.text[-1])
        return "".join(text)

    example_dict = example.to_dict()
    example_dict["token_annotation"]["ORTH"] = [__spacing(t) for t in example.y]
    text = make_text_from_orth(example_dict)
    doc = nlp.make_doc(text)
    yield example.from_dict(doc, example_dict)


@spacy.registry.augmenters("spacing_insertion_v1")
def create_spacing_insertion_augmenter_v1(
    level: float,
    max_insertions: int = 1,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates and augmneter that randomly adds a space after a chara cter.
    Tokens are kept the same.

    Args:
        level (float): The probability to add a space after a character.
        max_insertions (int, optional): Maximum number of insertions pr. word.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.
    """
    return partial(
        spacing_insertion_augmenter_v1,
        level=level,
        max_insertions=max_insertions,
    )
