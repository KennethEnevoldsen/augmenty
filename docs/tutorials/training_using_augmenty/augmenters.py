"""Definition of the augmenters used in the config.cfg file.

Can be run using spacy the following way:

    python -m spacy train config.cfg --code augmenters.p


Where config.cfg is the config file and augmenters.py is this file.


Within the config.cfg file, the augmenters are defined as follows:

    [corpora.train.augmenter]
    @augmenters = "my_augmenter"
"""

import spacy

import augmenty


@spacy.registry.augmenters("my_augmenter")  # type: ignore
def my_augmenters():
    # create the augmenters you wish to use
    # note that not all augmenters are compatible with all tasks (e.g. token deletion is not compatible with dependency parsing as e.g. the sentence
    # root token can be deleted)
    keystroke_augmenter = augmenty.load(
        "keystroke_error_v1",
        keyboard="en_qwerty_v1",
        level=0.03,
    )

    char_swap_augmenter = augmenty.load("char_swap_v1", level=0.03)

    # combine them into a single augmenter to be used for training
    return augmenty.combine([keystroke_augmenter, char_swap_augmenter])


if __name__ == "__main__":
    # run this file to test the augmenters
    nlp = spacy.blank("en")
    augmenter = my_augmenters()

    texts = ["This is a test sentence."]

    for i in range(10):
        augmented_texts = augmenty.texts(texts, augmenter, nlp=nlp)

        for text in augmented_texts:
            print(text)
