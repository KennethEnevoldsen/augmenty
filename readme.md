
Todo:
- [ ] Create a keyboard for each spacy langauge
- [ ] Add synonym list for each spacy lang (check NL augment)
- [ ] Add entity, names ... (check NL augment)
- [ ] Create tests for all augmenters
- [ ] Function to create a list of all augmenters and examples (maybe with a given sentence)
- [ ] A list of what each function respect (i.e. does augmenter X respect POS-tags?) - maybe this can be done with catalogue?
- [ ] create yield both augmenter (yield both augmented and unaugmented example)

Augmenters to add:
- [x] Spacing
  - [x] Randomly add spacing between two letters
  - [x] [Grundvigian Letter spacing](http://ceur-ws.org/Vol-2612/short3.pdf)
- [x] Casing
  - [x] spongebob case
  - [x] Random casing
  - [x] random starting case
  - [x] doc uppercase
  - [x] starting case based on POS (maybe using a conditional function which return true or false)
- [x] Danish
  - [x] Historic noun casing
- [ ] Spans
  - [ ] Entity dict augmentation
  - [ ] Emoji EOS - replace punctuations with emojis (maybe using a model like deepmoji)
- [x] Token
  - [x] Swap tokens
  - [x] Synonym replacement



Considered augmenters:
- Random insertion of token:
  - Unsure of how this would even be represented in a dependency tree or what POS tag to assign it to. Could work for span classification tasks though.
- Random deletion of token:
  - Unsure of how this would even be represented in a dependency tree or what POS tag to assign it to. Could work for span classification tasks though.

Additions to current augmenters:
- [ ] Synonym replacement
  - [ ] Adapt to allow replace with multi word expression. This is problematic as fixing the dep. tree might be difficult. If we ignore this we just have to fix the tokens.




FAQ:

- Many of these augmenters are completely useless for training?
That is true, many of these is rarely something you would train with. For instance randomly adding or removing spacing. However, augmentation can just as well be used to test whether a system is robust to certain variations.