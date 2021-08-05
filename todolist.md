Work order:

- [x] create documentation
  - [x] check that documentation completes
  - [x] Write introduction/tutorials
  - [ ] Set the view to view in github instead of on the website
- [ ] PR to spacy w. augmenters
- [x] publish
  - [ ] create issue DaCy to use augmenty and textdescriptives
    - [ ] Add synonym list from DaCy
  - [ ] add to spacy-universe
  - [ ] Create an overview of augmenters and augmentation utilies
- [ ] More robust tests
  - [x] Add test for entities which include a parsed example
  - [ ] Fix token swap for HEAD
  - [ ] Apply all augs with a range of inputs to 3 longer texts in Danish and English
- [ ] Design considerations
  - [ ] Make wordnet use lang of pipeline of no lang is given
- [ ] Add description of what is needed to add submit a new augmenter
  - [ ] A create function for the augmenter
    - [ ] which has the documentation, including at least one example
  - [ ] Adding it to spacy's registry using the registry decorator
  - [ ] Added a short description of it to the overview page
  - [ ] Adding at least one test of the function


Todo:
- [ ] Function to create a list of all augmenters and examples (maybe with a given sentence)
- [ ] A list of what each function respect (i.e. does augmenter X respect POS-tags?) - maybe this can be done with catalogue?
- [ ] remove defaults from the augmenter and move them to the create func.
- [ ] Create a searchable table either using augmenters either using https://sphinxcontrib-needs.readthedocs.io/en/latest/directives/needtable.html or https://github.com/crate/sphinx_csv_filter
- [ ] Add to each augmenter whether it respects token classification, spans, dep,  
- [ ] Add data, package and paper of augmenters ref
- [ ] add ignore casing to token_replace


- [ ] Create a list of augmenters to add
  - [ ] Check NL augment
  - [ ] check nlpaug


FAQ:

- Many of these augmenters are completely useless for training?
That is true, many of these is rarely something you would train with. For instance randomly adding or removing spacing. However, augmentation can just as well be used to test whether a system is robust to certain variations.

- I wish to add an augmenter, how do I do it?
(link to auto PR)

- Can I use augmenty without using spacy?
(show utility function example)