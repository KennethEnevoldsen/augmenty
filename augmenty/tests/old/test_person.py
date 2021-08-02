

from spacy.lang.da import Danish
from spacy.training import Example

import dacy
from dacy.augmenters import create_pers_augmenter

def test_create_pers_augmenter():
    nlp = dacy.load("da_dacy_medium_tft-0.0.0")
    aug = create_pers_augmenter(ent_dict={"first_name": ["Lasse"]}, patterns=["fn"], force_pattern_size=True, keep_name=False)
    
    doc = nlp("Mit navn er Kenneth Enevoldsen")
    example = Example(doc, doc)
    examples = aug(nlp, example)
    example_aug = next(examples)
    assert example_aug.x.text == "Mit navn er Lasse"

    aug = create_pers_augmenter(ent_dict={"first_name": ["Lasse"], "last_name": ["Hansen"]}, patterns=["fn,ln"], force_pattern_size=True,  keep_name=False)
    
    doc = nlp("Mit navn er Kenneth")
    example = Example(doc, doc)
    examples = aug(nlp, example)
    example_aug = next(examples)
    assert example_aug.x.text == "Mit navn er Lasse Hansen"

    aug = create_pers_augmenter(ent_dict=None, patterns=["abbpunct,abb"], force_pattern_size=True, keep_name=True)
    
    doc = nlp("Mit navn er Kenneth Enevoldsen")
    example = Example(doc, doc)
    examples = aug(nlp, example)
    example_aug = next(examples)
    assert example_aug.x.text == "Mit navn er K. E"