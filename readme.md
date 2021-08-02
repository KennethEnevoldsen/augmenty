
Work order:
- [ ] test package

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
install augmenty[all]  # includes NLTK 

FAQ:

- Many of these augmenters are completely useless for training?
That is true, many of these is rarely something you would train with. For instance randomly adding or removing spacing. However, augmentation can just as well be used to test whether a system is robust to certain variations.

- I wish to add an augmenter, how do I do it?
(link to auto PR)

- Does augmenty run on my OS?
(insert pytest)

- Can I use augmenty without using spacy?
(show utility function example)
