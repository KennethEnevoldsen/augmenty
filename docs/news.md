# News and Changelog

For the full list of changes in each release see the [GitHub releases](https://github.com/KennethEnevoldsen/augmenty/releases).

- **2.0.0**
  - Dropped support for Python 3.8 and 3.9, and added support for Python 3.11 to 3.14.
  - The wordnet augmenters now require `nltk>=3.10`, which uses the Open Multilingual Wordnet 2.0.
  - Removed the `da` extra, which only installed DaCy. The Danish augmenters require no additional dependencies.
- **1.1.0** (17/01/23)
  - Added support for spaCy 3.4.0, this requires refactoring the names of all augmenters from `{augmenter-name}.v1` to `{augmenter-name}_v1` as the `.` is no longer allowed in spaCy component names.
- **1.0.4** (11/10/22)
  - Hungarian keyboard was added (by [qeterme](https://github.com/qeterme))
- **1.0.0** (05/04/22)
  - Added new augmenters
    - paragraph subset augmenter
  - Renamed all augmenters to include versioning (e.g. v1) for their create functions.
  - Restructured tests to be cleaner and notably run faster
- **0.0.1** (03/08/21)
  - First version of augmenty launches 🎉
    - with more than 15 highly customizable augmenters,
    - a high-quality code-base (coverage of 96% and a codefactor A),
    - and utilities for easy application of augmenters to strings and spaCy Docs.
    - Furthermore, it also includes a series of convenience functions for combining and moderating augmentations.
