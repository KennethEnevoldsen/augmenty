import random
from functools import partial
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    Iterator,
    List,
    Optional,
    Union,
)

import numpy as np
from spacy.language import Language
from spacy.tokens import Doc, Span, Token
from spacy.training import Example
from spacy.util import registry

from augmenty import span

from ..augment_utilities import make_text_from_orth
from .utils import offset_range

# create entity type
ENTITY = Union[str, List[str], Span, Doc]


def _spacing_to_str(spacing: Union[List[str], List[bool]]) -> List[str]:
    def to_string(x: Union[str, bool]) -> str:
        if isinstance(x, str):
            return x
        else:
            return " " if x else ""

    return [to_string(x) for x in spacing]


def __normalize_entity(entity: ENTITY, nlp: Language) -> Dict[str, Any]:
    spacy = None
    pos = None
    tag = None
    morph = None
    lemma = None

    if isinstance(entity, str):
        ent_doc = nlp(entity)
        orth = [tok.text for tok in ent_doc]
        spacy = [tok.whitespace_ for tok in ent_doc]
    elif isinstance(entity, list):
        orth = entity
    elif isinstance(entity, (Span, Doc)):
        orth = [tok.text for tok in entity]
        spacy = [tok.whitespace_ for tok in entity]
        pos = [tok.pos_ for tok in entity]
        tag = [tok.tag_ for tok in entity]
        morph = [tok.morph for tok in entity]
        lemma = [tok.lemma_ for tok in entity]
    else:
        raise ValueError(
            f"entity must be of type str, List[str] or Span, not {type(entity)}",
        )
    # if not specifed use default values
    if spacy is None:
        spacy = [" "] * len(orth)
    if pos is None:
        pos = ["PROPN"] * len(orth)
    if tag is None:
        tag = ["PROPN"] * len(orth)
    if morph is None:
        morph = [""] * len(orth)
    if lemma is None:
        lemma = orth

    _spacy = _spacing_to_str(spacy)
    str_repr = ""
    for e, s in zip(orth[:-1], _spacy[:-1]):
        str_repr += e + s
    str_repr += orth[-1]

    return {
        "ORTH": orth,
        "SPACY": spacy,
        "POS": pos,
        "TAG": tag,
        "MORPH": morph,
        "LEMMA": lemma,
        "STR": str_repr,
    }


def _update_span_annotations(
    span_anno: Dict[str, list],
    ent: Span,
    offset: int,
    entity_offset: int,
) -> Dict[str, list]:
    """Update the span annotations to be in line with the new doc."""
    ent_range = (ent.start + offset, ent.end + offset)

    for anno_key, spans in span_anno.items():
        new_spans = []
        for span_start, span_end, _, __ in spans:
            span_start, span_end = offset_range(
                current_range=(span_start, span_end),
                inserted_range=ent_range,
                offset=entity_offset,
            )
            new_spans.append((span_start, span_end, _, __))

        span_anno[anno_key] = new_spans

    return span_anno


