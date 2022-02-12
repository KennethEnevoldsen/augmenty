import random
from functools import partial
from typing import Iterator, Callable

import spacy
from spacy.language import Language
from spacy.training import Example
from augmenty.augment_utilities import make_text_from_orth


@spacy.registry.augmenters("sent_subset.v1")
def create_sent_subset_augmenter_v1(
    level: float, respect_sentences: bool = True
) -> Callable[[Language, Example], Iterator[Example]]:
    """Create an augmenter that converts documents to uppercase.

    Args:
        level (float): The percentage of the document to include.
        respect_sentences (bool): should the augmenter respect sentence bounderies? Defaults to True.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.

    Example:
        >>> import augmenty
        >>> import spacy
        >>> nlp = spacy.blank("en")
        >>> upper_case_augmenter = augmenty.load("sent_subset.v1", level=0.7)
        >>> texts = ["Augmenty is a wonderful tool for augmentation. It have tons of different augmenters. Augmenty is developed using spaCy."]
        >>> list(augmenty.texts(texts, upper_case_augmenter, nlp))
        ["Augmenty is a wonderful tool for augmentation. Augmenty is developed using spaCy."]
    """
    return partial(
        sent_subset_augmenter_v1, level=level, respect_sentences=respect_sentences
    )


def sent_subset_augmenter_v1(
    nlp: Language, example: Example, *, level: float, respect_sentences: bool
) -> Iterator[Example]:
    example_dict = example.to_dict()
    token_anno = example_dict["token_annotation"]
    doc_anno = example_dict["doc_annotation"]

    ents = {ent.start: list(range(ent.start, ent.end)) for ent in example.y.ents}

    popped = 0
    drop = False
    sent_start = token_anno["SENT_START"].copy()

    for i, s_start in enumerate(sent_start):
        # only check the first token in entity (treat entity as one word)
        ent_iob = example.y[i].ent_iob_
        if ent_iob not in {"O", "B", ""}:
            continue
        if respect_sentences:
            if s_start:
                drop = True if random.random() > level else False
        else:
            drop = True if random.random() > level else False

        if drop:  # drop (entire) entity or token
            to_drop = ents.get(i, [i])
            for t in to_drop:
                for k in token_anno:
                    token_anno[k].pop(t - popped)
                doc_anno["entities"].pop(t - popped)
                popped += 1

    text = make_text_from_orth(example_dict)
    doc = nlp.make_doc(text)
    yield Example.from_dict(doc, example_dict)


# import augmenty
# import spacy
# from spacy.training import Example

# nlp = spacy.load("en_core_web_sm")
# text = "Augmenty is a wonderful tool for augmentation. It have tons of different augmenters. Augmenty is developed using spaCy."
# doc = nlp(text)
# example = Example(doc, doc)

# docs = list(
#     sent_subset_augmenter_v1(nlp, example=example, level=1, respect_sentences=True)
# )
# assert docs[0].text == text
# print("GOOD")
# docs = list(sent_subset_augmenter_v1(nlp, example, level=0.0, respect_sentences=True))
# assert docs[0].text == ""
# print("GOOD")
