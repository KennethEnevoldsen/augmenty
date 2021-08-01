from dacy.augmenters.keyboard import Keyboard, qwerty_da_array
from dacy.augmenters import create_keyboard_augmenter

from spacy.lang.da import Danish
from spacy.training import Example

def test_Keyboard():
    kb = Keyboard(keyboard_array = qwerty_da_array)

    assert kb.coordinate("q") == (1, 0)
    assert kb.is_shifted("q") is False
    assert kb.euclidian_distance("q", "a") <= 1
    assert len(set(kb.all_keys())) > 28*2
    assert "w" in kb.get_neighboors("q")
    kb.create_distance_dict()

def test_make_keyboard_augmenter():
    aug = create_keyboard_augmenter(doc_level=1, char_level=1, keyboard="QWERTY_DA")

    nlp = Danish()
    doc = nlp("q")
    example = Example(doc, doc)
    examples = aug(nlp, example)
    example_aug = next(examples)
    assert example_aug.x.text in "12wsa"