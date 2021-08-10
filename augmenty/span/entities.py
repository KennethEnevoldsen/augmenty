import random
from functools import partial
from typing import Callable, Dict, Iterable, Iterator, List, Optional, Union, Generator

import numpy as np

import spacy
from spacy.language import Language
from spacy.training import Example
from spacy.tokens import Token

from ..augment_utilities import make_text_from_orth


@spacy.registry.augmenters("ents_replace.v1")
def create_ent_augmenter(
    ent_dict: Dict[str, Iterable[List[str]]],
    level: float,
    replace_consistency: bool = True,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Create an augmenter which replaces an entity based on a dictionary lookup.

    Args:
        ent_dict (Dict[str, Iterable[List[str]]]): A dictionary with keys corresponding the the entity type
            you wish to replace (e.g. "PER") and a itarable of the replacements. A replacement is a list of string of
            the desired entity replacement ["Kenneth", "Enevoldsen"].
        level (float): the percentage of entities to be augmented.
        replace_consistency (bool, optional): Should an entity always be replaced with the same entity? Defaults to True.
    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter

    Example:
        >>> ent_dict = {"ORG": [["Google"], ["Apple"]], "PERSON": [["Kenneth"], ["Lasse", "Hansen"]]}
        >>> ent_augmenter = create_ent_augmenter(ent_dict, level = 0.1)  # augment 10% of names
    """
    return partial(
        ent_augmenter,
        ent_dict=ent_dict,
        level=level,
        replace_consistency=replace_consistency,
    )


def ent_augmenter(
    nlp: Language,
    example: Example,
    ent_dict: Dict[str, Iterable[List[str]]],
    level: float,
    replace_consistency: bool,
) -> Iterator[Example]:
    replaced_ents = {}
    example_dict = example.to_dict()

    offset = 0

    tok_anno = example_dict["token_annotation"]
    ents = example_dict["doc_annotation"]["entities"]
    if example.y.has_annotation("HEAD"):
        head = np.array(tok_anno["HEAD"])

    for ent in example.y.ents:
        if ent.label_ in ent_dict and random.random() < level:
            if replace_consistency and ent.text in replaced_ents:
                new_ent = replaced_ents[ent.text]
            else:
                if isinstance(ent_dict[ent.label_], Generator):
                    new_ent = next(ent_dict[ent.label_])
                else:
                    new_ent = random.sample(ent_dict[ent.label_], k=1)[0]
                if replace_consistency:
                    replaced_ents[ent.text] = new_ent

            # Handle token annotations
            len_ent = len(new_ent)
            i = slice(ent.start + offset, ent.end + offset)
            tok_anno["ORTH"][i] = new_ent
            tok_anno["LEMMA"][i] = new_ent

            tok_anno["TAG"][i] = ["PROPN"] * len_ent
            tok_anno["POS"][i] = ["PROPN"] * len_ent

            tok_anno["MORPH"][i] = [""] * len_ent
            tok_anno["DEP"][i] = [tok_anno["DEP"][i][0]] + ["flat"] * (len_ent - 1)

            tok_anno["SENT_START"][i] = [tok_anno["SENT_START"][i][0]] + [0] * (len_ent - 1)
            tok_anno["SPACY"][i] = [True] * (len_ent - 1) + (
                tok_anno["SPACY"][i][-1:]  # set last spacing
            )

            if example.y.has_annotation("HEAD"):
                # Handle HEAD
                offset_ = len_ent - (ent.end - ent.start)

                head[head > ent.start + offset] += offset_
                # keep first head correcting for changing entity size, set rest to refer to index of first name
                head = np.concatenate(
                    [
                        np.array(head[: ent.start + offset]),  # before
                        np.array(
                            [head[ent.start + offset]]
                            + [ent.start + offset] * (len_ent - 1)
                        ),  # the entity
                        np.array(head[ent.start + 1 + offset :]),  # after
                    ]
                )
                offset += offset_

            # Handle entities IOB tags
            if len_ent == 1:
                ents[i] = ["U-" + ent.label_]
            else:
                ents[i] = (
                    ["B-" + ent.label_]
                    + ["I-" + ent.label_] * (len_ent - 2)
                    + ["L-" + ent.label_]
                )

    if example.y.has_annotation("HEAD"):
        tok_anno["HEAD"] = head.tolist()
    else:
        tok_anno["HEAD"] = list(range(len(tok_anno["ORTH"])))

    text = make_text_from_orth(example_dict)

    doc = nlp.make_doc(text)
    yield Example.from_dict(doc, example_dict)


@spacy.registry.augmenters("per_replace.v1")
def create_per_replace_augmenter(
    names: Dict[
        str, List[str]
    ],  # {"firstname": ["Kenneth", "Lasse"], "lastname": ["Enevoldsen", "Hansen"]}
    patterns: List[List[str]],  # ["firstname", "firstname", "lastname"]
    level: float,
    names_p: Dict[str, List[float]] = {},
    patterns_p: Optional[List[float]] = None,
    replace_consistency: bool = True,
    person_tag: str = "PERSON"
) -> Callable[[Language, Example], Iterator[Example]]:
    """Create an augmenter which replaces a name (PER) with a news sampled from the names dictionary.

    Args:
        names (Dict[str, List[str]]): A dictionary of list of names to sample from.
            These could for example include first name and last names.
        pattern (List[List[str]]): The pattern to create the names. This should be a list of patterns.
            Where a pattern is a list of strings, where the string denote the list in the names
            dictionary in which to sample from.
        level (float): The proportion of PER entities to replace.
        names_p (Dict[str, List[float]], optional): The probability to sample each name.
            Defaults to {}, indicating equal probability for each name.
        patterns_p (Optional[List[float]], optional): The probability to sample each pattern.
            Defaults to None, indicating equal probability for each pattern.
        replace_consistency (bool, optional): Should the entity always be replaced with the same entity? Defaults to True.
        person_tag (str, optional) The tag of the person entity. Defaults to "PERSON".

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter

    Example:
        >>> names = {"firstname": ["Kenneth", "Lasse"], "lastname": ["Enevoldsen", "Hansen"]}
        >>> patterns = [["firstname"], ["firstname", "lastname"], ["firstname", "firstname", "lastname"]]
        >>> per_augmenter = create_per_replace_augmenter(names, patterns, level=0.1) # replace 10% of names
    """

    names_gen = generator_from_name_dict(names, patterns, names_p, patterns_p)

    return create_ent_augmenter(
        ent_dict={person_tag: names_gen},
        level=level,
        replace_consistency=replace_consistency,
    )


def generator_from_name_dict(
    names: Dict[str, List[str]],
    patterns: List[List[str]],
    names_p: Dict[str, List[float]],
    patterns_p: Optional[List[float]],
):
    """
    A utility function for create_pers_replace_augmenter, which creates an infinite generator based on
    a names dictionary and a list of patterns, where the string in the pattern correspond to the list
    in the pattern.
    """
    lp = len(patterns)

    while True:
        i = np.random.choice(lp, size=1, replace=True, p=patterns_p)[0]
        yield [
            str(np.random.choice(names[p], size=1, replace=True, p=names_p.get(p))[0])
            for p in patterns[i]
        ]


@spacy.registry.augmenters("ents_format.v1")
def create_ent_format_augmenter(
    reordering: List[Union[int, None]],
    formatter: List[Union[Callable[[Token], str], None]],
    level: float,
    ent_types: Optional[List[str]] = None,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter which reorders and formats a entity according to reordering and formatting functions.

    Args:
        reordering (List[Union[int, None]]): A reordering consisting of a the desired order of the list of indices,
            where None denotes the remainder. For instance if this function was solely used on names [-1, None]
            indicate last name (the last token in the name) followed by the remainder of the name. Similarly one could more
            use the reordering [3, 1, 2] e.g. indicating last name, first name, middle name. Note that if the entity only include two
            tokens the 3 will be ignored producing the pattern [1, 2].
        formatter (List[Union[Callable[[Token], str], None]]): A list of function taking in a spaCy Token returning the reformatted str.
            E.g. the function `lambda token: token.text[0] + "."` would abbreviate the token and add punctuation. None corresponds to no augmentation.
        level (float): The probability of an entities being augmented.
        ent_types (Optional[Iterable[str]], optional):  The entity types which should be augmented. Defaults to None, indicating all entity types.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter

    Example:
        >>> import augmenty
        >>> import spacy
        >>> nlp = spacy.load("en_core_web_sm")
        >>> abbreviate = lambda token: token.text[0] + "."
        >>> augmenter = augmenty.load("ents_format.v1", reordering = [-1, None], formatter=[None, abbreviate], level=1, ent_types=["PER"])
        >>> texts = ["my name is Kenneth Enevoldsen"]
        >>> list(augmenty.texts(texts, augmenter, nlp))
        ["my name is Enevoldsen K."]
    """
    return partial(
        ent_format_augmenter,
        reordering=reordering,
        formatter=formatter,
        level=level,
        ent_types=ent_types,
    )


def ent_format_augmenter(
    nlp: Language,
    example: Example,
    reordering: List[Union[int, None]],
    formatter: List[Union[Callable[[Token], str], None]],
    level: float,
    ent_types: Optional[List[str]] = None,
) -> Iterator[Example]:
    example_dict = example.to_dict()

    tok_anno = example_dict["token_annotation"]
    ents = example_dict["doc_annotation"]["entities"]

    for ent in example.y.ents:
        if (ent_types is None or ent.label_ in ent_types) and random.random() < level:

            # reorder tokens
            new_ent = []
            ent_ = [e for e in ent]
            for i in reordering:
                if i is not None and i >= len(ent):
                    continue
                new_ent += ent_ if i is None else [ent_.pop(i)]

            # format tokens
            new_ent_ = [e.text if f is None else f(e) for e, f in zip(new_ent, formatter)]

            if len(new_ent_) < len(new_ent):
                new_ent_ += new_ent[len(new_ent_) :]

            tok_anno["ORTH"][ent.start : ent.end] = new_ent_
            tok_anno["LEMMA"][ent.start : ent.end] = new_ent_

    text = make_text_from_orth(example_dict)

    doc = nlp.make_doc(text)
    yield Example.from_dict(doc, example_dict)
