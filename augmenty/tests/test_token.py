import spacy
from spacy.lang.da import Danish
from spacy.lang.en import English
from spacy.tokens import Doc

import augmenty

import pytest

from .books import BOOKS


@pytest.fixture()
def nlp():
    nlp = spacy.load("en_core_web_sm")
    return nlp


def test_create_starting_case_augmenter(nlp):
    text = "some of the start cases here should not be lowercased. There is naturally a chance that it might not end up that way, but it should be very very very rare."

    aug = spacy.registry.augmenters.get("random_starting_case.v1")(level=1)
    doc = nlp(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp)
    assert next(docs).text != text


def test_create_conditional_token_casing_augmenter(nlp):
    tokens = ["Jeg", "ejer", "en", "hund"]
    pos = ["PRON", "VERB", "DET", "NOUN"]
    spaces = [True, True, True, False]
    solution = "jeg ejer en hund"

    doc = Doc(nlp.vocab, words=tokens, pos=pos, spaces=spaces)

    def conditional(token):
        if token.pos_ == "PRON":
            return True
        return False

    aug = spacy.registry.augmenters.get("conditional_token_casing.v1")(
        level=1, lower=True, conditional=conditional
    )

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp)
    assert next(docs).text == solution


def test_create_token_dict_replace_augmenter(nlp):

    doc1 = Doc(
        nlp.vocab, words=["I", "am", "happy", "!"], spaces=[True, True, False, False]
    )
    doc2 = Doc(
        nlp.vocab,
        words=["Look", "a", "flat", "door", "!"],
        pos=["", "", "ADJ", "", ""],
        spaces=[True, True, True, False, False],
    )

    aug = spacy.registry.augmenters.get("token_dict_replace.v1")(
        level=1,
        replace={
            "happy": ["cheery", "joyful"],
            "flat": {"ADJ": ["level"], "ADV": ["firmly"]},
        },
    )

    docs = augmenty.docs([doc1, doc2], augmenter=aug, nlp=nlp)
    assert next(docs).text in ["I am cheery!", "I am joyful!"]
    assert next(docs).text == "Look a level door!"


def test_create_wordnet_synonym_augmenter(nlp):
    text = "Skal jeg pande dig en?"
    nlp_da = Danish()

    aug = spacy.registry.augmenters.get("wordnet_synonym.v1")(level=1, lang="da", respect_pos=False)
    doc = nlp_da(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_da)
    assert next(docs)[2].text in ["stegepande"]

    aug = spacy.registry.augmenters.get("wordnet_synonym.v1")(level=1, lang="da")
    docs = nlp.pipe(BOOKS)
    docs = list(augmenty.docs(docs, augmenter=aug, nlp=nlp))

    text = "Det kan jeg ikke slå"
    doc = nlp_da(text)
    doc[-1].pos_ = "VERB"
    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_da)
    assert next(docs)[-1].text in ["pulsere", "banke"]


def test_create_grundtvigian_spacing_augmenter(nlp):
    text = "not very happy"

    aug = spacy.registry.augmenters.get("grundtvigian_spacing_augmenter.v1")(level=1)
    doc = nlp(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp)

    assert next(docs).text == "n o t v e r y h a p p y"


def test_create_spacing_insertion_augmenter(nlp):
    text = "test"

    aug = augmenty.load("spacing_insertion.v1", level=1, max_insertions=1)
    doc = nlp(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp)

    assert next(docs)[0].text == "t est"

    aug = augmenty.load("spacing_insertion.v1", level=1, max_insertions=2)
    doc = nlp(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp)

    assert next(docs)[0].text == "t e st"


def test_create_token_swap_augmenter(nlp):

    doc1 = Doc(
        nlp.vocab,
        words=["I", "am", "happy", "!", "New"],
        sent_starts=[True, False, False, False, True],
    )
    doc2 = Doc(
        nlp.vocab,
        words=["I", "am", "happy", "!", "New"],
        ents=["O", "B-PER", "I-PER", "O", "O"],
        sent_starts=[True, False, False, False, True],
    )

    aug = spacy.registry.augmenters.get("token_swap.v1")(level=1)

    docs = augmenty.docs([doc1, doc2], augmenter=aug, nlp=nlp)
    assert next(docs).text in ["I happy am ! New ", "am I happy ! New "]
    assert next(docs).text in ["I happy am ! New ", "I am happy ! New "]


def test_create_word_embedding_augmenter():
    nlp = spacy.load("en_core_web_md")
    text = "cat"

    doc = nlp(text)
    
    aug = augmenty.load("word_embedding.v1", level=1)
    docs = list(augmenty.docs([doc], augmenter=aug, nlp=nlp))
    assert docs[0].text in ['FELINE', 'cats', 'FELINES', 'TABBY', 'KENNEL', 'dog', 'kitty', 'sanrio', 'pet']

    aug = augmenty.load("word_embedding.v1", level=1, ignore_casing=False)
    docs = list(augmenty.docs([doc], augmenter=aug, nlp=nlp))
    assert docs[0].text in ['FELINE', 'cats', 'FELINES', 'TABBY', 'KENNEL', 'dog', 'kitty', 'sanrio', 'pet']

    aug = augmenty.load("word_embedding.v1", level=1, nlp=nlp)
    docs = list(augmenty.docs([doc], augmenter=aug, nlp=nlp))
    assert docs[0].text in ['FELINE', 'cats', 'FELINES', 'TABBY', 'KENNEL', 'dog', 'kitty', 'sanrio', 'pet']
