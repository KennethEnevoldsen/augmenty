import subprocess
import sys

import augmenty


def test_augmenters():
    augmenters = augmenty.augmenters()

    assert isinstance(augmenters, dict)
    assert "upper_case_v1" in augmenters


def test_spacy_augmenters_available_without_pipeline():
    """spaCy >=3.8 only registers its own augmenters once the registry is
    populated, which normally happens when a pipeline is created. Run in a fresh
    interpreter as other tests will already have created pipelines.
    """
    code = (
        "import augmenty\n"
        "assert 'spacy.lower_case.v1' in augmenty.augmenters()\n"
        "augmenty.load('spacy.lower_case.v1', level=1)\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_keyboards():
    kb = augmenty.keyboards()

    assert isinstance(kb, list)
    assert "da_qwerty_v1" in kb


def test_meta():
    meta = augmenty.meta()

    assert isinstance(meta, dict)
    assert "upper_case_v1" in meta
