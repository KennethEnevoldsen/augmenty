import random
from functools import partial
from typing import Callable, Dict, Iterator, List, Optional, Union

import spacy
from spacy.language import Language
from spacy.tokens import Token
from spacy.training import Example

from ..augment_utilities import make_text_from_orth
from .static_embedding_util import static_embedding
from .wordnet_util import init_wordnet


def token_dict_replace_augmenter_v1(
    nlp: Language,
    example: Example,
    level: float,
    replace: Union[Dict[str, List[str]], Dict[str, Dict[str, List[str]]]],  # type: ignore
    ignore_casing: bool,
    getter: Callable[[Token], str],  # type: ignore
    keep_titlecase: bool,
) -> Iterator[Example]:  # type: ignore
    def __replace(t):
        text = t.text
        if ignore_casing is True:
            text = text.lower()
        if text in replace and random.random() < level:
            if isinstance(replace[t.text], dict):
                pos = getter(t)
                if pos in replace[t.text]:
                    text = random.sample(replace[t.text][pos], k=1)[0]  # type: ignore
            else:
                text = random.sample(replace[t.text], k=1)[0]  # type: ignore
            if keep_titlecase is True and t.is_title is True:
                text = text.capitalize()
            return text
        return t.text

    example_dict = example.to_dict()
    example_dict["token_annotation"]["ORTH"] = [__replace(t) for t in example.reference]
    text = make_text_from_orth(example_dict)
    doc = nlp.make_doc(text)
    yield example.from_dict(doc, example_dict)


@spacy.registry.augmenters("token_dict_replace_v1")  # type: ignore
def create_token__dict_replace_augmenter_v1(
    level: float,
    replace: Union[Dict[str, List[str]], Dict[str, Dict[str, List[str]]]],  # type: ignore
    ignore_casing: bool = True,
    getter: Callable[[Token], str] = lambda token: token.pos_,  # type: ignore
    keep_titlecase: bool = True,
) -> Callable[[Language, Example], Iterator[Example]]:  # type: ignore
    """Creates an augmenter swaps a token with its synonym based on a
    dictionary.

    Args:
        level: Probability to replace token given that it is in synonym dictionary.
        replace: A dictionary of words and a list of their replacement (e.g. synonyms) or a dictionary denoting replacement based on pos tag.
        ignore_casing: When doing the lookup should the model ignore casing?
        getter: A getter function to extract the POS-tag.
        keep_titlecase: Should the model keep the titlecase of the replaced word.

    Returns:
        The augmenter.

    Examples:
        >>> replace = {"act": ["perform", "move", "action"], }
        >>> create_token_dict_replace_augmenter(replace=replace, level=.10)
        >>> # or
        >>> replace = {"act": {"VERB": ["perform", "move"], "NOUN": ["action", "deed"]}}
        >>> create_token_dict_replace_augmenter(replace=replace, level=.10)
    """
    if ignore_casing is True:
        for k in replace:
            replace[k.lower()] = replace[k]  # type: ignore

    return partial(
        token_dict_replace_augmenter_v1,
        level=level,
        replace=replace,
        getter=getter,
        ignore_casing=ignore_casing,
        keep_titlecase=keep_titlecase,
    )


@spacy.registry.augmenters("wordnet_synonym_v1")  # type: ignore
def create_wordnet_synonym_augmenter_v1(
    level: float,
    lang: Optional[str] = None,  # type: ignore
    respect_pos: bool = True,
    getter: Callable = lambda token: token.pos_,  # type: ignore
    keep_titlecase: bool = True,
) -> Callable[[Language, Example], Iterator[Example]]:  # type: ignore
    """Creates an augmenter swaps a token with its synonym based on a
    dictionary.

    Args:
        lang: Language supplied a ISO 639-1 language code. If None, the lang is based on the language of the
            spacy nlp pipeline used. Possible language codes include:
            "da", "ca", "en", "eu", "fa", "fi", "fr", "gl", "he", "id", "it", "ja",
            "nn", "no", "pl", "pt", "es", "th".
        level: Probability to replace token given that it is in synonym dictionary.
        respect_pos: Should POS-tag be respected?
        getter: A getter function to extract the POS-tag.
        keep_titlecase: Should the model keep the titlecase of the replaced word.

    Returns:
        The augmenter.

    Example:
        >>> english_synonym_augmenter = create_wordnet_synonym_augmenter(level=0.1,
        >>>                                                              lang="en")
    """
    init_wordnet()
    from nltk.corpus import wordnet  # type: ignore

    from .wordnet_util import lang_wn_dict, upos_wn_dict

    def wordnet_synonym_augmenter_v1(
        nlp: Language,
        example: Example,
        level: float,
        lang: Optional[str],  # type: ignore
        getter: Callable,  # type: ignore
        respect_pos: bool,
        keep_titlecase: bool,
    ) -> Iterator[Example]:  # type: ignore
        if lang is None:
            lang = nlp.lang
            lang = lang_wn_dict[lang]  # type: ignore

        def __replace(t):
            word = t.text.lower()
            if random.random() < level and (
                respect_pos is False or getter(t) in upos_wn_dict
            ):
                if respect_pos is True:
                    syns = wordnet.synsets(word, pos=upos_wn_dict[getter(t)], lang=lang)
                else:
                    syns = wordnet.synsets(word, lang=lang)
                if syns:
                    rep = {
                        l
                        for syn in syns
                        for l in syn.lemma_names(lang=lang)  # noqa E741 # type: ignore
                    }
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
        lang = lang_wn_dict[lang]
    return partial(
        wordnet_synonym_augmenter_v1,
        level=level,
        lang=lang,
        getter=getter,
        keep_titlecase=keep_titlecase,
        respect_pos=respect_pos,
    )


