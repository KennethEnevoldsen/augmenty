import random
from functools import partial
from typing import Callable, Dict, Iterable, Iterator, List, Optional, Union

import numpy as np

import spacy
from spacy.language import Language
from spacy.training import Example

from ..augment_utilites import make_text_from_orth



def ent_augmenter(
    nlp: Language,
    example: Example,
    ent_dict: Dict[str, Iterable[List[str]]], # {"ORG": [["Google"], ["Apple"]], "PER": [["Kenneth"], ["Lasse", "Hansen"]]}
    level: float,
) -> Iterator[Example]:
    # ensure Kenneth -> Lars and not Kenneth -> Lars and Kenneth -> Peter
    replaced_ents = {}
    example_dict = example.to_dict()

    for ent in example.y.ents:
        if ent.label_ in ent_dict:
            if ent.text in replaced_ents:
                new_ent = replaced_ents[ent.text]
            else:
                new_ent =  random.sample(ent_dict[ent.label_], k=1)[0]
                replaced_ents[ent.text] = new_ent

        for token in dict
        (ent.start, ent.end)



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


    text = make_text_from_orth(example_dict)

    doc = nlp.make_doc(text)
    yield Example.from_dict(doc, example_dict)



def pers_replace_augmenter(
    nlp: Language,
    example: Example,
    names: Dict[str, Iterable[str]], # {"firstname": ["Kenneth", "Lasse"], "lastname": ["Enevoldsen", "Hansen"]}
    pattern: List[str], #["firstname", "firstname", "lastname"]
    level: float,
) -> Iterator[Example]:
    pass
    # ensure Kenneth -> Lars and not Kenneth -> Lars and Kenneth -> Peter
    # create utility functions for abbrpunct and abbr from list.

def pers_format_augmenter(
    nlp: Language,
    example: Example,
    pattern: List[str], # firstname, lastname, abpunct_fn, abpunct_ln, abbr_ln, abbr_fn
    # reordering
    # abbreviate, abbraviate punct, dont abbreviate
    reordering: List[Union[int, None]], # e.g. [-1, None] -1 == last name, None == the rest, or [3, 1, 2] last name, first name, middle name.
    # if the name is only two long the 3 is ignored.
    level: float,
) -> Iterator[Example]:
    pass