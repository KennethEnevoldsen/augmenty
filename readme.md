<a href="https://github.com/kennethenevoldsen/augmenty"><img src="img/icon.png" width="175" height="175" align="right" /></a>
# Augmenty: The cherry on top of your NLP pipeline

[![PyPI version](https://badge.fury.io/py/augmenty.svg)](https://pypi.org/project/augmenty/)
[![python version](https://img.shields.io/badge/Python-%3E=3.7-blue)](https://github.com/kennethenevoldsen/augmenty)
[![Code style: black](https://img.shields.io/badge/Code%20Style-Black-black)](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)
[![spacy](https://img.shields.io/badge/built%20with-spaCy-09a3d5.svg)](https://spacy.io)
[![github actions pytest](https://github.com/kennethenevoldsen/augmenty/actions/workflows/pytest-cov-comment.yml/badge.svg)](https://github.com/kennethenevoldsen/augmenty/actions)
[![github actions docs](https://github.com/kennethenevoldsen/augmenty/actions/workflows/documentation.yml/badge.svg)](https://kennethenevoldsen.github.io/augmenty/)
![github coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/KennethEnevoldsen/af8637d94475ea8bcb6b6a03c4fbcd3e/raw/badge-augmenty-pytest-coverage.json)
[![CodeFactor](https://www.codefactor.io/repository/github/kennethenevoldsen/augmenty/badge)](https://www.codefactor.io/repository/github/kennethenevoldsen/augmenty)
<!-- [![Demo](https://img.shields.io/badge/Try%20the-Demo-important)](https://huggingface.co/chcaa/da_augmenty_medium_trf?text=augmenty+er+en+pipeline+til+anvendelse+af+dansk+sprogteknologi+lavet+af+K.+Enevoldsen%2C+L.+Hansen+og+K.+Nielbo+fra+Center+for+Humanities+Computing.) -->


Augmenty is an augmentation library based on spaCy for augmenting texts. Augmenty differs from other augmentation libraries in that it corrects (as far as possible) the token, 
sentence and document labels under the augmentation.


## 📖 Documentation

| Documentation              |                                                                              |
| -------------------------- | ---------------------------------------------------------------------------- |
| 🔧 **[Installation]**      | Installation instructions                                                    |
| 📚 **[Usage Guides]**      | Guides and instruction on how to use augmenty and its features.              |
| 🍒 **[Augmenters]** | Contains a full list of current and planned augmenters in augmenty.         |
| 📰 **[News and changelog]** | New additions, changes and version history.                                 | 
| 🎛 **[API Reference]**      | The detailed reference for augmenty's API. Including function documentation |

<!-- | ⭐️ **[augmenty 101]**        | New to spaCy? Here's everything you need to know!              | -->

[Installation]: https://kennethenevoldsen.github.io/augmenty/
[usage guides]: https://kennethenevoldsen.github.io/augmenty/
[api reference]: https://kennethenevoldsen.github.io/augmenty/
[news]: https://kennethenevoldsen.github.io/augmenty/
[List of augmenters]: https://github.com/kennethenevoldsen/augmenty/augmenters.md

## 💬 Where to ask questions

| Type                            | Platforms                               |
| ------------------------------- | --------------------------------------- |
| 🚨 **Bug Reports**              | [GitHub Issue Tracker]                  |
| 🎁 **Feature Requests & Ideas** | [GitHub Issue Tracker]                  |
| 👩‍💻 **Usage Questions**          | [GitHub Discussions]                    |
| 🗯 **General Discussion**       | [GitHub Discussions]                    |

[github issue tracker]: https://github.com/kennethenevoldsen/augmenty/issues
[github discussions]: https://github.com/kennethenevoldsen/augmenty/discussions


# 🤔 FAQ


<details>
  <summary>How do I test the code and run the test suite?</summary>


augmenty comes with an extensive test suite. In order to run the tests, you'll usually want to clone the repository and build augmenty from the source. This will also install the required development dependencies and test utilities defined in the requirements.txt.


```
pip install -r requirements.txt
pip install pytest

python -m pytest
```

which will run all the test in the `augmenty/tests` folder.

Specific tests can be run using:

```
python -m pytest augmenty/tests/test_readability.py
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
  <summary>Does augmenty run on X?</summary>

  augmenty is intended to run on all major OS, this includes Windows (latest version), MacOS (Catalina) and the latest version of Linux (Ubuntu). Below you can see if augmenty passes its test suite for the system of interest. The first one indicated Linux. Please note these are only the systems augmenty is being actively tested on, if you run on a similar system (e.g. an earlier version of Linux) augmenty will likely run there as well.

| Operating System | Status                                                                                                                                                                                                                  |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ubuntu (Latest)  | [![github actions pytest ubuntu](https://github.com/kennethenevoldsen/augmenty/actions/workflows/pytest-cov-comment.yml/badge.svg)](https://github.com/kennethenevoldsen/augmenty/actions/workflows/pytest-cov-comment.yml)     |
| MacOS (Catalina) | [![github actions pytest catalina](https://github.com/kennethenevoldsen/augmenty/actions/workflows/pytest_mac_catalina.yml/badge.svg)](https://github.com/kennethenevoldsen/augmenty/actions/workflows/pytest_mac_catalina.yml) |
| Windows (Latest) | [![github actions pytest windows](https://github.com/kennethenevoldsen/augmenty/actions/workflows/pytest_windows.yml/badge.svg)](https://github.com/kennethenevoldsen/augmenty/actions/workflows/pytest_windows.yml)            |

  
</details>

<br /> 

<details>
  <summary>How is the documentation generated?</summary>

  augmenty uses [sphinx](https://www.sphinx-doc.org/en/master/index.html) to generate documentation. It uses the [Furo](https://github.com/pradyunsg/furo) theme with a custom styling.

  To make the documentation you can run:
  
  ```
  # install sphinx, themes and extensions
  pip install sphinx furo sphinx-copybutton sphinxext-opengraph

  # generate html from documentations

  make -C docs html
  ```
  
</details>

 <br /> 

# Citing this work

If you use this library in your research, please cite:

```bibtex
@inproceedings{augmenty2021,
    title={Augmenty, the cherry on top of your NLP pipeline},
    author={Enevoldsen, Kenneth and Hansen, Lasse},
    year={2021}
}
```
