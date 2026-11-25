# FAQ

## How do I cite this work?

If you use this library in your research, it would be much appreciated if you would cite the package. For the most up to date citation see
"Cite this repository" on the [GitHub page](https://github.com/KennethEnevoldsen/augmenty).

## Does this package run on X?

This package is intended to run on all major operating systems, this includes Windows (latest version), macOS (latest) and the latest version of Linux (Ubuntu).
It is tested on Python 3.10, 3.12 and 3.14.
Please note these are only the systems this package is being actively tested on, if you run on a similar system (e.g. an earlier version of Linux) this package
will likely run there as well, if not please create an issue.

## How is the documentation generated?

Augmenty uses [Sphinx](https://www.sphinx-doc.org/en/master/index.html) to generate documentation. It uses the [Furo](https://github.com/pradyunsg/furo) theme with custom styling.

To build the documentation you can run:

```bash
make build-docs  # build the documentation using uv
make view-docs   # open it in your browser
```

## Many of these augmenters are completely useless for training?

That is true, some of the augmenters are rarely something you would augment with during training. For instance, randomly adding or removing spacing.
However, augmentation can also be used to test whether a model is robust to certain variations.

## Can I use augmenty without using spaCy?

Indeed augmenty contains convenience functions for applying augmentation directly to raw texts.
Check out the [getting started guide](tutorials/introduction.ipynb) to learn how.
However, augmenty still uses spaCy in the background for this task.
