Creating and Contributing Augmenters
============================================

After using augmenty you might want to create and contribute an augmenter. Most augmenters can be created based on already existing augmenters. For instance, the augmenter :code:`per_replace.v1`, 
which replaces names in a text is a special case of the augmenter :code:`ents_replace.v1` with better handling of first and last names. 
If you want to create an augmenter from scratch following spaCy's guide on creating custom augmenters is a good start. You can always use augmenters from augmenty as inspiration as well. 
If you find yourself in trouble feel free to ask in the augmenty `forums <https://github.com/KennethEnevoldsen/augmenty/discussions>`__.

When you are satisfied with your augmenter feel free submit a `pull request <https://github.com/KennethEnevoldsen/augmenty/pulls>`__ to add the augmenter to augmenty.

When adding an new augmenter to Augmenty you should:

- Add the augmenter.
- Add a create function for the augmenter.

  * You should also add this to the spacy augmenters registry. You can do this easily using the decorator :code:`@spacy.registry.augmenters("name_of_your_augmenter_v1")`. This allows the function to be fetchable using :code:`augmenty.load`.
  * This is also the function that should contain the documentation. Which we recommend includes at least one example of usage.

- Add at least one test of the function.
- Add an entry to the file `meta.json <https://github.com/KennethEnevoldsen/augmenty/blob/main/augmenty/meta.json>`__. This entry is used for generating the augmenters overview and can contain:

  * "description": An optional short description, if there isn't any it is extracted from the function documentation.
  * "respects": What label the augmentation respects.
  * "references": An optional dictionary of references, where the key refers to the reference type. Typically these include, "Data" (a reference to any data used), "Package" (a reference to any additional packages used), "Usage" (the reference to articles or other work using the augmentation). Each of this should contain a dictionary (or a list of dictionaries in case of multiples), where each have a "name" (e.g. "Miller (1998)") and a "link". See examples of other augmenters in the meta.json.

