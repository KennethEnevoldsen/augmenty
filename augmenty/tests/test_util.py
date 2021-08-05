import augmenty


def test_augmenters():
    augmenters = augmenty.augmenters()

    assert isinstance(augmenters, dict)
    assert "upper_case.v1" in augmenters


def test_keyboards():
    kb = augmenty.keyboards()

    assert isinstance(kb, list)
    assert "da_qwerty.v1" in kb
