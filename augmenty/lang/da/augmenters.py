from functools import partial
from typing import Callable, Iterator

import spacy
from spacy.language import Language
from spacy.training import Example

from ...character import char_replace_augmenter
from ...token.casing import create_conditional_casing_augmenter

@spacy.registry.augmenters("æøå_augmenter.v1")
def create_æøå_augmenter(
    level: float,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Augments æ, ø, and å into their spelling variants ae, oe, aa.

    Args:
        level (float): probability to augment æ, ø or å.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The desired augmenter.
    """
    replace_dict = {
        "æ": ["ae"],
        "ø": ["oe"],
        "å": ["aa"],
        "Æ": ["Ae"],
        "Ø": ["Oe"],
        "Å": ["Aa"],
    }
    return partial(
        char_replace_augmenter,
        replacement=replace_dict,
        level=level
    )

@spacy.registry.augmenters("historical_noun_casing_augmenter.v1")
def create_historical_noun_casing_augmenter() -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter that changes all nouns to uppercase, reflecting that 
     cases the first letter a token based on the getter.
    Either lower og upper needs to specifiedd as True.

    Args:
        conditional (Callable):
        lower (Optional[bool], optional): If the conditional returns True should the casing the lowercased.
            Default to None.
        upper (Optional[bool], optional): If the conditional returns True should the casing the uppercased.
            Default to None.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.
    """
    def conditional(token):
        if token.pos_ == "NOUN":
            return True
        return False

    return create_conditional_casing_augmenter(conditional=conditional, upper=True)