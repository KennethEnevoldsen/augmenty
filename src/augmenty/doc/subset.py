import random
from functools import partial
from typing import Iterator, Union

import numpy as np
import spacy
from spacy.language import Language
from spacy.training import Example

from augmenty.augment_utilities import make_text_from_orth
from augmenty.util import Augmenter


def paragraph_subset_augmenter_v1(
    nlp: Language,
    example: Example,
    *,
    min_paragraph: Union[float, int],
    max_paragraph: Union[float, int],
    respect_sentences: bool,
) -> Iterator[Example]:
    example_dict = example.to_dict()
    token_anno = example_dict["token_annotation"]
    doc_anno = example_dict["doc_annotation"]

    doc_len = len(example.y)
    if respect_sentences:
        sents = list(example.y.sents)
        n = len(sents)
    else:
        n = doc_len

    min_n = (
        int(min_paragraph * n) if isinstance(min_paragraph, float) else min_paragraph  # type: ignore
    )
    max_n = (
        int(max_paragraph * n) if isinstance(max_paragraph, float) else max_paragraph  # type: ignore
    )
    n_to_keep = random.randint(min_n, max_n)
    start_n = random.randint(0, n - n_to_keep)
    end_n = start_n + n_to_keep

    if respect_sentences:
        sents = sents[start_n:end_n]  # type: ignore
        if sents:
            start, end = sents[0].start, sents[-1].end  # type: ignore
        else:
            start, end = 0, 0
    else:
        start, end = start_n, end_n

    # Respect entity spans
    start_is_in_entity = start != 0 and example.y[start].ent_iob_ not in {"O", "B", ""}
    end_is_in_entity = end < doc_len - 1 and example.y[end].ent_iob_ not in {
        "O",
        "B",
        "",
    }
    while start_is_in_entity:
        start -= 1
        start_is_in_entity = start != 0 and example.y[start].ent_iob_ not in {
            "O",
            "B",
            "",
        }
    while end_is_in_entity:
        end += 1
        end_is_in_entity = end < doc_len - 1 and example.y[end].ent_iob_ not in {
            "O",
            "B",
            "",
        }

    for k in token_anno:
        token_anno[k] = token_anno[k][start:end]
    doc_anno["entities"] = doc_anno["entities"][start:end]
    if example.y.has_annotation("HEAD"):
        token_anno["HEAD"] = (np.array(token_anno["HEAD"]) - start).tolist()  # type: ignore
    else:
        token_anno["HEAD"] = list(range(len(token_anno["HEAD"])))  # type: ignore

    text = make_text_from_orth(example_dict)
    doc = nlp.make_doc(text)
    yield Example.from_dict(doc, example_dict)


@spacy.registry.augmenters("paragraph_subset_augmenter_v1")  # type: ignore
def create_paragraph_subset_augmenter_v1(
    min_paragraph: Union[float, int] = 1,
    max_paragraph: Union[float, int] = 1.00,
    respect_sentences: bool = True,
) -> Augmenter:
    """Create an augmenter that extracts a subset of a document.

    Args:
        min_paragraph: An float indicating the min percentage of the
            document to include or a float indicating the minimum number of paragraps
            to include (tokens in respect sentences is False). E.g. 1, indicates at least one sentence.
        max_paragraph: An float indicating the max percentage of the
            document to include or a float indicating the maximum number of paragraps
            to include (tokens in respect sentences is False). E.g. 1.00 indicates 100%.
        respect_sentences: should the augmenter respect sentence bounderies?

    Returns:
        The augmenter.

    Example:
        >>> import augmenty
        >>> import spacy
        >>> nlp = spacy.blank("en")
        >>> nlp.add_pipe("sentencizer")
        >>> augmenter = augmenty.load("sent_subset_v1", level=0.7)
        >>> text = "Augmenty is a wonderful tool for augmentation. " +
        >>>   "It have tons of different augmenters. " +
        >>>   " Augmenty is developed using spaCy."
        >>> list(augmenty.texts([text], augmenter, nlp))
        ["Augmenty is a wonderful tool for augmentation. Augmenty is developed using
        spaCy."]
    """
    return partial(
        paragraph_subset_augmenter_v1,
        respect_sentences=respect_sentences,
        min_paragraph=min_paragraph,
        max_paragraph=max_paragraph,
    )
