"""
Augmentation function for SpaCy which augments persons (PER) entities.
"""

import random
from functools import partial
from typing import Callable, Dict, Iterator, List, Optional

import numpy as np

import spacy
from spacy.language import Language
from spacy.training import Example

from ..augment_utilites import make_text_from_orth


@spacy.registry.augmenters("pers_augmenter.v1")
def create_pers_augmenter(
    ent_dict: Dict[str, List[str]],
    patterns: List[str],
    force_pattern_size: bool,
    keep_name: bool,
    patterns_prob: Optional[List[float]] = None,
    prob: float = 1,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Create person augmenter

    Args:
        ent_dict (Dict[str, List[str]]): A dictionary with keys "first_name" and "last_name". Values should be a list of names to sample from.
        patterns (List[str]): The patterns to replace names with. Should be a list of strings with each pattern in a string separated by a comma.
            Will choose one at random if more than one, optionally weighted by pattern_probs.
            Options: "fn", "ln", "abb", "abbpunct". .
            "fn" = first name
            "ln" = last name
            "abb" = abbreviate to first character (e.g. Lasse -> L)
            "abbpunct" = abbreviate to first character including punctuation (e.g. Lasse -> L.).
            Patterns can be arbitrarily combined, e.g. ["fn,ln", "abbpunct,ln,ln,ln"]
        force_pattern_size (bool): Whether to force entities to have the same format/length as the pattern. Defaults to False.
        keep_name (bool): Whether to use the current name or sample from ent_dict. I.e., if True, will only augment if the pattern is "abb" or "abbpunct",
            if False, will sample new names from ent_dict. Defaults to True.
        patterns_prob (List[float]). Weights for the patterns, must be None or have same lengths as pattern.
            Defaults to None (equal weights)
        prob (float, optional): which proportion of entities to augment. Defaults to 1.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter

    >>> from dacy.dataset import danish_names
    >>> name_dict = danish_names()
    >>> pers_aug = create_pers_augmenter(name_dict, patterns=["fn,ln","abbpunct,ln"], force_pattern_size=True, keep_name=False)
    """
    return partial(
        pers_augmenter,
        ent_dict=ent_dict,
        patterns=patterns,
        patterns_prob=patterns_prob,
        force_pattern_size=force_pattern_size,
        keep_name=keep_name,
        prob=prob,
    )


def pers_augmenter(
    nlp: Language,
    example: Example,
    ent_dict: Dict[str, List[str]],
    patterns: list,
    patterns_prob: Optional[List[float]],
    force_pattern_size: bool,
    keep_name: bool,
    prob: float,
) -> Iterator[Example]:
    example_dict = example.to_dict()

    # Get slices containing names
    entity_slices = get_ent_slices(example_dict["doc_annotation"]["entities"])
    # Extract tokens corresponding to names
    name_tokens = get_slice_spans(
        example_dict["token_annotation"]["ORTH"], entity_slices
    )
    # Augment names
    aug_ents = augment_entity(
        entities=name_tokens,
        ent_dict=ent_dict,
        patterns=patterns,
        patterns_prob=patterns_prob,
        force_pattern_size=force_pattern_size,
        keep_name=keep_name,
        prob=prob,
    )
    # Update fields in example dictionary to match changes
    example_dict = update_spacy_properties(example_dict, aug_ents, entity_slices)
    # Construct the text with augmented entities
    text = make_text_from_orth(example_dict)

    doc = nlp.make_doc(text)
    yield Example.from_dict(doc, example_dict)


def augment_entity(
    entities: List[List[str]],
    ent_dict: Dict[str, List[str]],
    patterns: List[str],
    patterns_prob: Optional[List[float]],
    force_pattern_size: bool,
    keep_name: bool,
    prob: float,
) -> List[List[str]]:
    """Augment entities. For each entity to augment, randomly sample a pattern
    and apply transformation to the entity. See create_pers_augmenter.

    Examples:
        >>> entities = [["Lasse", "Hansen"], ["Kenneth", "Christian", "Enevoldsen"]]
        >>> ent_dict = {"first_name" : ["John", "Ole"], "last_name" : ["Eriksen"]}
        >>> patterns = ["fn,ln", "abbpunct,ln"]
        >>> augment_entity(entities, ent_dict, patterns, None, force_pattern_size=False, keep_name=True, prob=1)
        [['L.', 'Hansen'], ['K.', 'Christian', 'Enevoldsen']]
        >>> augment_entity(entities, ent_dict, patterns, None, force_pattern_size=True, keep_name=True, prob=1)
        [['Lasse', 'Hansen'], ['K.', 'Christian']]
        >>> augment_entity(entities, ent_dict, patterns, None, force_pattern_size=True, keep_name=False, prob=1)
        [['Ole', 'Eriksen'], ['J.', 'Eriksen']]
        >>> augment_entity(entities, ent_dict, patterns, None, force_pattern_size=False, keep_name=False, prob=1)
        [['O.', 'Eriksen'], ['John', 'Eriksen', 'Enevoldsen']]

    Returns:
        List[List[str]]: Augmented names
    """

    if isinstance(patterns, str):
        patterns = [patterns]

    new_entity_spans = []

    patterns_dict = {
        "fn": sample_first_name,
        "ln": sample_last_name,
        "abb": sample_abbreviation,
        "abbpunct": sample_abbreviation_punct,
    }

    for i, _ in enumerate(entities):
        pattern = random.choices(patterns, weights=patterns_prob, k=1)[0]
        pattern = pattern.split(",")

        entity_span = entities[i]
        if force_pattern_size:
            entity_span = resize_entity_list(entity_span, pattern, ent_dict)

        new_entity = []

        for j, ent in enumerate(entity_span):
            if random.random() > prob:
                new_entity.append(ent)
            else:
                if j >= len(pattern):
                    new_entity.append(ent)
                else:
                    new_entity.append(
                        patterns_dict[pattern[j]](ent, keep_name, ent_dict)
                    )
        new_entity_spans.append(new_entity)
    return new_entity_spans


# Name sampling functions


def sample_first_name(name: str, keep_name: bool, name_dict: dict) -> str:
    if keep_name:
        return name
    return random.choice(name_dict["first_name"])


def sample_abbreviation(name: str, keep_name: bool, name_dict: dict) -> str:
    if keep_name:
        return name[0]
    return random.choice(name_dict["first_name"])[0]


def sample_abbreviation_punct(name: str, keep_name: bool, name_dict: dict) -> str:
    if keep_name:
        return name[0] + "."
    return random.choice(name_dict["first_name"])[0] + "."


def sample_last_name(name: str, keep_name: bool, name_dict: dict) -> str:
    if keep_name:
        return name
    return random.choice(name_dict["last_name"])


# Slicers


def get_ent_slices(entities: List[str], ent_type="PER") -> List[tuple]:
    slices = []

    start = None
    for i, ent in enumerate(entities):
        if ent.endswith(ent_type):
            if ent.startswith("U"):
                slices.append(tuple([i, i + 1]))
            if ent.startswith("B"):
                start = i
            if ent.startswith("L"):
                slices.append(tuple([start, i + 1]))
    return slices


def get_slice_spans(l: List[str], slices: List[tuple]):
    """Get the spans corresponding to some slices"""
    return [l[slice(s[0], s[1])] for s in slices]


def update_spacy_properties(
    example_dict: dict,
    augmented_entities: List[List[str]],
    entity_slices: List[tuple],
) -> dict:

    for k, v in example_dict["token_annotation"].items():
        example_dict["token_annotation"][k] = update_slice(
            k, v, augmented_entities, entity_slices
        )
    example_dict["doc_annotation"]["entities"] = update_slice(
        "entities",
        example_dict["doc_annotation"]["entities"],
        augmented_entities,
        entity_slices,
    )
    return example_dict


def update_slice(
    type: str,
    values: List[str],
    aug_ents: List[List[str]],
    entity_slices: List[tuple],
) -> List[str]:
    if type == "ORTH":
        return handle_orth(values, aug_ents, entity_slices)
    if type == "SPACY":
        return handle_spacy(values, aug_ents, entity_slices)
    if type == "TAG":
        return handle_tag(values, aug_ents, entity_slices)
    if type == "LEMMA":
        return handle_lemma(values, aug_ents, entity_slices)
    if type == "POS":
        return handle_pos(values, aug_ents, entity_slices)
    if type == "MORPH":
        return handle_morph(values, aug_ents, entity_slices)
    if type == "HEAD":
        return handle_head(values, aug_ents, entity_slices)
    if type == "DEP":
        return handle_dep(values, aug_ents, entity_slices)
    if type == "SENT_START":
        return handle_sent_start(values, aug_ents, entity_slices)
    if type == "entities":
        return handle_entities(values, aug_ents, entity_slices)


# Handlers for spacy properties


def handle_orth(
    values: List[str], aug_ents: List[List[str]], entity_slices: List[tuple]
) -> List[str]:
    """replace original entity with augmented entity"""
    running_add = 0
    for i, s in enumerate(entity_slices):
        values[slice(s[0] + running_add, s[1] + running_add)] = aug_ents[i]
        running_add += len(aug_ents[i]) - (s[1] - s[0])
    return values


def handle_spacy(
    values: List[str], aug_ents: List[List[str]], entity_slices: List[tuple]
) -> List[str]:
    running_add = 0
    for i, s in enumerate(entity_slices):
        values[s[0] + running_add : s[1] + running_add] = [True] * (
            len(aug_ents[i]) - 1
        ) + (  # fix last spacing
            values[s[0] + running_add : s[1] + running_add][-1:]
        )
        running_add += len(aug_ents[i]) - (s[1] - s[0])
    return values


def handle_tag(
    values: List[str], aug_ents: List[List[str]], entity_slices: List[tuple]
) -> List[str]:
    running_add = 0
    for i, s in enumerate(entity_slices):
        values[s[0] + running_add : s[1] + running_add] = ["PROPN"] * len(aug_ents[i])
        running_add += len(aug_ents[i]) - (s[1] - s[0])
    return values


def handle_lemma(
    values: List[str], aug_ents: List[List[str]], entity_slices: List[tuple]
) -> List[str]:
    return handle_orth(values, aug_ents, entity_slices)


def handle_pos(
    values: List[str], aug_ents: List[List[str]], entity_slices: List[tuple]
) -> List[str]:
    """keep first pos tag as original, add PROPN to rest"""
    running_add = 0
    for i, s in enumerate(entity_slices):
        values[s[0] + running_add : s[1] + running_add] = [
            values[slice(s[0] + running_add, s[1] + running_add)][0]
        ] + ["PROPN"] * (len(aug_ents[i]) - 1)
        running_add += len(aug_ents[i]) - (s[1] - s[0])
    return values


def handle_morph(
    values: List[str], aug_ents: List[List[str]], entity_slices: List[tuple]
) -> List[str]:
    running_add = 0
    for i, s in enumerate(entity_slices):
        values[s[0] + running_add : s[1] + running_add] = [""] * len(aug_ents[i])
        running_add += len(aug_ents[i]) - (s[1] - s[0])
    return values


def handle_head(
    values: List[str], aug_ents: List[List[str]], entity_slices: List[tuple]
) -> List[str]:
    """keep first head correcting for changing entity size, set rest to refer to index of first name"""
    values = np.array(values)

    offset = 0
    for aug_ent, s in zip(aug_ents, entity_slices):
        offset_ = len(aug_ent) - (s[1] - s[0])
        values[values > s[0] + offset] += offset_
        values = np.concatenate(
            [
                np.array(values[: s[0] + offset]),
                np.array(
                    [values[s[0] + offset]] + [s[0] + offset] * (len(aug_ent) - 1)
                ),
                np.array(values[s[1] + offset :]),
            ]
        )
        offset += offset_
    l = values.tolist()
    return l


def handle_dep(
    values: List[str], aug_ents: List[List[str]], entity_slices: List[tuple]
) -> List[str]:
    """Keep first dep tag, add flat to rest"""
    running_add = 0
    for i, s in enumerate(entity_slices):
        values[s[0] + running_add : s[1] + running_add] = [
            values[s[0] + running_add : s[1] + running_add][0]
        ] + ["flat"] * (len(aug_ents[i]) - 1)
        running_add += len(aug_ents[i]) - (s[1] - s[0])
    return values


def handle_sent_start(
    values: List[str], aug_ents: List[List[str]], entity_slices: List[tuple]
) -> List[str]:
    """keep first (if sent start), set rest to 0"""
    running_add = 0
    for i, s in enumerate(entity_slices):
        values[s[0] + running_add : s[1] + running_add] = [
            values[s[0] + running_add : s[1] + running_add][0]
        ] + [0] * (len(aug_ents[i]) - 1)
        running_add += len(aug_ents[i]) - (s[1] - s[0])
    return values


def handle_entities(
    values: List[str], aug_ents: List[List[str]], entity_slices: List[tuple]
) -> List[str]:
    running_add = 0
    for i, s in enumerate(entity_slices):
        len_aug_ent = len(aug_ents[i])
        if len_aug_ent == 1:
            values[s[0] + running_add : s[1] + running_add] = ["U-PER"]
        else:
            values[s[0] + running_add : s[1] + running_add] = (
                ["B-PER"] + ["I-PER"] * (len_aug_ent - 2) + ["L-PER"]
            )
        running_add += len_aug_ent - (s[1] - s[0])
    return values


def resize_entity_list(
    entity: List[str], pattern: List[str], ent_dict: dict
) -> List[str]:
    """Make the number of entities match the number of patterns.
    If less names in the entity list, sample random last name"""
    if len(entity) > len(pattern):
        return entity[: len(pattern)]
    return entity + [
        random.choice(ent_dict["last_name"]) for _ in range(len(pattern) - len(entity))
    ]
