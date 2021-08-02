import augmenty


def test_augmenters():
    augmenters = augmenty.augmenters()

    assert isinstance(augmenters, dict)
    assert "upper_case.v1" in augmenters
