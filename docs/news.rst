News and Changelog
==============================

To see the automatically created changelog see the `CHANGELOG.md <https://github.com/KennethEnevoldsen/augmenty/blob/main/CHANGELOG.md>`__ file.

* 1.1.0 (17/01/23):

  - Added support for SpaCy 3.4.0, this requires refactoring the names of all augmenters from ``{augmenter-name}.v1`` to `{augmenter-name}_v1`` as the ``.`` is no longer allowed in SpaCy component names.

* 1.0.4 (11/10/22):
   
  - Hungarian keyboard was added (by `qeterme <https://github.com/qeterme>`__)

* 1.0.0 (05/04/22)

  - Added new augmenters
  
    * paragraph subset augmenter
 
  - Renamed all augmenters to include versioning (e.g. v1) for their create functions.
  - restructured tests to be cleaner and notably run faster

* 0.0.1 (03/08/21)

  - First version of augmenty launches 🎉

    * with more than 15 highly customizable augmenters,
    * A high-quality code-base (coverage of 96% and a codefactor A),
    * and utilities for easy application of augmenters to strings and spaCy Docs.
    * Furthermore, it also includes a series of convenience functions for combining and moderating augmentations.
    
