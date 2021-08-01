import random
from functools import partial
from typing import Iterator, Callable

import spacy
from spacy.language import Language
from spacy.training import Example

from ..augment_utilites import make_text_from_orth


@spacy.registry.augmenters("grundtvigian_spacing_augmenter.v1")
def create_grundtvigian_spacing_augmenter(
    level: float,
) -> Callable[[Language, Example], Iterator[Example]]:
    """The Danish philosopher N.F.S. Grundtvig used letter spacing to add
     e m p h a s i s  to words (Baunvig, Jarvis and Nielbo, 2020).
     This augmenter randomly adds letter spacing emphasis to words.
     This augmentation which are human readable, but which are clearly
     challenging for systems using a white-space centric tokenization.

    Args:
        level (float): The probability add grundtvigian letter spacing emphasis.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.
    """
    return partial(grundtvigian_spacing_augmenter, level=level)


def grundtvigian_spacing_augmenter(
    nlp: Language,
    example: Example,
    level: float,
) -> Iterator[Example]:
    def __spacing(t):
        if random.random() < level:
            return " ".join([c for c in text])
        return t.text

    example_dict = example.to_dict()
    example_dict["token_annotation"]["ORTH"] = [__spacing(t) for t in example.y]
    text = make_text_from_orth(example_dict)
    doc = nlp.make_doc(text)
    yield example.from_dict(doc, example_dict)


@spacy.registry.augmenters("random_spacing_augmenter.v1")
def create_random_spacing_augmenter(
    level: float,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Randomly adds a space after a chara cter. Tokens are kept the same.

    Args:
        level (float): The probability to add a space after a character.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.
    """
    return partial(random_spacing_augmenter, level=level)


def random_spacing_augmenter(
    nlp: Language,
    example: Example,
    level: float,
) -> Iterator[Example]:
    def __spacing(t):
        text = []
        for c in t.text:
            text.append(c)
            if random.random() < level:
                text.append(" ")
        text = text[:-1] if  text[-1] == " " else text
        return " ".join(text)

    example_dict = example.to_dict()
    example_dict["token_annotation"]["ORTH"] = [__spacing(t) for t in example.y]
    text = make_text_from_orth(example_dict)
    doc = nlp.make_doc(text)
    yield example.from_dict(doc, example_dict)
