import random
from functools import partial
from typing import Iterator, Callable

import spacy
from spacy.language import Language
from spacy.training import Example

from ..augment_utilites import make_text_from_orth


@spacy.registry.augmenters("synonym_augmenter.v1")
def create_synonym_augmenter(
    level: float, 
    synonyms: dict, 
    getter: Callable = lambda token: token.pos_
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter swaps a token with its synonym based on a dictionary.

    Args:
        level (float): Probability to replace token given that it is in synonym dictionary.
        synonyms (dict): a dictionary of words and a list of their synonyms
            {"act": ["perform", "move", "action"], ...} or {"act": {"VERB": ["perform", "move"], "NOUN": ["action", "deed"]}}, ...}
            Union[Dict[str, Iterable], Dict[str, Dict[str, Iterable]]]

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.
    """
    return partial(synonym_augmenter, level=level, synonyms=synonyms, getter=getter)


def synonym_augmenter(
    nlp: Language,
    example: Example,
    level: float,
    synonyms: dict,
    getter: Callable,
) -> Iterator[Example]:
    def __replace(t):
        if t.text in synonyms and random.random() < level:
            if isinstance(synonyms[t.text], dict):
                pos = getter(t)
                if pos in synonyms[t.text]:
                    return random.sample(synonyms[t.text][pos], k=1)[0]
            else:
                return random.sample(synonyms[t.text], k=1)[0]
        return t

    example_dict = example.to_dict()
    example_dict["token_annotation"]["ORTH"] = [__replace(t) for t in example.reference]
    text = make_text_from_orth(example_dict)
    doc = nlp.make_doc(text)
    yield example.from_dict(doc, example_dict)

