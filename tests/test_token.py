import spacy  # type: ignore
from spacy.tokens import Doc  # type: ignore

import augmenty
from augmenty.token.insert import create_token_insert_random_augmenter_v1

from .books import BOOKS
from .fixtures import nlp_da, nlp_en, nlp_en_md  # noqa


def test_create_starting_case_augmenter(nlp_en):  # noqa F811
    text = (
        "some of the start cases here should not be lowercased."
        + " There is naturally a chance that it might not end up that way, but it"
        + " should be very very very rare."
    )

    aug = spacy.registry.augmenters.get("random_starting_case_v1")(level=1)
    doc = nlp_en(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_en)
    assert next(docs).text != text


def test_create_conditional_token_casing_augmenter(nlp_en):  # noqa F811
    tokens = ["Jeg", "ejer", "en", "hund"]
    pos = ["PRON", "VERB", "DET", "NOUN"]
    spaces = [True, True, True, False]
    solution = "jeg ejer en hund"

    doc = Doc(nlp_en.vocab, words=tokens, pos=pos, spaces=spaces)

    def conditional(token):
        if token.pos_ == "PRON":
            return True
        return False

    aug = spacy.registry.augmenters.get("conditional_token_casing_v1")(
        level=1,
        lower=True,
        conditional=conditional,
    )

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_en)
    assert next(docs).text == solution


def test_create_token_dict_replace_augmenter(nlp_en):  # noqa F811
    doc1 = Doc(
        nlp_en.vocab,
        words=["I", "am", "happy", "!"],
        spaces=[True, True, False, False],
    )
    doc2 = Doc(
        nlp_en.vocab,
        words=["Look", "a", "flat", "door", "!"],
        pos=["", "", "ADJ", "", ""],
        spaces=[True, True, True, False, False],
    )

    aug = spacy.registry.augmenters.get("token_dict_replace_v1")(
        level=1,
        replace={
            "happy": ["cheery", "joyful"],
            "flat": {"ADJ": ["level"], "ADV": ["firmly"]},
        },
    )

    docs = augmenty.docs([doc1, doc2], augmenter=aug, nlp=nlp_en)
    assert next(docs).text in ["I am cheery!", "I am joyful!"]
    assert next(docs).text == "Look a level door!"


def test_create_wordnet_synonym_augmenter(nlp_en, nlp_da):  # noqa F811
    text = "Skal jeg pande dig en?"

    aug = spacy.registry.augmenters.get("wordnet_synonym_v1")(
        level=1,
        lang="da",
        respect_pos=False,
    )
    doc = nlp_da(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_da)
    assert next(docs)[2].text in ["stegepande"]

    aug = spacy.registry.augmenters.get("wordnet_synonym_v1")(level=1, lang="da")
    docs = nlp_en.pipe(BOOKS)
    docs = list(augmenty.docs(docs, augmenter=aug, nlp=nlp_en))

    text = "Det kan jeg ikke slå"
    doc = nlp_da(text)
    doc[-1].pos_ = "VERB"
    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_da)
    assert next(docs)[-1].text in ["pulsere", "banke"]


def test_create_letter_spacing_augmenter(nlp_en):  # noqa F811
    text = "not very happy"

    aug = spacy.registry.augmenters.get("letter_spacing_augmenter_v1")(level=1)
    doc = nlp_en(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_en)

    assert next(docs).text == "n o t v e r y h a p p y"


def test_create_spacing_insertion_augmenter(nlp_en):  # noqa F811
    text = "test"

    aug = augmenty.load("spacing_insertion_v1", level=1, max_insertions=1)
    doc = nlp_en(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_en)

    assert next(docs)[0].text == "t est"

    aug = augmenty.load("spacing_insertion_v1", level=1, max_insertions=2)
    doc = nlp_en(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_en)

    assert next(docs)[0].text == "t e st"


