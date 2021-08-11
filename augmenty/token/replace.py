import random
from functools import partial
from typing import Dict, Iterator, Callable, List, Optional, Union

import spacy
from spacy.language import Language
from spacy.training import Example
from spacy.tokens import Token

from ..augment_utilities import make_text_from_orth


@spacy.registry.augmenters("token_dict_replace.v1")
def create_token__dict_replace_augmenter(
    level: float,
    replace: Union[Dict[str, List[str]], Dict[str, Dict[str, List[str]]]],
    ignore_casing: bool = True,
    getter: Callable[[Token], str] = lambda token: token.pos_,
    keep_titlecase: bool = True,
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
        >>> create_token_dict_replace_augmenter(replace=replace, level=.10)
        >>> # or
        >>> replace = {"act": {"VERB": ["perform", "move"], "NOUN": ["action", "deed"]}}
        >>> create_token_dict_replace_augmenter(replace=replace, level=.10)
    """
    if ignore_casing is True:
        for k in replace:
            replace[k.lower()] = replace[k]

    return partial(
        token_dict_replace_augmenter,
        level=level,
        replace=replace,
        getter=getter,
        ignore_casing=ignore_casing,
        keep_titlecase=keep_titlecase,
    )


def token_dict_replace_augmenter(
    nlp: Language,
    example: Example,
    level: float,
    replace: Union[Dict[str, List[str]], Dict[str, Dict[str, List[str]]]],
    ignore_casing: bool,
    getter: Callable[[Token], str],
    keep_titlecase: bool,
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
    level: float,
    lang: Optional[str] = None,
    respect_pos: bool = True,
    getter: Callable = lambda token: token.pos_,
    keep_titlecase: bool = True,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter swaps a token with its synonym based on a dictionary.

    Args:
        lang (Optional[str], optional): Language supplied a ISO 639-1 language code. Defaults to None,
            in which case the lang is based on the language of the spacy nlp pipeline used.
            Possible language codes include:
            "da", "ca", "en", "eu", "fa", "fi", "fr", "gl", "he", "id", "it", "ja", "nn", "no", "pl", "pt", "es", "th".
        level (float): Probability to replace token given that it is in synonym dictionary.
        respect_pos (bool, optional): Should POS-tag be respected? Defaults to True.
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
        respect_pos: bool,
        keep_titlecase: bool,
    ) -> Iterator[Example]:
        if lang is None:
            lang = nlp.lang
            lang = lang_dict[lang]

        def __replace(t):
            word = t.text.lower()
            if random.random() < level and (respect_pos is False or getter(t) in upos_wn_dict):
                if respect_pos is True:
                    syns = wordnet.synsets(word, pos=upos_wn_dict[getter(t)], lang=lang)
                else:
                    syns = wordnet.synsets(word, lang=lang)
                if syns:
                    rep = {l for syn in syns for l in syn.lemma_names(lang=lang)}
                    if word in rep:
                        rep.remove(word)
                    if rep:
                        text = random.sample(rep, k=1)[0]
                        if keep_titlecase is True and t.is_title is True:
                            text = text.capitalize()
                        return text
            return t.text

        example_dict = example.to_dict()
        example_dict["token_annotation"]["ORTH"] = [
            __replace(t) for t in example.reference
        ]
        text = make_text_from_orth(example_dict)
        doc = nlp.make_doc(text)
        yield example.from_dict(doc, example_dict)

    if lang:
        lang = lang_dict[lang]
    return partial(
        wordnet_synonym_augmenter,
        level=level,
        lang=lang,
        getter=getter,
        keep_titlecase=keep_titlecase,
        respect_pos=respect_pos,
    )


def token_replace_augmenter(
    nlp: Language,
    example: Example,
    level: float,
    replace: Callable[[Token], str],
    keep_titlecase: bool,
) -> Iterator[Example]:
    if keep_titlecase is True:
        def __replace(t) -> str:
            text = replace(t)
            if t.is_title is True:
                text = text.capitalize()
            return text
    else:
        __replace = replace

    example_dict = example.to_dict()
    example_dict["token_annotation"]["ORTH"] = [__replace(t) if random.random() < level else t.text for t in example.reference]
    text = make_text_from_orth(example_dict)
    doc = nlp.make_doc(text)
    yield example.from_dict(doc, example_dict)

@spacy.registry.augmenters("token_replace.v1")
def create_token_replace_augmenter(
    replace: Callable[[Token], str],
    keep_titlecase: bool=True,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter which replaces a token based on a replace function.

    Args:
        level (float): Probability to replace token given that it is in synonym dictionary.
        replace (Callable[[Token], str): A callable which takes a spaCy Token as input and returns the replaces word as a string.
        keep_titlecase (bool, optional): If original text was uppercased cased should replaces text also be? Defaults to True.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.

    Examples:
        >>> def remove_vowels(token):
            vowels = ['a','e','i','o','u', 'y']
            non_vowels = [c for c in token.text if c.lower() not in vowels]
            return ''.join(non_vowels)
        >>> remove_vowel_augmenter = create_token_replace_augmenter(replace=remove_vowels, level=.10)
    """
    return partial(token_replace_augmenter, replace=replace, keep_titlecase=keep_titlecase)

@spacy.registry.augmenters("word_embedding.v1")
def create_word_embedding_augmenter(
    level=float,
    n: int=10,
    nlp: Optional[Language]=None,
    keep_titlecase: bool=True, 
    ignore_casing: bool=True,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter which replaces a token based on a replace function.

    Args:
        level (float): Probability to replace token given that it is in synonym dictionary.
        n (int, optional): Number of most similar word vectors to sample from 
        nlp (Optional[Language], optional): A spaCy text-processing pipeline used for supplying the word vectors if the nlp model supplies doesn't contain word vectors.
        keep_titlecase (bool, optional): If original text was uppercased cased should replaces text also be? Defaults to True.
        ignore_case (bool, optional): The word embedding augmenter does not replace a word with the same word. Should this operation ignore casing? Default to True.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.

    Examples:
        >>> nlp = spacy.load('en_core_web_lg')
    """
    import numpy as np

    def replace(t: Token, n: int, ignore_casing: bool, nlp: Language) -> str:
        if nlp is None:
            vocab = t.doc.vocab
        else:
            vocab = nlp.vocab
        if vocab.vectors.shape == (0, 0):
            raise ValueError("Vectors are empty. Typically this is due to using a transformer-based or small spaCy model. Specify nlp for the create_word_embedding_augmenter to a spaCy pipeline with static word embedding to avoid this issue.")
        if t.text in vocab:
            v = vocab.get_vector(t.text)
            v = np.reshape(v, (1,-1))
            ms = vocab.vectors.most_similar(v, n=n)
            rep = [vocab.strings[w] for w in ms[0][0]]
            if ignore_casing is True:
                rep = [w for w in rep if w.lower() != t.text.lower()]
            else:
                rep = [w for w in rep if w != t.text]
            if rep:
                return random.choice(rep)
        return t.text

    __replace = partial(replace, n=n, ignore_casing=ignore_casing, nlp=nlp)
    return partial(token_replace_augmenter, replace=__replace, keep_titlecase=keep_titlecase, level=level)