FAQ
-------


How do I cite this work?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you use this library in your research, it would be much appreciated it if you would cite:

.. code-block::
   
   @software{enevoldsen_augmenty_2021,
      author = {Enevoldsen, Kenneth},
      doi = {10.5281/zenodo.6675315},
      title = {{Augmenty: The cherry on top of your NLP pipeline}},
      url = {https://github.com/KennethEnevoldsen/augmenty},
      version = {1.0.1}
   }

How do I test the code and run the test suite?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This package comes with an extensive test suite. In order to run the tests,
you'll usually want to clone the repository and build the package from the
source. This will also install the required development dependencies
and test utilities defined in the extras_require section of the :code:`pyproject.toml`.

.. code-block:: bash

   pip install -e ".[tests]"

   python -m pytest


which will run all the test in the `tests` folder.

Specific tests can be run using:

.. code-block:: bash

   python -m pytest tests/desired_test.py

If you want to check code coverage you can run the following:

.. code-block::

   python -m pytest --cov=.


Does this package run on X?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This package is intended to run on all major OS, this includes Windows (latest version), MacOS (latest) and the latest version of Linux (Ubuntu). 
Similarly it also tested on python 3.8, and 3.9.
Please note these are only the systems this package is being actively tested on, if you run on a similar system (e.g. an earlier version of Linux) this package
will likely run there as well, if not please create an issue.

How is the documentation generated?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Augmenty uses `sphinx <https://www.sphinx-doc.org/en/master/index.html>`__ to generate documentation. It uses the `Furo <https://github.com/pradyunsg/furo>`__ theme with custom styling.

To make the documentation you can run:

.. code-block::

  # install sphinx, themes and extensions
  pip install sphinx furo sphinx-copybutton sphinxext-opengraph

  # generate html from documentations

  make -C docs html


Many of these augmenters are completely useless for training?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

That is true, some of the augmenters are rarely something you would augment with during training. For instance, randomly adding or removing spacing.
However, augmentation can also be used to test whether a model is robust to certain variations.

Can I use augmenty without using spaCy?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Indeed augmenty contains convenience functions for applying augmentation directly to raw texts.
Check out the `getting started guide <https://kennethenevoldsen.github.io/augmenty/introduction.html>`__ to learn how.
However, augmenty still used spaCy in the background for this task.

How is the documentation generated?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

SpaCy-wrap uses `sphinx <https://www.sphinx-doc.org/en/master/index.html>`__ to generate
documentation. It uses the `Furo <https://github.com/pradyunsg/furo>`__ theme
with custom styling.

To make the documentation you can run:

.. code-block:: bash

   # install sphinx, themes and extensions
   pip install -e ".[docs]"

   # generate html from documentations

   make -C docs html

  


