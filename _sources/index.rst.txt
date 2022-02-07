Augmenty
================================

.. image:: https://img.shields.io/github/stars/kennethenevoldsen/augmenty.svg?style=social&label=Star&maxAge=2592000
   :target: https://github.com/kennethenevoldsen/augmenty

Augmenty is an augmentation library based on spaCy for augmenting texts. Augmenty differs from other augmentation libraries in that it corrects (as far as possible) the token, 
sentence and document labels under the augmentation.


Contents
---------------------------------
  
The documentation is organized into three parts:

- **Getting started** contains the installation instructions, guides, and tutorials on how to use augmenty.
- **Augmenters** contains the documentation for each augmenter implemented in augmenty.
- **API references** contains the documentation of each function and public class other than augmenters.

.. toctree::
   :maxdepth: 3
   :caption: Getting started

   installation
   tutorials/introduction
   news
   adding_an_augmenter
   faq
   
.. toctree::
   :maxdepth: 3
   :caption: Augmenters

   augmenters_overview
   augmenty.character
   augmenty.token
   augmenty.span
   augmenty.doc
   augmenty.lang
   augmenty.augment_utilities


.. toctree::
   :maxdepth: 3
   :caption: API references

   augmenty.util
   augmenty.keyboard


.. toctree::
  GitHub Repository <https://github.com/kennethenevoldsen/augmenty>


Indices and search
==================

* :ref:`genindex`
* :ref:`search`
