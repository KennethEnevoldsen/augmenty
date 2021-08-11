from typing import Callable, Iterator

import spacy
from spacy.language import Language
from spacy.training import Example

from ...character import create_char_replace_augmenter
from ...token import create_conditional_token_casing_augmenter


@spacy.registry.augmenters("da_æøå_replace.v1")
def create_da_æøå_replace_augmenter(
    level: float,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter that augments æ, ø, and å into their spelling variants ae, oe, aa.

    Args:
        level (float): probability to augment æ, ø or å.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The desired augmenter.

    Example:
        >>> import augmenty
        >>> from spacy.lang.en import English
        >>> nlp = English()
        >>> augmenter = augmenty.load("da_æøå_replace.v1", level=0.1)
        >>> texts = ["æ ø Å"]
        >>> list(augmenty.texts(texts, augmenter, nlp))
        ["ae oe Aa"]
    """
    replace_dict = {
        "æ": ["ae"],
        "ø": ["oe"],
        "å": ["aa"],
        "Æ": ["Ae"],
        "Ø": ["Oe"],
        "Å": ["Aa"],
    }
    return create_char_replace_augmenter(replace=replace_dict, level=level)


@spacy.registry.augmenters("da_historical_noun_casing.v1")
def create_da_historical_noun_casing_augmenter(level: float) -> Callable[
    [Language, Example], Iterator[Example]
]:
    """Creates an augmenter that capitalizes nouns.

    Args:
        level (float): The probabiliy to upper case a noun.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.
    """

    def conditional(token):
        if token.pos_ == "NOUN":
            return True
        return False

    return create_conditional_token_casing_augmenter(conditional=conditional, upper=True, level=level)
