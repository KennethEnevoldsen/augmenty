"""
Pytest script for testing all augmenters in a variety of cases.
"""

import pytest

import augmenty

import numpy as np

from .fixtures import (  # noqa
    nlp_en,
    nlp_da,
    nlp_en_md,
    books_w_annotations,
    books_without_annotations,
    dane_test,
)

np.seterr(divide="raise", invalid="raise")


def is_pronoun(token):
    if token.pos_ == "PRON":
        return True
    return False


abbreviate = lambda token: token.text[0] + "."


ignore = {
    "spacy.orth_variants.v1",
    "token_replace.v1",
    "token_insert.v1",
    "paragraph_subset_augmenter.v1",
    "word_embedding.v1",
}

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
    "letter_spacing_augmenter.v1": {},
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
        "replace": {"act": {"VERB": ["perform", "move"], "NOUN": ["action", "deed"]}}
    },
    "token_swap.v1": {},
    "upper_case.v1": {},
    "wordnet_synonym.v1": {},
    "random_synonym_insertion.v1": {"context_window": 5, "verbose": False},
    "duplicate_token.v1": {},
    "token_insert_random.v1": {},
}


@pytest.mark.parametrize("aug,args", [(k, augmenters_args[k]) for k in augmenters_args])
@pytest.mark.parametrize("level", [0.1, 0.5, 1])
@pytest.mark.timeout(100)
@pytest.mark.parametrize(
    "examples,nlp",
    [
        (pytest.lazy_fixture("dane_test"), pytest.lazy_fixture("nlp_da")),
        (
            pytest.lazy_fixture("books_without_annotations"),
            pytest.lazy_fixture("nlp_en"),
        ),
        # (pytest.lazy_fixture("books_w_annotations"), pytest.lazy_fixture("nlp_en_md")),
    ],
)
def test_augmenters(aug, args, examples, nlp, level):
    args["level"] = level
    aug = augmenty.load(aug, **args)
    augmented_examples = [e for ex in examples for e in aug(nlp=nlp, example=ex)]


def test_check_untested():
    for aug_name in augmenty.augmenters():
        assert (aug_name in augmenters_args) or (aug_name in ignore)