def token_replace_augmenter_v1(
    nlp: Language,
    example: Example,
    level: float,
    replace: Callable[[Token], str],  # type: ignore
    keep_titlecase: bool,
) -> Iterator[Example]:  # type: ignore
    if keep_titlecase is True:

        def __replace(t) -> str:
            text = replace(t)
            if t.is_title is True:
                text = text.capitalize()
            return text

    else:
        __replace = replace  # type: ignore

    example_dict = example.to_dict()
    example_dict["token_annotation"]["ORTH"] = [
        __replace(t) if random.random() < level else t.text for t in example.reference
    ]
    text = make_text_from_orth(example_dict)
    doc = nlp.make_doc(text)
    yield example.from_dict(doc, example_dict)


@spacy.registry.augmenters("token_replace_v1")  # type: ignore
def create_token_replace_augmenter_v1(
    replace: Callable[[Token], str],  # type: ignore
    keep_titlecase: bool = True,
) -> Callable[[Language, Example], Iterator[Example]]:  # type: ignore
    """Creates an augmenter which replaces a token based on a replace function.

    Args:
        level: Probability to replace token given that it is in synonym dictionary.
        replace: A callable which takes a spaCy Token as input and returns the replaces word as a string.
        keep_titlecase: If original text was uppercased cased should replaces text also be?

    Returns:
        The augmenter.

    Examples:
        >>> def remove_vowels(token):
        ...    vowels = ['a','e','i','o','u', 'y']
        ...    non_vowels = [c for c in token.text if c.lower() not in vowels]
        ...    return ''.join(non_vowels)
        >>> aug = create_token_replace_augmenter(replace=remove_vowels, level=.10)
    """
    return partial(  # type: ignore
        token_replace_augmenter_v1,
        replace=replace,
        keep_titlecase=keep_titlecase,
    )


@spacy.registry.augmenters("word_embedding_v1")  # type: ignore
def create_word_embedding_augmenter_v1(
    level=float,
    n: int = 10,
    nlp: Optional[Language] = None,  # type: ignore
    keep_titlecase: bool = True,
    ignore_casing: bool = True,
) -> Callable[[Language, Example], Iterator[Example]]:  # type: ignore
    """Creates an augmenter which replaces a token based on a replace function.

    Args:
        level: Probability to replace token given that it is in synonym dictionary.
        n: Number of most similar word vectors to sample from nlp
        nlp: A spaCy text-processing pipeline used for supplying the word vectors if the nlp model supplies doesn't contain word vectors.
        keep_titlecase: If original text was uppercased cased should replaces text also be?
        ignore_case: The word embedding augmenter does not replace a word with the same word. Should this operation ignore casing?

    Returns:
        The augmenter.

    Examples:
        >>> nlp = spacy.load('en_core_web_lg')
        >>> aug = create_word_embedding_augmenter(nlp=nlp, level=.10)
    """

    def replace(
        t: Token,
        n: int,
        ignore_casing: bool,
        embedding: static_embedding,
    ) -> str:
        if embedding.vocab is None:
            embedding.update_from_vocab(t.doc.vocab)
        if embedding.vocab.vectors.shape == (0, 0):  # type: ignore
            raise ValueError(
                "Vectors are empty. Typically this is due to using a transformer-based "
                + "or small spaCy model. Specify nlp for the "
                + "create_word_embedding_augmenter to a spaCy pipeline with static word"
                + " embedding to avoid this issue.",
            )
        if t.text in embedding:
            rep = embedding.most_similar(t.text, n=n + 2)
            if ignore_casing is True:
                rep = [w for w in rep if w.lower() != t.text.lower()][:n]
            else:
                rep = [w for w in rep if w != t.text][:n]
            if rep:
                return random.choice(rep)
        return t.text

    embedding = static_embedding.from_vocab(nlp.vocab) if nlp else static_embedding()

    __replace = partial(replace, n=n, ignore_casing=ignore_casing, embedding=embedding)
    return partial(
        token_replace_augmenter_v1,
        replace=__replace,
        keep_titlecase=keep_titlecase,
        level=level,  # type: ignore
    )
