import random
from functools import partial
from typing import Dict, Iterator, Callable, List, Optional, Union

import spacy
from spacy.language import Language
from spacy.training import Example
from spacy.tokens import Token

from ..augment_utilities import make_text_from_orth


@spacy.registry.augmenters("token_replace.v1")
def create_token_replace_augmenter(
    level: float,
    replace: Union[Dict[str, List[str]], Dict[str, Dict[str, List[str]]]],
    ignore_casing: bool = True,
    getter: Callable[[Token], str] = lambda token: token.pos_,
    keep_titlecase: bool=True, 
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter swaps a token with its synonym based on a dictionary.

    Args:
        level (float): Probability to replace token given that it is in synonym dictionary.
        replace (Union[Dict[str, List[str]], Dict[str, Dict[str, List[str]]]]): A dictionary of
            words and a list of their replacement (e.g. synonyms) or a dictionary denoting
            replacement based on pos tag.
        ignore_casing: When doing the lookup should the model ignore casing? Defaults to True.
        getter (Callable[[Token], str], optional): A getter function to extract the POS-tag.
        keep_titlecase (bool): Should the model keep the titlecase of the replaced word. Defaults to True.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.

    Examples:
        >>> replace = {"act": ["perform", "move", "action"], }
        >>> create_token_replace_augmenter(replace=replace, level=.10)
        >>> # or
        >>> replace = {"act": {"VERB": ["perform", "move"], "NOUN": ["action", "deed"]}}
        >>> create_token_replace_augmenter(replace=replace, level=.10)
    """
    if ignore_casing is True:
        for k in replace:
            replace[k.lower()] = replace[k]
            
    return partial(token_replace_augmenter, level=level, replace=replace, getter=getter, ignore_casing=ignore_casing, keep_titlecase=keep_titlecase)


def token_replace_augmenter(
    nlp: Language,
    example: Example,
    level: float,
    replace: Union[Dict[str, List[str]], Dict[str, Dict[str, List[str]]]],
    ignore_casing: bool,
    getter: Callable[[Token], str],
    keep_titlecase: bool
) -> Iterator[Example]:
    def __replace(t):
        text = t.text
        if ignore_casing is True:
            text = text.lower()
        if text in replace and random.random() < level:
            if isinstance(replace[t.text], dict):
                pos = getter(t)
                if pos in replace[t.text]:
                    text = random.sample(replace[t.text][pos], k=1)[0]
            else:
                text = random.sample(replace[t.text], k=1)[0]
            if keep_titlecase is True and t.is_title is True:
                text = text.capitalize()
            return text
        return t.text

    example_dict = example.to_dict()
    example_dict["token_annotation"]["ORTH"] = [__replace(t) for t in example.reference]
    text = make_text_from_orth(example_dict)
    doc = nlp.make_doc(text)
    yield example.from_dict(doc, example_dict)


@spacy.registry.augmenters("wordnet_synonym.v1")
def create_wordnet_synonym_augmenter(
    level: float, lang: Optional[str] = None, getter: Callable = lambda token: token.pos_, keep_titlecase: bool=True,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter swaps a token with its synonym based on a dictionary.

    Args:
        lang (Optional[str], optional): Language supplied a ISO 639-1 language code. Defaults to None, 
            in which case the lang is based on the language of the spacy nlp pipeline used.
            Possible language codes include:
            "da", "ca", "en", "eu", "fa", "fi", "fr", "gl", "he", "id", "it", "ja", "nn", "no", "pl", "pt", "es", "th".
        level (float): Probability to replace token given that it is in synonym dictionary.
        getter (Callable[[Token], str], optional): A getter function to extract the POS-tag.
        keep_titlecase (bool): Should the model keep the titlecase of the replaced word. Defaults to True.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.

    Example:
        >>> english_synonym_augmenter = create_wordnet_synonym_augmenter(level=0.1, lang="en")
    """
    try:
        from nltk import download
        download("wordnet", quiet=True, raise_on_error=True)
        download("omw", quiet=True, raise_on_error=True)
        from nltk.corpus import wordnet
    except ModuleNotFoundError as e:
        print(e)
        raise ModuleNotFoundError(
            "This augmenter requires NLTK. Use `pip install nltk` or `pip install augmenty[all]`"
        )

    upos_wn_dict = {
        "VERB": "v",
        "NOUN": "n",
        "ADV": "r",
        "ADJ": "s",
    }

    lang_dict = {
        "da": "dan",
        "ca": "cat",
        "en": "eng",
        "eu": "eus",
        "fa": "fas",
        "fi": "fin",
        "fr": "fre",
        "gl": "glg",
        "he": "heb",
        "id": "ind",
        "it": "ita",
        "ja": "jpn",
        "nn": "nno",
        "no": "nob",
        "pl": "pol",
        "pt": "por",
        "es": "spa",
        "th": "tha",
    }

    def wordnet_synonym_augmenter(
        nlp: Language,
        example: Example,
        level: float,
        lang: Optional[str],
        getter: Callable,
        keep_titlecase: bool
    ) -> Iterator[Example]:
        if lang is None:
            lang = nlp.lang

        def __replace(t):
            word = t.text
            if random.random() < level and getter(t) in upos_wn_dict:
                syns = wordnet.synsets(word, pos=upos_wn_dict[getter(t)], lang=lang)
                if syns:
                    syn = random.sample(syns, k=1)[0]
                    text = random.sample(syn.lemma_names(lang=lang), k=1)[0]
                    if keep_titlecase is True and t.is_title is True:
                        return text.capitalize()
            return t.text

        example_dict = example.to_dict()
        example_dict["token_annotation"]["ORTH"] = [
            __replace(t) for t in example.reference
        ]
        text = make_text_from_orth(example_dict)
        doc = nlp.make_doc(text)
        yield example.from_dict(doc, example_dict)

    return partial(
        wordnet_synonym_augmenter, level=level, lang=lang_dict[lang], getter=getter, keep_titlecase=keep_titlecase,
    )
