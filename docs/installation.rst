Installation
==================
To get started using augmenty simply install it using pip by running the following line in your terminal:

.. code-block::

   pip install augmenty


augmenty relies on additional packages for some augmentations. For instance, the wordnet augmenter relies on the NLTK package.
You can install these additional dependencies by running the following command:

.. code-block::

   pip install augmenty[all]


Language specific augmentations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

augmenty supports language specific augmentations, which are not installed by default. To install these augmentations, run the following command:

.. code-block::

   pip install augmenty[{lang}]


Where valid values for {lang} are:

- ``da``: Danish

Development Installation
^^^^^^^^^^^^^^^^^^^^^^^^^

To set up the development environment for this package, clone the repository and install the
package using the following commands:

.. code-block::

   git clone https://github.com/KennethEnevoldsen/augmenty

   pip install -e ".[style,tests,docs]"