Augmenty
================================

.. image:: https://img.shields.io/github/stars/kennethenevoldsen/augmenty.svg?style=social&label=Star&maxAge=2592000
   :target: https://github.com/kennethenevoldsen/augmenty

Augmenty is an augmentation library based on spaCy for augmenting texts. Augmenty differs from other augmentation libraries in that it corrects (as far as possible) the token, 
sentence and document labels under the augmentation.

The documentation is organized into three parts:

- **Getting started** contains the installation instructions, guides, and tutorials on how to use augmenty.
- **Augmenters** contains the documentation for each augmenter implemented in augmenty.
- **API references** contains the documentation of each function and public class other than augmenters.


Where to ask questions?
^^^^^^^^^^^^^^^^^^^^^^^^

To ask report issues or request features, please use the
`GitHub Issue Tracker <https://github.com/kennethenevoldsen/augmenty/issues>`__.
Questions related to SpaCy are kindly referred to the SpaCy GitHub or forum. Otherwise,
please use the discussion Forums.

+------------------------------+-------------------------+
| Type                         |                         |
+------------------------------+-------------------------+
| **Bug Reports**              | `GitHub Issue Tracker`_ |
+------------------------------+-------------------------+
| **Feature Requests & Ideas** | `GitHub Issue Tracker`_ |
+------------------------------+-------------------------+
| **Usage Questions**          | `GitHub Discussions`_   |
+------------------------------+-------------------------+
| **General Discussion**       | `GitHub Discussions`_   |
+------------------------------+-------------------------+

.. _GitHub Issue Tracker: https://github.com/KennethEnevoldsen/augmenty/issues
.. _GitHub Discussions: https://github.com/KennethEnevoldsen/augmenty/discussions
  

.. toctree::
   :maxdepth: 3
   :caption: Getting started
   :hidden:

   installation
   tutorials/introduction
   news
   adding_an_augmenter
   faq
   
.. toctree::
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


.. toctree::
   :maxdepth: 3
   :caption: API references
   :hidden:

   augmenty.util
   augmenty.keyboard


.. toctree::
   :hidden:
   
   GitHub Repository <https://github.com/kennethenevoldsen/augmenty>


Indices and search
==================

* :ref:`genindex`
* :ref:`search`
