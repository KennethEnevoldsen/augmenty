import augmenty
import spacy
from spacy.language import Language
from spacy.tokens import Doc


def test_create_random_casing_augmenter(nlp_en: Language):
    text = (
        "some of the cases here should not be lowercased."
        + " there is naturally a chance that it might not end up that way,"
        + " but it should be very very very rare."
    )

    aug = spacy.registry.augmenters.get("random_casing_v1")(level=1)  # type: ignore
    doc = nlp_en(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_en)
    assert next(docs).text != text  # type: ignore


def test_create_char_replace_random_augmenter(nlp_en: Language):
    text = "The augmented version of this should not be the same"

    aug = spacy.registry.augmenters.get("char_replace_random_v1")(level=1)  # type: ignore
    doc = nlp_en(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_en)
    assert next(docs).text != text  # type: ignore


def test_create_char_replace_augmenter(nlp_en: Language):
    aug = spacy.registry.augmenters.get("char_replace_v1")(  # type: ignore
        level=1,
        replace={"b": ["p"], "q": ["a", "b"]},
    )

    doc = nlp_en("The augmented version of this should be the same")
    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_en)
    assert next(docs).text == "The augmented version of this should pe the same"  # type: ignore

    doc = nlp_en("q w")
    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_en)
    doc: Doc = next(docs)  # type: ignore
    assert doc[0].text in ["a", "b"]  # type: ignore
    assert doc[1].text == "w"  # type: ignore


def test_create_keystroke_error_augmenter(nlp_da: Language):
    text = "q"

    aug = spacy.registry.augmenters.get("keystroke_error_v1")(  # type: ignore
        level=1,
        keyboard="da_qwerty_v1",
    )
    doc = nlp_da(text)

    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_da)
    aug_doc: Doc = next(docs)  # type: ignore
    assert aug_doc.text in "12wsa"


def test_create_char_swap_augmenter(nlp_en: Language):
    aug = spacy.registry.augmenters.get("char_swap_v1")(level=1)  # type: ignore
    doc = nlp_en("qw")
    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_en)
    aug_doc: Doc = next(docs)  # type: ignore
    assert aug_doc.text == "wq"


def test_create_spacing_augmenter(nlp_en: Language):
    aug = spacy.registry.augmenters.get("remove_spacing_v1")(level=1)  # type: ignore
    doc = nlp_en("a sentence.")
    docs = augmenty.docs([doc], augmenter=aug, nlp=nlp_en)
    assert next(docs).text == "asentence."  # type: ignore
