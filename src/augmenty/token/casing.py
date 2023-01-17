import random
from functools import partial
from typing import Callable, Iterator, Optional

import spacy  # type: ignore
from spacy.language import Language  # type: ignore
from spacy.training import Example  # type: ignore

from ..augment_utilities import make_text_from_orth


uncapitalize = lambda s: s[:1].lower() + s[1:] if s else s  # noqa: E731


def starting_case_augmenter_v1(
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


@spacy.registry.augmenters("random_starting_case_v1")
def create_starting_case_augmenter_v1(
    level: float,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter which randomly cases the first letter in each
    token.

    Args:
        level (float): Probability to randomly case the first letter of a token.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.

    Example:
        >>> import augmenty
        >>> from spacy.lang.en import English
        >>> nlp = English()
        >>> augmenter = augmenty.load("random_starting_case_v1", level=0.5)
        >>> texts = ["one two three"]
        >>> list(augmenty.texts(texts, augmenter, nlp))
        ["one Two Three"]
    """
    return partial(starting_case_augmenter_v1, level=level)


def conditional_casing_augmenter_v1(
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


@spacy.registry.augmenters("conditional_token_casing_v1")
def create_conditional_token_casing_augmenter_v1(
    conditional: Callable,
    level: float,
    lower: Optional[bool] = None,
    upper: Optional[bool] = None,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter that conditionally cases the first letter of a
    token based on the getter. Either lower og upper needs to specifiedd as
    True.

    Args:
        level (float):
        conditional (Callable):
        lower (Optional[bool], optional): If the conditional returns True should the
            casing the lowercased. Default to None.
        upper (Optional[bool], optional): If the conditional returns True should the
            casing the uppercased. Default to None.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.

    Example:
        >>> def is_pronoun(token):
        ... if token.pos_ == "PRON":
        ...    return True
        ... return False
        >>> aug = augmenty.load("conditional_token_casing_v1", level=1, lower=True,
        >>>                     conditional=is_pronoun)
    """
    if upper == lower or (upper is None and lower is None):
        raise ValueError(
            "You need to specify the desired casing the token should get either using "
            + "lower=True/False or upper=True/False.",
        )
    if lower is True:
        upper = False
    if lower is False:
        upper = True
    return partial(
        conditional_casing_augmenter_v1,
        level=level,
        upper=upper,
        conditional=conditional,
    )