def test_create_token_swap_augmenter(nlp_en):  # noqa F811
    doc1 = Doc(
        nlp_en.vocab,
        words=["I", "am", "happy", "!", "New"],
        sent_starts=[True, False, False, False, True],
    )
    doc2 = Doc(
        nlp_en.vocab,
        words=["I", "am", "happy", "!", "New"],
        ents=["O", "B-PER", "I-PER", "O", "O"],
        sent_starts=[True, False, False, False, True],
    )

    aug = spacy.registry.augmenters.get("token_swap_v1")(level=1)

    docs = augmenty.docs([doc1, doc2], augmenter=aug, nlp=nlp_en)
    assert next(docs).text in ["I happy am ! New ", "am I happy ! New "]
    assert next(docs).text in ["I happy am ! New ", "I am happy ! New "]


def test_create_word_embedding_augmenter(nlp_en_md):  # noqa F811
    text = "cat"

    doc = nlp_en_md(text)

    rep = [
        "cat",
        "dog",
        "cats",
        "kitty",
        "pet",
        "puppy",
        "dogs",
        "rabbit",
        "squirrel",
        "fox",
        "bunny",
        "rabbits",
    ]

    aug = augmenty.load("word_embedding_v1", level=1)
    docs = list(augmenty.docs([doc], augmenter=aug, nlp=nlp_en_md))
    assert docs[0].text.lower() in rep

    aug = augmenty.load("word_embedding_v1", level=1, ignore_casing=False)
    docs = list(augmenty.docs([doc], augmenter=aug, nlp=nlp_en_md))
    assert docs[0].text.lower() in rep

    aug = augmenty.load("word_embedding_v1", level=1, nlp=nlp_en_md)
    docs = list(augmenty.docs([doc], augmenter=aug, nlp=nlp_en_md))
    assert docs[0].text.lower() in rep


def test_create_token_insert_augmenter(nlp_en):  # noqa F811
    words = ["cat"]
    spaces = [False]
    doc = Doc(nlp_en.vocab, words=words, spaces=spaces, pos=["NOUN"])
    insert_fun = lambda t: {"ORTH": "word"}  # noqa: E731
    aug = augmenty.load("token_insert_v1", level=1, insert=insert_fun)
    docs = list(augmenty.docs([doc], augmenter=aug, nlp=nlp_en))
    assert len(docs[0]) == 2
    assert docs[0][0].text == "word"


def test_create_token_insert_random_augmenter(nlp_en):  # noqa F811
    texts = ["one two three"] * 3
    # w. word list
    aug = create_token_insert_random_augmenter_v1(
        level=0.5,
        insert=["words", "to", "insert"],
    )
    list(augmenty.texts(texts, aug, nlp_en))
    # w. dict
    aug = create_token_insert_random_augmenter_v1(
        level=0.5,
        insert=[
            {
                "ORTH": "replacements",
                "LEMMA": "replacement",
                "POS": "NOUN",
                "TAG": "NOUN",
                "entities": "O",
                "MORPH": "Number=Plur",
            },
        ],
    )
    list(augmenty.texts(texts, augmenter=aug, nlp=nlp_en))
    # w. None (i.e. vocab)
    aug = create_token_insert_random_augmenter_v1(level=0.5)
    list(augmenty.texts(texts, augmenter=aug, nlp=nlp_en))


def test_create_duplicate_token_augmenter(nlp_en, nlp_en_md):  # noqa F811
    words = ["cat"]
    spaces = [False]
    doc = Doc(nlp_en.vocab, words=words, spaces=spaces)
    aug = augmenty.load("duplicate_token_v1", level=1)
    docs = list(augmenty.docs([doc], augmenter=aug, nlp=nlp_en))
    assert len(docs[0]) == 2
    assert docs[0][0].text == "cat"
    assert docs[0][1].text == "cat"
    docs = list(
        augmenty.docs(nlp_en_md("I am not happy"), augmenter=aug, nlp=nlp_en_md),
    )


def test_create_random_synonym_insertion_augmenter(nlp_en):  # noqa F811
    words = ["cat"]
    spaces = [False]
    doc = Doc(nlp_en.vocab, words=words, spaces=spaces, pos=["NOUN"])
    aug = augmenty.load("random_synonym_insertion_v1", level=1)
    docs = list(augmenty.docs([doc], augmenter=aug, nlp=nlp_en))
    assert len(docs[0]) == 2
    assert docs[0][1].text == "cat"
    assert docs[0][1].pos_ == "NOUN"
