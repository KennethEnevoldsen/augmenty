Work order:

- [x] create documentation
  - [x] check that documentation completes
  - [ ] Write introduction/tutorials
  - [ ] Set the view to view in github instead of on the website
- [ ] create logo
- [ ] PR to spacy w. augmenters
- [ ] set up GitHub w. secrets
  - [ ] fix main -> master
- [ ] publish
  - [ ] create issue DaCy to use augmenty and textdescriptives
    - [ ] Add synonym list from DaCy
  - [ ] add to spacy-universe
  - [ ] Create an overview of augmenters and augmentation utilies


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