import spacy
from augmenty import augment_docs
from spacy.lang.da import Danish


def test_create_random_casing_augmenter(nlp):
    text = "some of the start cases here should not be lowercased. There is naturally a chance that it might not end up that way, but it should be very very very rare."

    aug = spacy.augmenters.get("create_random_casing_augmenter.v1")(level=1)
    doc = nlp(text)

    docs = augment_docs([doc], augmenter=aug, nlp=nlp)
    assert next(docs).text != text


def test_create_random_casing_augmenter(nlp):
    text = "The augmented version of this should not be the same"

    aug = spacy.augmenters.get("char_replace_random.v1")(level=1)
    doc = nlp(text)

    docs = augment_docs([doc], augmenter=aug, nlp=nlp)
    assert next(docs).text != text


def test_create_char_replace_augmenter(nlp):
    aug = spacy.augmenters.get("char_replace.v1")(
        level=1, replace={"b": ["p"], "q": ["a", "b"]}
    )

    doc = nlp("The augmented version of this should not be the same")
    docs = augment_docs([doc], augmenter=aug, nlp=nlp)
    assert next(docs).text != "The augmented version of this should not pe the same"

    doc = nlp("q w")
    docs = augment_docs([doc], augmenter=aug, nlp=nlp)
    assert next(docs)[0].text in ["a", "b"]
    assert next(docs)[1].text == "w"


def test_create_keystroke_error_augmenter():
    text = "The augmented version of this should not be the same"
    aug_text = "The augmented version of this should not pe the same"

    nlp = Danish()
    aug = spacy.augmenters.get("keystroke_error.v1")(level=1, keyboard="da_qwerty.v1")
    doc = nlp(text)

    docs = augment_docs([doc], augmenter=aug, nlp=nlp)
    assert next(docs).text in "12wsa"


def test_create_char_swap_augmenter(nlp):
    aug = spacy.augmenters.get("char_swap.v1")(level=1)
    doc = nlp("qw")
    docs = augment_docs([doc], augmenter=aug, nlp=nlp)
    assert next(docs).text == "wq"


def test_create_spacing_augmenter(nlp):
    aug = spacy.augmenters.get("remove_spacing.v1")(level=1)
    doc = nlp("a sentence.")
    docs = augment_docs([doc], augmenter=aug, nlp=nlp)
    assert next(docs).text == "asentence."
