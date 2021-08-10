import random
from functools import partial
from typing import Iterator, Callable, Optional

import spacy
from spacy.language import Language
from spacy.training import Example

from ..augment_utilities import make_text_from_orth


@spacy.registry.augmenters("random_starting_case.v1")
def create_starting_case_augmenter(
    level: float,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter which randomly cases the first letter in each token.

    Args:
        level (float): Probability to randomly case the first letter of a token.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.

    Example:
        >>> import augmenty
        >>> from spacy.lang.en import English
        >>> nlp = English()
        >>> augmenter = augmenty.load("random_starting_case.v1", level=0.5)
        >>> texts = ["one two three"]
        >>> list(augmenty.texts(texts, augmenter, nlp))
        ["one Two Three"]
    """
    return partial(starting_case_augmenter, level=level)


@spacy.registry.augmenters("conditional_token_casing.v1")
def create_conditional_token_casing_augmenter(
    conditional: Callable,
    level: float, 
    lower: Optional[bool] = None,
    upper: Optional[bool] = None,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter that conditionally cases the first letter of a token based on the getter.
    Either lower og upper needs to specifiedd as True.

    Args:
        level (float):
        conditional (Callable):
        lower (Optional[bool], optional): If the conditional returns True should the casing the lowercased.
            Default to None.
        upper (Optional[bool], optional): If the conditional returns True should the casing the uppercased.
            Default to None.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.
    """
    if upper == lower or (upper is not True and lower is not True):
        raise ValueError(
            "You need to specify the desired casing the token should get either using lower=True or upper=True."
        )
    if lower is True:
        upper = False
    return partial(conditional_casing_augmenter, level=level, upper=upper, conditional=conditional)


def starting_case_augmenter(
    nlp: Language,
    example: Example,
    level: float,
) -> Iterator[Example]:
    def __casing(t):
        if random.random() < level:
            return (
                uncapitalize(t.text) if random.random() < 0.5 else t.text.capitalize()
            )
        return t.text

    example_dict = example.to_dict()
    example_dict["token_annotation"]["ORTH"] = [__casing(t) for t in example.reference]
    text = make_text_from_orth(example_dict)
    doc = nlp.make_doc(text)
    yield example.from_dict(doc, example_dict)


def conditional_casing_augmenter(
    nlp: Language,
    example: Example,
    level: float,
    upper: bool,
    conditional: Callable,
) -> Iterator[Example]:
    def __casing(t):
        if conditional(t) and random.random() < level:
            if upper:
                return t.text.capitalize()
            return uncapitalize(t.text)
        return t.text

    example_dict = example.to_dict()
    example_dict["token_annotation"]["ORTH"] = [__casing(t) for t in example.reference]
    text = make_text_from_orth(example_dict)
    doc = nlp.make_doc(text)
    yield example.from_dict(doc, example_dict)


uncapitalize = lambda s: s[:1].lower() + s[1:] if s else s
