import time

import spacy
from spacy.lang.da import Danish
from spacy.lang.en import English

from dacy.datasets import dane

import augmenty

import pytest
from .books import BOOKS


@pytest.fixture()
def nlp():
    nlp = spacy.load("en_core_web_md")
    return nlp


@pytest.fixture()
def nlp_da():
    nlp = Danish()
    return nlp


@pytest.fixture()
def nlp_en():
    nlp = English()
    return nlp


@pytest.fixture()
def examples(nlp_da):
    test = dane(splits=["test"])
    return [e for e in test(nlp_da)]


import numpy as np
np.seterr(divide='ignore', invalid='ignore')

def test_all(nlp, examples, nlp_en, nlp_da):
    def is_pronoun(token):
        if token.pos_ == "PRON":
            return True
        return False

    abbreviate = lambda token: token.text[0] + "."

    # augmenter args
    augmenters_args = {
        "char_replace.v1": {"replace": {"ss": "ß"}},
        "char_replace_random.v1": {},
        "char_swap.v1": {},
        "conditional_token_casing.v1": {"conditional": is_pronoun, "lower": False},
        "da_historical_noun_casing.v1": {},
        "da_æøå_replace.v1": {},
        "ents_format.v1": {
            "reordering": [-1, None],
            "formatter": [None, abbreviate],
            "ent_types": ["PER"],
        },
        "ents_replace.v1": {
            "ent_dict": {
                "ORG": [["Google"], ["Apple"]],
                "PERSON": [["Kenneth"], ["Lasse", "Hansen"]],
            }
        },
        "grundtvigian_spacing_augmenter.v1": {},
        "keystroke_error.v1": {},
        "per_replace.v1": {
            "names": {
                "firstname": ["Kenneth", "Lasse"],
                "lastname": ["Enevoldsen", "Hansen"],
            },
            "patterns": [
                ["firstname"],
                ["firstname", "lastname"],
                ["firstname", "firstname", "lastname"],
            ],
        },
        "random_casing.v1": {},
        "random_starting_case.v1": {},
        "remove_spacing.v1": {},
        "spacing_insertion.v1": {},
        "spacy.lower_case.v1": {},
        "spongebob.v1": {},
        "token_dict_replace.v1": {
            "replace": {
                "act": {"VERB": ["perform", "move"], "NOUN": ["action", "deed"]}
            }
        },
        "token_swap.v1": {},
        "upper_case.v1": {},
        "word_embedding.v1": {"nlp": nlp},
        "wordnet_synonym.v1": {},
    }

    ignore = ["spacy.orth_variants.v1", "token_replace.v1"]

    for aug_name in augmenty.augmenters():
        print(aug_name, end="")
        s = time.time()
        if aug_name in ignore:
            continue
        args = augmenters_args[aug_name]
        for level in [0.1, 0.5, 1]:
            args["level"] = level
            aug = augmenty.load(aug_name, **args)

            # English no processing
            texts = list(augmenty.texts(BOOKS, aug, nlp=nlp_en))

            # English w. processing
            texts = list(augmenty.texts(BOOKS, aug, nlp=nlp_en))

            # tagged dataset
            augmented_examples = [
                e for ex in examples for e in aug(nlp=nlp_da, example=ex)
            ]
        print(": ", time.time() - s)
