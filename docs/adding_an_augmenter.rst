Creating and Contributing Augmenters
============================================

After using augmenty you might want to create and contribute an augmenter. Most augmenters can be created based on already existing augmenters. For instance, the augmenter :code:`per_replace.v1`, 
which replaces names in a text is a special case of the augmenter :code:`ents_replace.v1` with better handling of first and last names. 
If you want to create an augmenter from scratch following spaCy's guide on creating custom augmenters is a good start. You can always use augmenters from augmenty as inspiration as well. 
If you find yourself in trouble feel free to ask in the augmenty `forums <https://github.com/KennethEnevoldsen/augmenty/discussions>`__.

When you are satisfied with your augmenter feel free submit a `pull request <https://github.com/KennethEnevoldsen/augmenty/pulls>`__ to add the augmenter to augmenty.

An augmenter in Augmenty should include:
- Documentation including an example
- Adding it spacy augmenters registry. You can do this easily using the decorator :code:`@spacy.registry.augmenters("name_of_your_augmenter.v1")`

Additionally, you might want to add known references using the augmenter to the `reference.json <https://github.com/KennethEnevoldsen/augmenty/blob/master/augmenty/references.json>`__.