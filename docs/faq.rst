FAQ
-------


How do I test the code and run the test suite?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Augmenty comes with an extensive test suite. To run the tests, you should clone the repository, then build augmenty from the source. 
This will also install the required development dependencies and test utilities defined in the requirements.txt.


.. code-block::
   
   pip install -r requirements.txt
   pip install pytest

   python -m pytest


which will run all the test in the :code:`augmenty/tests` folder.

Specific tests can be run using:

.. code-block::

   python -m pytest augmenty/tests/desired_test.py


If you want to check code coverage you can run the following:

.. code-block::

   pip install pytest-cov

   python -m pytest --cov=.


Does augmenty run on X?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Augmenty is intended to run on all major OS, this includes Windows (latest version), MacOS (Catalina) and the latest version of Linux (Ubuntu). 
Similarly it also tested on python 3.7, 3.8, and 3.9.
Please note these are only the systems augmenty is being actively tested on, if you run on a similar system (e.g. an earlier version of Linux) augmenty
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
  

How do I cite this work?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you use this library in your research, it would be much appreciated it if you would cite:

.. code-block::
   
   @inproceedings{augmenty2021,
      title={Augmenty, the cherry on top of your NLP pipeline},
      author={Enevoldsen, Kenneth and Hansen, Lasse},
      year={2021}
   }
