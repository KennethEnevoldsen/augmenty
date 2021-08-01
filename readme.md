
Todo:
- [ ] Create a keyboard for each spacy language
- [ ] Add synonym list for each spacy lang (check NL augment)
- [ ] Add entity, names ... (check NL augment)
- [ ] Create tests for all augmenters
- [ ] Function to create a list of all augmenters and examples (maybe with a given sentence)
- [ ] A list of what each function respect (i.e. does augmenter X respect POS-tags?) - maybe this can be done with catalogue?
- [ ] create yield both augmenter (yield both augmented and unaugmented example)
- [ ] normalize framing for create functions
- [ ] remove defaults from the augmenter and move them to the create func.
- [ ] Create a searchable table either using augmenters either using https://sphinxcontrib-needs.readthedocs.io/en/latest/directives/needtable.html or https://github.com/crate/sphinx_csv_filter 


- [ ] Create a list of augmenters to add
  - [ ] Check NL augment
  - [ ] check nlpaug
  - [ ] Emoji EOS - replace punctuations with emojis (maybe use the [tweeteval](https://huggingface.co/cardiffnlp/twitter-roberta-base-emoji?text=I+like+you.+I+love+you) model)
  - [ ] names -> Usernames


Considered augmenters:
- Random insertion of token:
  - Unsure of how this would even be represented in a dependency tree or what POS tag to assign it to. Could work for span classification tasks though.
- Random deletion of token:
  - Unsure of how this would even be represented in a dependency tree or what POS tag to assign it to. Could work for span classification tasks though.

Additions to current augmenters:
- [ ] Synonym replacement
  - [ ] Adapt to allow replace with multi word expression. This is problematic as fixing the dep. tree might be difficult. If we ignore this we just have to fix the tokens.




Tutorials
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


FAQ:

- Many of these augmenters are completely useless for training?
That is true, many of these is rarely something you would train with. For instance randomly adding or removing spacing. However, augmentation can just as well be used to test whether a system is robust to certain variations.

- I wish to add an augmenter, how do I do it?
(link to auto PR)

- Does augmenty run on my OS?
(insert pytest)

- Can I use augmenty without using spacy?
(show utility function example)
