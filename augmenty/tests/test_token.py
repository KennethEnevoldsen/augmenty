import spacy
from spacy.lang.da import Danish
from spacy.tokens import Doc

from augmenty import augment_docs


def test_create_starting_case_augmenter(nlp):
    text = "some of the start cases here should not be lowercased. There is naturally a chance that it might not end up that way, but it should be very very very rare."

    aug = spacy.augmenters.get("random_starting_case.v1")(level=1)
    doc = nlp(text)

    docs = augment_docs([doc], augmenter=aug, nlp=nlp)
    assert next(docs).text != text


def test_create_conditional_token_casing_augmenter(nlp):
    tokens = ["Jeg", "ejer", "en", "hund"]
    pos = ["PRON", "VERB", "DET", "NOUN"]
    solution = "jeg ejer en hund"

    doc = Doc(nlp.vocab, words=tokens, pos=pos)

    def conditional(token):
        if token.pos_ == "PRON":
            return True
        return False

    aug = spacy.augmenters.get("conditional_token_casing.v1")(
        level=1, lower=True, conditional=conditional
    )

    docs = augment_docs([doc], augmenter=aug, nlp=nlp)
    assert next(docs).text == solution


def test_create_token_replace_augmenter(nlp):

    doc1 = Doc(nlp.vocab, words=["I", "am", "happy", "!"])
    doc2 = Doc(
        nlp.vocab,
        words=["Look", "a", "flat", "door", "!"],
        pos=["", "", "", "ADJ", "", ""],
    )

    aug = spacy.augmenters.get("token_replace.v1")(
        level=1,
        replace={
            "happy": ["cheery", "joyful"],
            "flat": {"ADJ": ["level"], "ADV": ["firmly"]},
        },
    )

    docs = augment_docs([doc1, doc2], augmenter=aug, nlp=nlp)
    assert next(docs).text in ["I am cheery!", "I am joyful!"]
    assert next(docs).text != "Look a level door!"


def test_create_wordnet_synonym_augmenter():
    text = "Skal jeg pande dig en?"
    nlp = Danish()

    aug = spacy.augmenters.get("wordnet_synonym.v1")(level=1)
    doc = nlp(text)

    docs = augment_docs([doc], augmenter=aug, nlp=nlp)
    assert next(docs)[2] in ["pande", "stegepande"]


def test_create_grundtvigian_spacing_augmenter(nlp):
    text = "not very happy"

    aug = spacy.augmenters.get("grundtvigian_spacing_augmenter.v1")(level=1)
    doc = nlp(text)

    docs = augment_docs([doc], augmenter=aug, nlp=nlp)

    assert next(docs).text == "n o t v e r y h a p p y"


def test_create_grundtvigian_spacing_augmenter(nlp):
    text = "test"

    aug = spacy.augmenters.get("spacing_insertion.v1")(level=1, max_insertions=1)
    doc = nlp(text)

    docs = augment_docs([doc], augmenter=aug, nlp=nlp)

    assert next(docs)[0].text == "t est"

    aug = spacy.augmenters.get("spacing_insertion.v1")(level=1, max_insertions=2)
    doc = nlp(text)

    docs = augment_docs([doc], augmenter=aug, nlp=nlp)

    assert next(docs)[0].text == "t e st"


def test_create_token_swap_augmenter(nlp):

    doc1 = Doc(nlp.vocab, words=["I", "am", "happy", "!"])
    doc2 = Doc(
        nlp.vocab, words=["I", "am", "happy", "!"], ents=["", "", "B-PER", "I-PER", ""]
    )

    aug = spacy.augmenters.get("token_swap.v1")(level=1)

    docs = augment_docs([doc1, doc2], augmenter=aug, nlp=nlp)
    assert next(docs).text in ["I happy am!", "am I happy!"]
    assert next(docs).text == "I happy am!"
