---
title: 'Augmenty: A Python Library for Structured Text Augmentation'
tags:
  - Python
  - natural language processing
  - spacy
  - augmentation
authors:
  - name: Kenneth Enevoldsen
    orcid: 0000-0001-8733-0966
    affiliation: "1"

affiliations:
 - name: Center for Humanities Computing, Aarhus University, Aarhus, Denmark
   index: 1
date: 7 December 2023
bibliography: paper.bib
---

# Summary
Text augmentation is a useful tool for training [@wei-zou-2019-eda] and evaluating [@ribeiro-etal-2020-beyond] natural language processing models and systems. Despite its utility, existing libraries are often limited in terms of functionality and flexibility. They are confined to basic tasks such as text-classification or by catering to specific downstream use-cases such as estimating robustness [@goel-etal-2021-robustness]. Recognizing these constraints, `Augmenty` is a tool for structured augmentation of text along with its annotations. `Augmenty` integrates seamlessly with the popular NLP library `spaCy`  [@honnibal_efficient_2020] and seeks to be compatible with all models and tasks supported by `spaCy`. Augmenty provides a wide range of augmenters which can be combined in a flexible manner to create complex augmentation pipelines. It also includes a set of primitives that can be used to create custom augmenters such as word replacement augmenters. This functionality allows for augmentations within a range of applications such as named entity recognition (NER), part-of-speech tagging, and dependency parsing.

# Statement of need
<!-- augmentation is useful -->
Augmentation has proven to be a powerful tool within disciplines such as computer vision [@wang2017effectiveness] and speech recognition [@Park2019SpecAugmentAS] where it is used for both training more robust models and for evaluating the ability of the models to handle pertubations. Within natural language processing (NLP) augmentation has seen some uses as a tool for generating additional training data [@wei-zou-2019-eda], but has shined as a tool for model evaluation, such as estimating robustness [@goel-etal-2021-robustness] and bias [@lassen-etal-2023-detecting], or for creating novel datasets [@nielsen-2023-scandeval]. 

Despite its utility, existing libraries for text augmentation often exhibit limitations in terms of functionality and flexibility. Commonly they only provide pure string augmentation which typically leads to the annotations becoming misaligned with the text. This has limited the use of augmentation to tasks such as text classification while neglecting structured prediction tasks such as named entity recognition (NER) or coreference resolution. This has limited the use of augmentation to a wide range of tasks both for training and evaluation.

<!-- limitation of existing methods -->
Existing tools such as `textgenie` [@pandya_hetpandyatextgenie_2023], and `textaugment` [@marivate2020improving] implements powerful techniques such as backtranslation and paraprashing, which are useful augmentations for text-classification tasks. However, these tools neglect a category of tasks which require that the annotations are aligned with the augmentation of the text. For instance even simple augmentations such as replacing the named entity "Jane Doe" with "John" will lead to a misalignment of the NER annotation, part-of-speech tags, etc., which if not properly handled will lead to a misinterpretation of the model performance or generation of incorrect training samples. 

`Augmenty` seeks to remedy this by providing a flexible and easy-to-use interface for structured text augmentation. `Augmenty` is built to integrate well with `spaCy` [@honnibal_efficient_2020] and seeks to be compatible with the broad set of tasks supported by `spaCy`. Augmenty provides augmenters which take a spaCy `Doc`-object (but works just as well with `string`-objects) and return a new `Doc`-object with the augmentations applied. This allows for augmentations of both the text and the annotations present in the `Doc`-object.

Other tools for data augmentation focus on specific downstream application such as `textattack` [@morris2020textattack] which is useful for adversarial attacks of classification systems or `robustnessgym` [@goel-etal-2021-robustness] which is useful for evaluating robustness of classification systems. `Augmenty` does not seek to replace any of these tools
but seeks to provide a general purpose tool for augmentation of both the text and its annotations. This allows for augmentations within a range of applications such as named entity recognition, part-of-speech tagging, and dependency parsing.

# Features & Functionality

`Augmenty` is a Python library that implements augmentations based on `spaCy`'s `Doc` object. `spaCy`'s `Doc` object is a container for a text and its annotations. This makes it easy to augment text and annotations simultaneously. The `Doc` object can easily be extended to include custom augmentation not available in `spaCy` by adding custom attributes to the `Doc` object. While `Augmenty` is built to augment `Doc`s the object is easily converted into strings, lists or other formats. The annotations within a `Doc` can be provided either by human annotations or using a trained model.

Augmenty implements a series of augmenters for token-, span- and sentence-level augmentation. These augmenters range from primitive augmentations such as word replacement to language specific augmenters such as keystroke error augmentations based on a French keyboard layout. Augmenty also integrates with other libraries such as `NLTK` [bird2009natural] to allow for augmentations based on WordNet [@miller-1994-wordnet] and allows for specification of static word vectors [pennington-etal-2014-glove] to allow for augmentations based on word similarity. Lastly, `augmenty` provides a set of utility functions for repeating augmentations, combining augmenters or adjust the percentage of documents that should be augmented. This allow for the flexible construction of augmentation pipelines specific to the task at hand.

# Example Use Cases

Augmenty has already seen used in a number of projects. The code base was initially developed for evaluating the robustness and bias of `DaCy` [@Enevoldsen_DaCy_A_Unified_2021], a state-of-the-art Danish NLP pipeline. It is also continually used to evaluate Danish NER systems for biases and robustness on the DaCy website.
Augmenty has also been used to detect intersectional biases [@lassen-etal-2023-detecting] and used within benchmarks of Danish language models [@sloth_dadebiasgenda-lens_2023].

Besides its existing use-cases `Augmenty` could for example also be used to a) upsample minority classes without duplicating samples, b) train less biased models by e.g. replacing names with names of minority groups c) train more robust models e.g. by augmenting with typos or d) generate pseudo historical data by augmenting with known spelling variations of words.


# Target Audience

The package is mainly targeted at NLP researchers and practitioners who wish to augment their data for training or evaluation. The package is also targeted at researchers who wish to evaluate their models with augmentations or want to generate new datasets.


# Acknowledgements
The authors thank the [contributors](https://github.com/KennethEnevoldsen/augmenty/graphs/contributors) of the package notably Lasse Hansen which provided meaningful feedback on the design of the package at early stages of development.