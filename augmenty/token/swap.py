import random
from functools import partial
from typing import Iterator, Callable

import numpy as np

import spacy
from spacy.language import Language
from spacy.training import Example
from spacy.tokens import Token

from ..augment_utilities import make_text_from_orth


@spacy.registry.augmenters("token_swap.v1")
def create_token_swap_augmenter(
    level: float, respect_ents: bool = True, respect_eos: bool = True
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter that randomly swaps two neighbouring tokens.

    Args:
        level (float): The probability to swap two tokens.
        respect_ents (bool, optional): Should the pipeline respect entities? Defaults to True. In which
            case it will not swap a token inside an entity with a token outside the entity span, unless
            it is a one word span. If false it will disregard correcting the entity labels.
        respect_eos (bool, optional): Should it respect end of sentence bounderies? Default to True, indicating
            that it will not swap and end of sentence token. If False it will disregard correcting the sentence
            start as this becomes arbitrary.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.
    """
    return partial(
        token_swap_augmenter,
        level=level,
        respect_eos=respect_eos,
        respect_ents=respect_ents,
    )


def token_swap_augmenter(
    nlp: Language,
    example: Example,
    level: float,
    respect_ents: bool,
    respect_eos: bool,
) -> Iterator[Example]:

    example_dict = example.to_dict()

    n_tok = len(example.y)

    if respect_ents is True:
        swap_ents = False

    is_swapped = set()

    tok_anno = example_dict["token_annotation"]
    for i in range(n_tok):
        if i in is_swapped:
            continue
        if random.random() < level:
            # select which neighbour
            fb = random.choice([1, -1])

            min_i = i + fb if 0 < i + fb < n_tok else i - fb

            if min_i in is_swapped:
                continue

            if min_i > i:
                i, min_i = min_i, i  # make so that i is always the biggest
                is_swapped.add(i)

            if respect_eos is True and (
                example.y[i].is_sent_end is True or example.y[min_i].is_sent_end is True
            ):
                continue

            if respect_ents is True:
                # 0: not labelled
                # 2 not an ent
                # 3 start ent
                # 1 in ent
                if example.y[min_i].ent_iob in {0, 2} and example.y[i].ent_iob in {
                    0,
                    2,
                }:
                    # Neither is an entity
                    # swap and keep ent spans the same
                    pass
                elif (example.y[min_i].ent_iob == 3 and example.y[i].ent_iob == 1) or (
                    example.y[min_i].ent_iob == 1 and example.y[i].ent_iob == 1
                ):
                    # both part of the same entity
                    # swap and keep ent spans the same
                    pass
                elif (example.y[min_i].ent_iob == 3 and example.y[i].ent_type == 0) or (
                    example.y[i].ent_iob == 3
                    and i != n_tok
                    and example.y[i + 1].ent_iob in {0, 2}
                ):
                    # 1st or second token is a one word entity
                    # swap and swap ents
                    swap_ents = True
                else:
                    # don't swap
                    continue

            for k in tok_anno:
                if k in ["SENT_START", "SPACY"]:
                    continue
                if k == "HEAD":
                    if example.y.has_annotation("HEAD"):
                        head = np.array(tok_anno[k])
                        head[head == i], head[head == min_i] = min_i, i
                        tok_anno[k] = head
                    else:
                        continue
                tok_anno[k][i], tok_anno[k][min_i] = tok_anno[k][min_i], tok_anno[k][i]

            if respect_ents is True and swap_ents is True:
                ents = example_dict["doc_annotation"]["entities"]
                ents[i], ents[min_i] = ents[min_i], ents[i]

    text = make_text_from_orth(example_dict)
    doc = nlp.make_doc(text)
    yield example.from_dict(doc, example_dict)
