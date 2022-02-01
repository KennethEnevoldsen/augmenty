"""

pip install streamlit
pip install st-annotated-text

streamlit run demo/streamlit.py
"""

import spacy
import json
import sys

sys.path.append(".")
sys.path.append("..")

import augmenty
import streamlit as st
from annotated_text import annotated_text

import random

random.seed(1)

st.title("Augmentation using 🍒 Augmenty")
st.markdown(
    "Not all augmenters are included as some require external sources. This demo uses the SpaCy model `en_core_web_md` for tagging and named entity recognition."
)

not_relevant = {
    "spacy.orth_variants.v1",
    "char_replace.v1",
    "conditional_token_casing.v1",
    "ents_format.v1",
    "token_replace.v1",
    "wordnet_synonym.v1",
}
augmenters = augmenty.augmenters()
augmenter_list = sorted([a for a in augmenters if a not in not_relevant])
nlp = spacy.load("en_core_web_md")

default = "Write the text you wish augmented here! it could for example include names such as Sara."
example = st.text_area("Example:", default)

st.markdown("## Choose your augmenter\n --------")

def_aug = "per_replace.v1"
for i, _ in enumerate(augmenter_list):
    if _ == def_aug:
        break
augmenter = st.selectbox("Augmenter", augmenter_list, index=i)
desc = augmenters[augmenter].__doc__.split("\n\n")[0]
st.markdown(f"## Description: \n{desc}")

level = st.slider("level", min_value=0.0, max_value=1.0, step=0.01, value=1.0)


if augmenter == "per_replace.v1":
    json_ = st.text_input(
        "replace dict:",
        '{"firstname": ["Charles", "Jens"], "lastname": ["Kirkegaard", "Andersen"]}',
    )
    st.markdown(
        'Sampling names using `pattern=[["firstname"], ["firstname", "lastname"], ["firstname", "lastname", "lastname"]].`'
    )
    names = json.loads(json_)
    aug = augmenty.load(
        augmenter,
        names=names,
        level=level,
        patterns=[
            ["firstname"],
            ["firstname", "lastname"],
            ["firstname", "lastname", "lastname"],
        ],
    )
elif augmenter == "ents_replace.v1":
    json_ = st.text_input(
        "replace dict:",
        '{"ORG": [["Google"], ["Apple"]], "PERSON": [["Kenneth"], ["Lasse", "Hansen"]]}',
    )
    ent_dict = json.loads(json_)
    aug = augmenty.load(augmenter, ent_dict=ent_dict, level=level)
else:
    aug = augmenty.load(augmenter, level=level)

st.markdown("## Augmented text")
highlight = st.checkbox("Highlight changes", value=True)


def is_diff(token, aug_token):
    if token.text != aug_token.text and highlight:
        return (aug_token.text, "", "#fd7c6e")
    return aug_token.text + aug_token.whitespace_


def augment(example):
    doc = nlp(example)
    return [(doc, aug_doc) for aug_doc in augmenty.docs([doc], augmenter=aug, nlp=nlp)]


for doc, aug_doc in augment(example):
    aug_text = [is_diff(t, a_t) for t, a_t in zip(doc, aug_doc)]
    annotated_text(*aug_text)

st.markdown(f"\n -------- \n Using augmenter: {augmenter}.")
