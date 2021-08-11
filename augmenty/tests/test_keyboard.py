import augmenty
from augmenty.keyboard import Keyboard


def test_Keyboard():
    kb = Keyboard.from_registry("da_qwerty.v1")

    assert kb.coordinate("q") == (1, 0)
    assert kb.is_shifted("q") is False
    assert kb.euclidian_distance("q", "a") <= 1
    assert len(set(kb.all_keys())) > 28 * 2
    assert "w" in kb.get_neighbours("q")
    kb.create_distance_dict()

    for keyboard in augmenty.keyboards():
        kb = Keyboard.from_registry(keyboard)

