import random
from functools import partial
from typing import Dict, Iterator, Callable, List, Optional, Union

import spacy
from spacy.language import Language
from spacy.training import Example
from spacy.tokens import Token

from wasabi import msg


from ..augment_utilities import make_text_from_orth
from .wordnet_util import init_wordnet


@spacy.registry.augmenters("token_insert.v1")
def create_token_insert_augmenter(
    level: float,
    insert: Callable[[Token], Dict[str, str]],
    respect_ents: bool = True,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter that randomly inserts a token generated based on a insert function.

    Args:
        level (float): The probability to insert a token.
        insert (Callable[[Token], Dict[str, str]]): An insert function. The function takes in a spacy Token and return a
            dictionary representing the new token to replace. The dictionary can contain the keys: "ORTH", "SPACY" (defaults to "True"),
            "entities" (default to "O"), "POS" (defaults to "X"), "TAG" (defaults to "X"), "MORPH" (defaults to "X"), "LEMMA" (defaults to the ORTH token).
            You can also specify "HEAD" and "DEP" if they are not specified they will get removed. If the function returns no word is inserted.
        respect_ents (bool, optional): Should the augmentation respect entities? Defaults to True. In which
            case it will not insert a token inside an entity.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.

    Example:
        >>> import random
        >>> insert_fun = lambda t: random.choice([{"ORTH": "words"}, {"ORTH": "to"}, {"ORTH": "insert"}])
        >>> aug = augmenty.load("token_insert.v1", level=0.2, insert=insert_fun)
        >>> list(augmenty.texts(["This is a cat"], aug))
        ["This insert is a cat"]
    """
    return partial(
        token_insert_augmenter, level=level, respect_ents=respect_ents, insert=insert
    )


def token_insert_augmenter(
    nlp: Language,
    example: Example,
    level: float,
    respect_ents: bool,
    insert: Callable[[Token], Dict[str, str]],
) -> Iterator[Example]:
    doc = example.y

    example_dict = example.to_dict()
    ents = example_dict["doc_annotation"]["entities"]
    tok_anno = example_dict["token_annotation"]

    n = 0
    for i, t in enumerate(doc):
        if random.random() < level:
            if (
                respect_ents
                and t.ent_type
                and (i + 1 == len(doc) or doc[i + 1].ent_iob == "I")
            ):
                continue

            insert_ = insert(t)
            if insert_ is None:
                continue
            tok_anno["ORTH"].insert(i + n, insert_["ORTH"])
            tok_anno["POS"].insert(i + n, insert_.get("POS", "X"))
            tok_anno["TAG"].insert(i + n, insert_.get("TAG", "X"))
            tok_anno["LEMMA"].insert(i + n, insert_.get("LEMMA", insert_["ORTH"]))
            tok_anno["MORPH"].insert(i + n, insert_.get("MORPH", ""))
            tok_anno["SPACY"].insert(i + n, insert_.get("SPACY", True))
            ents.insert(i + n, insert_.get("entities", "O"))

            # seems unlikely that "HEAD" and "DEP" will ever get inserted meaningfully
            if (doc.has_annotation("HEAD") and "HEAD" in insert_) and (
                doc.has_annotation("DEP") and "DEP" in insert_
            ):
                tok_anno["HEAD"].insert(i + n, insert_["HEAD"])
                tok_anno["DEP"].insert(i + n, insert_["DEP"])
            else:
                if "HEAD" in tok_anno:
                    tok_anno.pop("HEAD")
                if "DEP" in tok_anno:
                    tok_anno.pop("DEP")

            sent_start, tok_anno["SENT_START"][i + n] = tok_anno["SENT_START"][i + n], 0
            tok_anno["SENT_START"].insert(i + n, sent_start)

            n += 1

    text = make_text_from_orth(example_dict)
    doc = nlp.make_doc(text)
    yield example.from_dict(doc, example_dict)


@spacy.registry.augmenters("token_insert_random.v1")
def create_token_insert_random_augmenter(
    level: float,
    insert: Optional[List[Union[str, Dict[str, str]]]] = None,
    respect_ents: bool = True,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter that randomly swaps two neighbouring tokens.

    Args:
        level (float): The probability to insert a token.
        insert (List[Union[str, Dict[str, str]]], optional): A list of string or a list of dictionaries representing a token. If None
        it will sample from the vocabulary of the nlp pipeline.
        respect_ents (bool, optional): Should the augmentation respect entities? Defaults to True. In which
            case it will not insert a token inside an entity.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.

    Example:
        >>> import augmenty
        >>> from spacy.lang.en import English
        >>> nlp = English()
        >>> augmenter = create_token_insert_random_augmenter(level = 0.30, insert = ["words", "to", "insert"])
        >>> texts = ["one two three"]
        >>> list(augmenty.texts(texts, augmenter, nlp))
        ["one words two three"]
        >>> # You even to very detailed token replace:
        >>> create_token_insert_random_augmenter(level = 0.5, insert = [{"ORTH": "replacements", "LEMMA": "replacement", "POS": "NOUN", "TAG": "NOUN", "entities": "O", "MORPH": "Number=Plur"}])
    """

    d = {"insert": insert}

    def __insert(t: Token, d: dict) -> dict:
        if d["insert"] is None:
            d["insert"] = list(t.doc.vocab.strings)
        t = random.choice(d["insert"])
        if isinstance(t, dict):
            return t
        return {"ORTH": t}

    __insert = partial(__insert, d=d)
    return partial(
        token_insert_augmenter, level=level, respect_ents=respect_ents, insert=__insert
    )


@spacy.registry.augmenters("duplicate_token.v1")
def create_duplicate_token_augmenter(
    level: float,
    respect_ents: bool = True,
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter that randomly duplicate a token token.

    Args:
        level (float): The probability to dublicate a token.
        respect_ents (bool, optional): Should the augmentation respect entities? Defaults to True. In which
            case it will not insert a token inside an entity.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.

    Example:
        >>> import augmenty
        >>> from spacy.lang.en import English
        >>> nlp = English()
        >>> aug = create_duplicate_token_augmenter(level = 1)
        >>> texts = ["one two three"]
        >>> list(augmenty.texts(texts, augmenter, nlp))
        ["one one two two three three"]
    """
    def __insert(t: Token, respect_ents=respect_ents) -> dict:
        insert_token = {
            "ORTH": t.text,
            "LEMMA": t.lemma_,
            "POS": t.pos_,
            "TAG": t.tag_,
            "MORPH": t.morph,
        }
        if t.doc.has_annotation("ENT_TYPE") and respect_ents is False:
            insert_token["entities"] = t.ent_iob_ + t.ent_type_
        return insert_token


    return partial(
        token_insert_augmenter, level=level, respect_ents=respect_ents, insert=__insert
    )


@spacy.registry.augmenters("random_synonym_insertion.v1")
def create_random_synonym_insertion_augmenter(
    level: float,
    respect_pos: bool = True,
    respect_ents: bool = True,
    pos_getter=lambda token: token.pos_,
    lang: Optional[str] = None,
    context_window: Optional[int] = None, 
    verbose: bool = True
) -> Callable[[Language, Example], Iterator[Example]]:
    """Creates an augmenter that randomly inserts a synonym or from the tokens context.
    The synonyms are based on wordnet.

    Args:
        level (float): The probability to dublicate a token.
        respect_ents (bool, optional): Should the augmentation respect entities? Defaults to True. In which
            case it will not insert a token inside an entity.
        respect_pos (bool, optional): Should POS-tag of the synonyms be respected? Defaults to True.
        pos_getter (Callable[[Token], str], optional): A getter function to extract the POS-tag.
        lang (Optional[str], optional): Language supplied a ISO 639-1 language code. Defaults to None,
            in which case the lang is based on the language of the spacy nlp pipeline used.
            Possible language codes include:
            "da", "ca", "en", "eu", "fa", "fi", "fr", "gl", "he", "id", "it", "ja", "nn", "no", "pl", "pt", "es", "th".
        context_window (Optional[int], optional): Sets window in which synonyms can be generated from. If None the context
        is set to the sentence.
        verbose (bool, optional): Toggle the verbosity of the function. Default to True.

    Returns:
        Callable[[Language, Example], Iterator[Example]]: The augmenter.

    Example:
        >>> import augmenty
        >>> from spacy.lang.en import English
        >>> nlp = English()
        >>> aug = create_random_synonym_insertion_augmenter(level = 0.1)
        >>> texts = ["I saw a cat"]
        >>> list(augmenty.texts(texts, augmenter, nlp))
        ["I kitten saw a cat"]
    """
    init_wordnet()
    from nltk.corpus import wordnet
    from .wordnet_util import upos_wn_dict
    from .wordnet_util import lang_wn_dict

    def __insert(t: Token, lang: str, respect_pos: bool, verbose: bool) -> dict:
        doc = t.doc
        if respect_pos is True and doc.has_annotation("POS") is False:
            if verbose:
                msg.warn("respect_pos is True, but the doc is not annotated for part of speech. Setting respect_pos to False.")
            respect_pos = False

        if lang is None:
            lang = doc.lang_
            lang = lang_wn_dict[lang]

        rep = set()
        if context_window:
            span = doc[max(0, t.i-context_window): min(len(doc), t.i+context_window)]
        elif doc.has_annotation("SENT_START"):
            span = t.sent
        else:
            raise ValueError("context_window is None, but the document is not sentence segmented. Either use a nlp which include a sentencizer component or specify a context_window") 
        for t in span:
            word = t.lower_
            if respect_pos is True:
                pos = pos_getter(t)
                if pos in upos_wn_dict:
                    syns = wordnet.synsets(word, pos=upos_wn_dict[pos], lang=lang)
                    rep = rep.union(
                        {(l, pos) for syn in syns for l in syn.lemma_names(lang=lang)}
                    )
            else:
                syns = wordnet.synsets(word, lang=lang)
                rep = rep.union({l for syn in syns for l in syn.lemma_names(lang=lang)})

        if rep:
            text = random.sample(rep, k=1)[0]
            if isinstance(text, tuple):
                return {
                    "ORTH": text[0],
                    "POS": t.pos_,
                    "TAG": t.tag_,
                }
            return {
                "ORTH": text,
            }
        return None

    insert = partial(__insert, lang=lang, respect_pos=respect_pos, verbose=verbose)
    return partial(
        token_insert_augmenter, level=level, respect_ents=respect_ents, insert=insert
    )
