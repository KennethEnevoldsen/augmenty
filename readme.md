
Work order:
- [x] create tests for package
- [x] create list all
- [ ] setup init and load for package
- [ ] test the thing!
- [ ] setup install for package
- [ ] Add/update/check documentations and at examples to augmenters
- [ ] create documentation
- [ ] set up GitHub
- [ ] publish

Todo:
- [ ] Add synonym list from DaCy
- [ ] Add readme with sources for each language
- [ ] Add entity, names ... (check NL augment)
  - [ ] https://github.com/GEM-benchmark/NL-Augmenter/tree/main/transformations/gender_culture_diverse_name_two_way
  - [ ] Usernames
- [ ] Create tests for all augmenters
- [ ] Function to create a list of all augmenters and examples (maybe with a given sentence)
- [ ] A list of what each function respect (i.e. does augmenter X respect POS-tags?) - maybe this can be done with catalogue?
- [ ] create yield both augmenter (yield both augmented and unaugmented example)
- [ ] normalize framing for create functions
- [ ] remove defaults from the augmenter and move them to the create func.
- [ ] Create a searchable table either using augmenters either using https://sphinxcontrib-needs.readthedocs.io/en/latest/directives/needtable.html or https://github.com/crate/sphinx_csv_filter
- [ ] Add to each augmenter whether it respects token classification, spans, dep,  
- [ ] Add data, package and paper of augmenters ref
- [ ] add ignore casing to token_replace


- [ ] Create a list of augmenters to add
  - [ ] Check NL augment
  - [ ] check nlpaug



Tutorials:
- Getting started with augmenters
  - Getting an overview of the augmenters
  - Inspecting the augmentation
- Training with spaCy and augmenty
  - Using an easy data augmentation
  - Selecting the right augmenters for you
  - Combining augmenters?
  - Find the right level with W&B sweep
- Estimate model robustness and biases with augmenty
- Adding new augmenters


Installation:
install augmenty
install augmenty[da]  # includes DaCy for synonym list and more
install augmenty[all] # includes NLTK 

FAQ:

- Many of these augmenters are completely useless for training?
That is true, many of these is rarely something you would train with. For instance randomly adding or removing spacing. However, augmentation can just as well be used to test whether a system is robust to certain variations.

- I wish to add an augmenter, how do I do it?
(link to auto PR)

- Does augmenty run on my OS?
(insert pytest)

- Can I use augmenty without using spacy?
(show utility function example)


## 🤔 FAQ


<details>
  <summary>How do I test the code and run the test suite?</summary>


DaCy comes with an extensive test suite. In order to run the tests, you'll usually want to clone the repository and build DaCy from the source. This will also install the required development dependencies and test utilities defined in the requirements.txt.


```
pip install -r requirements.txt
pip install pytest

python -m pytest
```

which will run all the test in the `dacy/tests` folder.

Specific tests can be run using:

```
python -m pytest dacy/tests/test_readability.py
```

**Code Coverage**
If you want to check code coverage you can run the following:
```
pip install pytest-cov

python -m pytest--cov=.
```


</details>

<br /> 

<details>
  <summary>Why is vaderSentiment_da.py being excluded in the coverage test?</summary>

  It is excluded as the functionality is intended to move to another repository called sentida2, which is currently under development.
  
</details>

<br /> 


<details>
  <summary>Does DaCy run on X?</summary>

  DaCy is intended to run on all major OS, this includes Windows (latest version), MacOS (Catalina) and the latest version of Linux (Ubuntu). Below you can see if DaCy passes its test suite for the system of interest. The first one indicated Linux. Please note these are only the systems DaCy is being actively tested on, if you run on a similar system (e.g. an earlier version of Linux) DaCy will likely run there as well.

| Operating System | Status                                                                                                                                                                                                                  |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ubuntu (Latest)  | [![github actions pytest ubuntu](https://github.com/centre-for-humanities-computing/DaCy/actions/workflows/pytest-cov-comment.yml/badge.svg)](https://github.com/centre-for-humanities-computing/DaCy/actions/workflows/pytest-cov-comment.yml)     |
| MacOS (Catalina) | [![github actions pytest catalina](https://github.com/centre-for-humanities-computing/DaCy/actions/workflows/pytest_mac_catalina.yml/badge.svg)](https://github.com/centre-for-humanities-computing/DaCy/actions/workflows/pytest_mac_catalina.yml) |
| Windows (Latest) | [![github actions pytest windows](https://github.com/centre-for-humanities-computing/DaCy/actions/workflows/pytest_windows.yml/badge.svg)](https://github.com/centre-for-humanities-computing/DaCy/actions/workflows/pytest_windows.yml)            |

  
</details>

<br /> 

<details>
  <summary>How is the documentation generated?</summary>

  DaCy uses [sphinx](https://www.sphinx-doc.org/en/master/index.html) to generate documentation. It uses the [Furo](https://github.com/pradyunsg/furo) theme with a custom styling.

  To make the documentation you can run:
  
  ```
  # install sphinx, themes and extensions
  pip install sphinx furo sphinx-copybutton sphinxext-opengraph

  # generate html from documentations

  make -C docs html
  ```
  
</details>

 <br /> 