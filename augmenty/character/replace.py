"""
Augmenters for randomly or semi-randomly replacing characters
"""


import random
from functools import partial
from typing import Callable, Iterator

import spacy
from spacy.language import Language
from spacy.training import Example

from ..augment_utilities import make_text_from_orth
from ..keyboard import Keyboard


from ..util import registry


@spacy.registry.augmenters("char_replace_random.v1")
def create_char_random_augmenter(
    level: float, 
    keyboard: str = "en_qwerty.v1",
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter that replaces a character with a random character from the
    keyboard.

    Args:
        level (float): The probability to replace a character with a neightbouring character.
        keyboard (str, optional): A defined keyboard in the keyboard registry. To see a list of all keyboard you can run `augmenty,keyboards.get_all()`.
            Defaults to "en_qwerty.v1".

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter function.

    Example:
        >>> import augmenty
        >>> from spacy.lang.en import English
        >>> nlp = English()
        >>> char_random_augmenter = augmenty.load("char_replace_random.v1", level=0.1)
        >>> texts = ["A sample text"]
        >>> list(augmenty.texts(texts, char_random_augmenter, nlp))
        ["A sabple tex3"]
    """

    kb = Keyboard.from_registry(keyboard)
    replace_dict = {k: list(kb.all_keys()) for k in kb.all_keys()}
    return partial(char_replace_augmenter, replace=replace_dict, level=level)


@spacy.registry.augmenters("char_replace.v1")
def create_char_replace_augmenter(
    level: float, replace: dict
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter that replaces a character with a random character from replace dict

    Args:
        doc_level (float): probability to augment document.
        char_level (float): probability to augment character, if document is augmented.
        replace (dict): A dictionary denoting which characters denote potentials replace for each character.
            E.g. {"æ": ["ae"]}

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter function.
    """
    return partial(
        char_replace_augmenter,
        level=level,
        replace=replace,
    )


def char_replace_augmenter(
    nlp: Language,
    example: Example,
    level: float,
    replace: dict,
) -> Iterator[Example]:
    def __replace(t):
        t_ = []
        for i, c in enumerate(t.text):
            if random.random() < level and c in replace:
                c = random.choice(replace[c])
            t_.append(c)
        return "".join(t_)

    example_dict = example.to_dict()
    example_dict["token_annotation"]["ORTH"] = [__replace(t) for t in example.reference]
    text = make_text_from_orth(example_dict)
    doc = nlp.make_doc(text)
    yield example.from_dict(doc, example_dict)


@spacy.registry.augmenters("keystroke_error.v1")
def create_keystroke_error_augmenter(
    level: float,
    distance: float = 1.5,
    keyboard: str = "en_qwerty.v1",
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates a augmenter which augments a text with plausible typos based on keyboard distance.

    Args:
        level (float): The probability to replace a character with a neightbouring character.
        distance (float, optional): keyboard distance. Defaults to 1.5 corresponding to neighbouring keys including diagonals.
        keyboard (str, optional): A defined keyboard in the keyboard registry. To see a list of all keyboard you can run `augmenty,keyboards.get_all()`.
            Defaults to "en_qwerty.v1".

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmentation function

    Example:
        >>> import augmenty
        >>> from spacy.lang.en import English
        >>> nlp = English()
        >>> keystroke_error_augmenter = augmenty.load("keystroke_error.v1", level=0.1, keyboard="en_qwerty.v1")
        >>> texts = ["A sample text"]
        >>> list(augmenty.texts(texts, keystroke_error_augmenter, nlp))
        ["A sajple texr"]
    """
    kb = Keyboard.from_registry(keyboard)
    replace_dict = kb.create_distance_dict(distance=distance)
    return partial(char_replace_augmenter, replace=replace_dict, level=level)
