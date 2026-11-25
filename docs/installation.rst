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

Language specific augmenters (e.g. the Danish ``da_æøå_replace_v1``) and keyboard layouts are included in the
base installation and do not require any additional dependencies.

Development Installation
^^^^^^^^^^^^^^^^^^^^^^^^^

To set up the development environment for this package, clone the repository and install the
package using the following commands:

.. code-block::

   git clone https://github.com/KennethEnevoldsen/augmenty
   cd augmenty
   make install  # uses uv to install the package and all development dependencies