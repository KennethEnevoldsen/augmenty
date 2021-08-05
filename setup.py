import setuptools

with open("augmenty/about.py") as f:
    v = f.read()
    for l in v.split("\n"):
        if l.startswith("__version__"):
            __version__ = l.split('"')[-2]

with open("readme.md", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read()

setuptools.setup(
    name="augmenty",
    version=__version__,
    description="A augmentation library based on SpaCy for joint augmentation of text and labels.",
    license="Apache License 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kenneth C. Enevoldsen",
    author_email="kennethcenevoldsen@gmail.com",
    url="https://github.com/KennethEnevoldsen/augmenty",
    packages=setuptools.find_packages(),
    include_package_data=True,
    # external packages as dependencies
    install_requires=[
        "spacy>=3.0.0,<3.2.0"
        ],
    extras_require={
        'da' : ['dacy>=1.1.0'],
        'all' : ['nltk>=3.6.2,<3.7.0']
    },
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="NLP danish",
)
