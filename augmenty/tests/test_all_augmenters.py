import spacy
from spacy.lang.da import Danish
from spacy.lang.en import English
from spacy.training import Example

from dacy.datasets import dane

import augmenty

import pytest
from .books import BOOKS


import numpy as np

np.seterr(divide="raise", invalid="raise")


#### > should be import
def texts_to_example(texts, nlp):
    docs = nlp.pipe(texts)
    for doc in docs:
        yield Example(doc, doc)


nlp_en_md = spacy.load("en_core_web_md")
nlp_da = Danish()
nlp_en = English()

dane_test = dane(splits=["test"])(nlp_da)


def is_pronoun(token):
    if token.pos_ == "PRON":
        return True
    return False


abbreviate = lambda token: token.text[0] + "."


ignore = {"spacy.orth_variants.v1", "token_replace.v1", "token_insert.v1"}

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
        "replace": {"act": {"VERB": ["perform", "move"], "NOUN": ["action", "deed"]}}
    },
    "token_swap.v1": {},
    "upper_case.v1": {},
    "word_embedding.v1": {"nlp": nlp_en_md},
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
        (dane_test, nlp_da),
        (list(texts_to_example(BOOKS, nlp=nlp_en)), nlp_en),
        (list(texts_to_example(BOOKS, nlp=nlp_en_md)), nlp_en_md),
    ],
)
def test_augmenters(aug, args, examples, nlp, level):
    args["level"] = level
    aug = augmenty.load(aug, **args)
    augmented_examples = [e for ex in examples for e in aug(nlp=nlp, example=ex)]


def test_check_untested():
    for aug_name in augmenty.augmenters():
        assert aug_name in augmenters_args or aug_name in ignore