def ent_augmenter_v1(
    nlp: Language,
    example: Example,
    level: float,
    ent_dict: Dict[str, Iterable[ENTITY]],
    replace_consistency: bool,
    resolve_dependencies: bool,
) -> Iterator[Example]:
    replaced_ents: Dict[str, ENTITY] = {}
    example_dict = example.to_dict()

    offset = 0
    str_offset = 0

    spans_anno = example_dict["doc_annotation"]["spans"]
    tok_anno = example_dict["token_annotation"]
    ents = example_dict["doc_annotation"]["entities"]

    should_update_heads = example.y.has_annotation("HEAD") and resolve_dependencies
    if should_update_heads:
        head = np.array(tok_anno["HEAD"])

    for ent in example.y.ents:
        if ent.label_ in ent_dict and random.random() < level:
            if replace_consistency and ent.text in replaced_ents:
                new_ent = replaced_ents[ent.text]
            else:
                if isinstance(ent_dict[ent.label_], Generator):
                    new_ent = next(ent_dict[ent.label_])  # type: ignore
                else:
                    new_ent = random.sample(ent_dict[ent.label_], k=1)[  # type: ignore
                        0
                    ]
                if replace_consistency:
                    replaced_ents[ent.text] = new_ent

            normalized_ent = __normalize_entity(new_ent, nlp)
            new_ent = normalized_ent["ORTH"]
            spacing = normalized_ent["SPACY"]
            str_ent = normalized_ent["STR"]

            # Handle token annotations
            len_ent = len(new_ent)
            str_len_ent = len(str_ent)
            ent_range = (ent.start + offset, ent.end + offset)
            i = slice(*ent_range)
            tok_anno["ORTH"][i] = new_ent
            tok_anno["LEMMA"][i] = normalized_ent["LEMMA"]

            tok_anno["POS"][i] = normalized_ent["POS"]
            tok_anno["TAG"][i] = normalized_ent["TAG"]

            tok_anno["MORPH"][i] = normalized_ent["MORPH"]
            tok_anno["DEP"][i] = [ent[0].dep_] + ["flat"] * (len_ent - 1)

            # Set sentence start based on first token in previous entity
            tok_anno["SENT_START"][i] = [ent[0].sent_start] + [0] * (len_ent - 1)

            # set the last spacing to be equal to the last token spacing in the previous entity
            spacing[-1:] = [ent[-1].whitespace_]
            tok_anno["SPACY"][i] = spacing

            entity_offset = len_ent - (ent.end - ent.start)
            entity_str_offset = str_len_ent - len(ent.text)
            if should_update_heads:
                # Handle HEAD

                head[head > ent.start + offset] += entity_offset
                # keep first head correcting for changing entity size, set rest to
                # refer to index of first name
                head = np.concatenate(
                    [
                        np.array(head[: ent.start + offset]),  # before
                        np.array(
                            [head[ent.root.i + offset]]
                            + [ent.start + offset] * (len_ent - 1),
                        ),  # the entity
                        np.array(head[ent.end + offset :]),  # after
                    ],
                )

            spans_anno = _update_span_annotations(
                spans_anno,
                ent,
                str_offset,
                entity_str_offset,
            )
            offset += entity_offset
            str_offset += entity_str_offset

            # Handle entities IOB tags
            if len_ent == 1:
                ents[i] = ["U-" + ent.label_]
            else:
                ents[i] = (
                    ["B-" + ent.label_]
                    + ["I-" + ent.label_] * (len_ent - 2)
                    + ["L-" + ent.label_]
                )

    if should_update_heads:
        tok_anno["HEAD"] = head.tolist()  # type: ignore
    else:
        tok_anno["HEAD"] = list(range(len(tok_anno["ORTH"])))

    text = make_text_from_orth(example_dict)

    doc = nlp.make_doc(text)
    yield Example.from_dict(doc, example_dict)


