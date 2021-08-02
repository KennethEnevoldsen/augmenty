
from augmenty.utils import augment_docs
from utils import texts

import augmenty


def test_all_augmenter(nlp):
    for aug in augmenty.augmenters():
        for text in texts:
            doc = nlp(text)
            list(augment_docs([doc], aug, nlp))