import spacy
import augmenty
import pytest


@pytest.fixture()
def nlp():
    nlp = spacy.load("en_core_web_sm")
    return nlp


def test_combine(nlp):
    texts = ["Augmenty is a wonderful tool for augmentation."]

    ent_augmenter = augmenty.load(
        "ents_replace.v1",
        level=1.00,
        ent_dict={"ORG": [["spaCy"]]},
    )
    synonym_augmenter = augmenty.load("wordnet_synonym.v1", level=1, lang="en")

    combined_aug = augmenty.combine([ent_augmenter, synonym_augmenter])

    docs = nlp.pipe(texts)
    augmented_docs = list(augmenty.docs(docs, augmenter=combined_aug, nlp=nlp))

    assert augmented_docs[0][0].text == "spaCy"




def test_yield_original(nlp):
    texts = ["Augmenty is a wonderful tool for augmentation."]

    aug = augmenty.load("upper_case.v1", level=1)

    aug = augmenty.yield_original(aug)

    augmented_docs = list(augmenty.texts(texts, augmenter=aug, nlp=nlp))

    assert len(augmented_docs) == 2



def test_set_doc_level(nlp):
    texts = ["Augmenty is a wonderful tool for augmentation."]

    aug = augmenty.load("upper_case.v1", level=1)

    aug = augmenty.set_doc_level(aug, level = 0.5)

    # simply testing it it runs
    augmented_docs = list(augmenty.texts(texts, augmenter=aug, nlp=nlp))
