Work order:
- [x] create tests for package
- [x] create list all
- [x] setup init and load for package
- [x] test the thing!
- [x] setup install for package
- [x] Add/update/check documentations and at examples to augmenters
- [x] create readme
- [ ] create documentation
- [ ] set up GitHub w. secrets
- [ ] publish
- [ ] create issue DaCy to use augmenty and textdescriptives
  - [ ] Add synonym list from DaCy

Todo:
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