"""Pytest script for testing all augmenters in a variety of cases."""

import numpy as np
import pytest

import augmenty

from .fixtures import books_without_annotations  # noqa
from .fixtures import nlp_en  # noqa
from .fixtures import books_w_annotations, dane_test, nlp_da, nlp_en_md  # noqa

np.seterr(divide="raise", invalid="raise")


def is_pronoun(token):
    if token.pos_ == "PRON":
        return True
    return False


abbreviate = lambda token: token.text[0] + "."  # noqa: E731


ignore = {
    "spacy.orth_variants.v1",
    "token_replace_v1",
    "token_insert_v1",
    "paragraph_subset_augmenter_v1",
    "word_embedding_v1",
    "spacy.combined_augmenter.v1",
}

augmenters_args = {
    "char_replace_v1": {"replace": {"ss": "ß"}},
    "char_replace_random_v1": {},
    "char_swap_v1": {},
    "conditional_token_casing_v1": {"conditional": is_pronoun, "lower": False},
    "da_historical_noun_casing_v1": {},
    "da_æøå_replace_v1": {},
    "ents_format_v1": {
        "reordering": [-1, None],
        "formatter": [None, abbreviate],
        "ent_types": ["PER"],
    },
    "ents_replace_v1": {
        "ent_dict": {
            "ORG": [["Google"], ["Apple"]],
            "PERSON": [["Kenneth"], ["Lasse", "Hansen"]],
        },
    },
    "letter_spacing_augmenter_v1": {},
    "keystroke_error_v1": {},
    "per_replace_v1": {
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
    "random_casing_v1": {},
    "random_starting_case_v1": {},
    "remove_spacing_v1": {},
    "spacing_insertion_v1": {},
    "spacy.lower_case.v1": {},
    "spongebob_v1": {},
    "token_dict_replace_v1": {
        "replace": {"act": {"VERB": ["perform", "move"], "NOUN": ["action", "deed"]}},
    },
    "token_swap_v1": {},
    "upper_case_v1": {},
    "wordnet_synonym_v1": {},
    "random_synonym_insertion_v1": {"context_window": 5, "verbose": False},
    "duplicate_token_v1": {},
    "token_insert_random_v1": {},
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
    ],
)
def test_augmenters(aug, args, examples, nlp, level):
    args["level"] = level
    aug = augmenty.load(aug, **args)
    augmented_examples = [  # noqa
        e for ex in examples for e in aug(nlp=nlp, example=ex)
    ]


def test_check_untested():
    for aug_name in augmenty.augmenters():
        assert (aug_name in augmenters_args) or (aug_name in ignore)
