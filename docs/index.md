# Augmenty

[![GitHub stars](https://img.shields.io/github/stars/kennethenevoldsen/augmenty.svg?style=social&label=Star&maxAge=2592000)](https://github.com/kennethenevoldsen/augmenty)

Augmenty is an augmentation library based on spaCy for augmenting texts. Augmenty differs from other augmentation libraries in that it corrects (as far as possible) the token,
sentence and document labels under the augmentation.

The documentation is organized into three parts:

- **Getting started** contains the installation instructions, guides, and tutorials on how to use augmenty.
- **Augmenters** contains the documentation for each augmenter implemented in augmenty.
- **API references** contains the documentation of each function and public class other than augmenters.

## Where to ask questions?

To report issues or request features, please use the
[GitHub Issue Tracker](https://github.com/KennethEnevoldsen/augmenty/issues).
Questions related to spaCy are kindly referred to the spaCy GitHub or forum. Otherwise,
please use the discussion forums.

| Type                         |                                                                                |
| ---------------------------- | ------------------------------------------------------------------------------ |
| **Bug Reports**              | [GitHub Issue Tracker](https://github.com/KennethEnevoldsen/augmenty/issues)   |
| **Feature Requests & Ideas** | [GitHub Issue Tracker](https://github.com/KennethEnevoldsen/augmenty/issues)   |
| **Usage Questions**          | [GitHub Discussions](https://github.com/KennethEnevoldsen/augmenty/discussions) |
| **General Discussion**       | [GitHub Discussions](https://github.com/KennethEnevoldsen/augmenty/discussions) |

```{toctree}
:maxdepth: 3
:caption: Getting started
:hidden:

installation
tutorials/introduction
tutorials/training_using_augmenty/training_using_augmenty
news
adding_an_augmenter
faq
```

```{toctree}
:maxdepth: 3
:caption: Augmenters
:hidden:

augmenters_overview
augmenty.character
augmenty.token
augmenty.span
augmenty.doc
augmenty.lang
augmenty.augment_utilities
```

```{toctree}
:maxdepth: 3
:caption: API references
:hidden:

augmenty.util
augmenty.keyboard
```

```{toctree}
:hidden:

GitHub Repository <https://github.com/kennethenevoldsen/augmenty>
```

## Indices and search

- {ref}`genindex`
- {ref}`search`