@registry.augmenters("ents_replace_v1")
def create_ent_augmenter_v1(
    level: float,
    ent_dict: Dict[str, Iterable[ENTITY]],
    replace_consistency: bool = True,
    resolve_dependencies: bool = True,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Create an augmenter which replaces an entity based on a dictionary
    lookup.

    Args:
        level: the percentage of entities to be augmented.
        ent_dict: A dictionary with keys corresponding
            the the entity type you wish to replace (e.g. "PER") and a itarable of the
            replacements entities. A replacement can be either 1) a list of string of the desired entity
            i.e. ["Kenneth", "Enevoldsen"], 2) a string of the desired entity i.e. "Kenneth Enevoldsen", this
            will be split using the tokenizer of the nlp pipeline, or 3) Span object with the desired entity, here all information will be passed
            on except for the dependency tree.
        replace_consistency: Should an entity always be replaced with
            the same entity? Defaults to True.
        resolve_dependencies: Attempts to resolve the dependency tree
            by setting head of the original entitity aa the head of the
            first token in the new entity. The remainder is the passed as
    Returns:
        The augmenter

    Example:
        >>> ent_dict = {"ORG": [["Google"], ["Apple"]],
        >>>             "PERSON": [["Kenneth"], ["Lasse", "Hansen"]]}
        >>> # augment 10% of names
        >>> ent_augmenter = create_ent_augmenter(ent_dict, level = 0.1)
    """
    return partial(
        ent_augmenter_v1,
        level=level,
        ent_dict=ent_dict,
        replace_consistency=replace_consistency,
        resolve_dependencies=resolve_dependencies,
    )


def generator_from_name_dict(
    names: Dict[str, List[str]],
    patterns: List[List[str]],
    names_p: Dict[str, List[float]],
    patterns_p: Optional[List[float]],
):
    """A utility function for create_pers_replace_augmenter, which creates an
    infinite generator based on a names dictionary and a list of patterns,
    where the string in the pattern correspond to the list in the pattern."""
    lp = len(patterns)

    while True:
        i = np.random.choice(lp, size=1, replace=True, p=patterns_p)[0]
        yield [
            str(np.random.choice(names[p], size=1, replace=True, p=names_p.get(p))[0])
            for p in patterns[i]
        ]


@registry.augmenters("per_replace_v1")
def create_per_replace_augmenter_v1(
    names: Dict[
        str,
        List[str],
    ],  # {"firstname": ["Kenneth", "Lasse"], "lastname": ["Enevoldsen", "Hansen"]}
    patterns: List[List[str]],  # ["firstname", "firstname", "lastname"]
    level: float,
    names_p: Dict[str, List[float]] = {},
    patterns_p: Optional[List[float]] = None,
    replace_consistency: bool = True,
    person_tag: str = "PERSON",
) -> Callable[[Language, Example], Iterator[Example]]:
    """Create an augmenter which replaces a name (PER) with a news sampled from
    the names dictionary.

    Args:
        names: A dictionary of list of names to sample from.
            These could for example include first name and last names.
        pattern: The pattern to create the names. This should be a
            list of patterns.
            Where a pattern is a list of strings, where the string denote the list in
            the names dictionary in which to sample from.
        level: The proportion of PER entities to replace.
        names_p: The probability to sample each name.
            Defaults to {}, indicating equal probability for each name.
        patterns_p: The probability to sample each
            pattern. Defaults to None, indicating equal probability for each pattern.
        replace_consistency: Should the entity always be replaced with
            the same entity? Defaults to True.
        person_tag: The tag of the person entity. Defaults to "PERSON".
            However it should be noted that much such as the Danish spacy model uses
            "PER" instead.

    Returns:
        The augmenter

    Example:
        >>> names = {"firstname": ["Kenneth", "Lasse"],
        >>>          "lastname": ["Enevoldsen", "Hansen"]}
        >>> patterns = [["firstname"], ["firstname", "lastname"],
        >>>             ["firstname", "firstname", "lastname"]]
        >>> person_tag = "PERSON"
        >>> # replace 10% of names:
        >>> per_augmenter = create_per_replace_augmenter(names, patterns, level=0.1,
        >>>                                              person_tag=person_tag)
    """

    names_gen = generator_from_name_dict(names, patterns, names_p, patterns_p)

    return create_ent_augmenter_v1(
        ent_dict={person_tag: names_gen},
        level=level,
        replace_consistency=replace_consistency,
    )


def ent_format_augmenter_v1(
    nlp: Language,
    example: Example,
    reordering: List[Union[int, None]],
    formatter: List[Union[Callable[[Token], str], None]],
    level: float,
    ent_types: Optional[List[str]] = None,
) -> Iterator[Example]:
    example_dict = example.to_dict()

    tok_anno = example_dict["token_annotation"]

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
            new_ent_ = [
                e.text if f is None else f(e) for e, f in zip(new_ent, formatter)
            ]

            if len(new_ent_) < len(new_ent):
                new_ent_ += [e.text for e in new_ent[len(new_ent_) :]]

            tok_anno["ORTH"][ent.start : ent.end] = new_ent_
            tok_anno["LEMMA"][ent.start : ent.end] = new_ent_

    text = make_text_from_orth(example_dict)

    doc = nlp.make_doc(text)
    yield Example.from_dict(doc, example_dict)


@registry.augmenters("ents_format_v1")
def create_ent_format_augmenter_v1(
    reordering: List[Union[int, None]],
    formatter: List[Union[Callable[[Token], str], None]],
    level: float,
    ent_types: Optional[List[str]] = None,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter which reorders and formats a entity according to
    reordering and formatting functions.

    Args:
        reordering: A reordering consisting of a the desired
            order of the list of indices, where None denotes the remainder. For
            instance if this function was solely used on names [-1, None] indicate last
            name (the last token in the name) followed by the remainder of the name.
            Similarly one could more use the reordering [3, 1, 2] e.g. indicating last
            name, first name, middle name. Note that if the entity only include two
            tokens the 3 will be ignored producing the pattern [1, 2].
        formatter: A list of function
            taking in a spaCy Token returning the reformatted str. E.g. the function
            `lambda token: token.text[0] + "."` would abbreviate the token and add
            punctuation. None corresponds to no augmentation.
        level: The probability of an entities being augmented.
        ent_types:  The entity types which should
            be augmented. Defaults to None, indicating all entity types.

    Returns:
        The augmenter

    Example:
        >>> import augmenty
        >>> import spacy
        >>> nlp = spacy.load("en_core_web_sm")
        >>> abbreviate = lambda token: token.text[0] + "."
        >>> augmenter = augmenty.load("ents_format_v1", reordering = [-1, None],
        >>>                           formatter=[None, abbreviate], level=1,
        >>>                            ent_types=["PER"])
        >>> texts = ["my name is Kenneth Enevoldsen"]
        >>> list(augmenty.texts(texts, augmenter, nlp))
        ["my name is Enevoldsen K."]
    """
    return partial(
        ent_format_augmenter_v1,
        reordering=reordering,
        formatter=formatter,
        level=level,
        ent_types=ent_types,
    )
