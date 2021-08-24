def init_wordnet():
    try:
        from nltk import download

        download("wordnet", quiet=True, raise_on_error=True)
        download("omw", quiet=True, raise_on_error=True)
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

lang_wn_dict = {
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