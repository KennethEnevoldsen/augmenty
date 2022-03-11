import spacy
import augmenty


from .fixtures import nlp_en, nlp_da


def test_create_random_casing_augmenter(nlp_en):
    text = (
        "some of the cases here should not be lowercased."
        + " there is naturally a chance that it might not end up that way,"
        + " but it should be very very very rare."
    )

    aug = spacy.registry.augmenters.get("random_casing.v1")(level=1)
    doc = nlp_en(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_en)
    assert next(docs).text != text


def test_create_char_replace_random_augmenter(nlp_en):
    text = "The augmented version of this should not be the same"

    aug = spacy.registry.augmenters.get("char_replace_random.v1")(level=1)
    doc = nlp_en(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_en)
    assert next(docs).text != text


def test_create_char_replace_augmenter(nlp_en):
    aug = spacy.registry.augmenters.get("char_replace.v1")(
        level=1, replace={"b": ["p"], "q": ["a", "b"]}
    )

    doc = nlp_en("The augmented version of this should be the same")
    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_en)
    assert next(docs).text == "The augmented version of this should pe the same"

    doc = nlp_en("q w")
    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_en)
    doc = next(docs)
    assert doc[0].text in ["a", "b"]
    assert doc[1].text == "w"


def test_create_keystroke_error_augmenter(nlp_da):
    text = "q"

    aug = spacy.registry.augmenters.get("keystroke_error.v1")(
        level=1, keyboard="da_qwerty.v1"
    )
    doc = nlp_da(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_da)
    assert next(docs).text in "12wsa"


def test_create_char_swap_augmenter(nlp_en):
    aug = spacy.registry.augmenters.get("char_swap.v1")(level=1)
    doc = nlp_en("qw")
    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_en)
    assert next(docs).text == "wq"


def test_create_spacing_augmenter(nlp_en):
    aug = spacy.registry.augmenters.get("remove_spacing.v1")(level=1)
    doc = nlp_en("a sentence.")
    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_en)
    assert next(docs).text == "asentence."
