# Overview of Augmenters

The following tables list all the available augmenters in augmenty, along with a short description.It also list all of the labels which the augmenters respects. For instance if you wish to train an namedentity recognition pipeline you should not use augmenters which does not respect entity labels. Lastly the package includes a list of references to any data or packages used as well as references to example application of the augmenter in practice.

| Augmenter name | Description | Respects | References |
| :---: | --- | --- | --- |
| **char_replace.v1** | Creates an augmenter that replaces a character with a random character from replace dict | token labels, dependency parsing, entity labels, document labels |  |
| **char_replace_random.v1** | Creates an augmenter that replacies a character with a random character from the | token labels, dependency parsing, entity labels, document labels |  |
| **char_swap.v1** | Creates an augmenter that swaps two characters in a token with a given probability. | token labels, dependency parsing, entity labels, document labels |  |
| **conditional_token_casing.v1** | Creates an augmenter that conditionally cases the first letter of a token based on the getter. | token labels, dependency parsing, entity labels, document labels |  |
| **da_historical_noun_casing.v1** | Creates an augmenter that capitalizes nouns. | token labels, dependency parsing, entity labels, document labels |  |
| **da_æøå_replace.v1** | Creates an augmenter that augments æ, ø, and å into their spelling variants ae, oe, aa. | token labels, dependency parsing, entity labels, document labels |  |
| **ents_format.v1** | Creates an augmenter which reorders and formats a entity according to reordering and formatting functions. | token labels, dependency parsing, entity labels, document labels |  |
| **ents_replace.v1** | Create an augmenter which replaces an entity based on a dictionary lookup. | token labels, dependency parsing, entity labels, document labels |  |
| **grundtvigian_spacing_augmenter.v1** | The Danish philosopher N.F.S. Grundtvig used letter spacing to add | token labels, dependency parsing, entity labels, document labels |  |
| **keystroke_error.v1** | Creates a augmenter which augments a text with plausible typos based on keyboard distance. | token labels, dependency parsing, entity labels, document labels |  |
| **per_replace.v1** | Create an augmenter which replaces a name (PER) with a news sampled from the names dictionary. | token labels, dependency parsing, entity labels, document labels |  |
| **random_casing.v1** | Create an augment that randomly changes the casing of the document. | token labels, dependency parsing, entity labels, document labels |  |
| **random_starting_case.v1** | Creates an augmenter which randomly cases the first letter in each token. | token labels, dependency parsing, entity labels, document labels |  |
| **remove_spacing.v1** | Creates an augmenter that removes spacing with a given probability. | token labels, dependency parsing, entity labels, document labels |  |
| **spacing_insertion.v1** | Creates and augmneter that randomly adds a space after a chara cter. Tokens are kept the same. | token labels, dependency parsing, entity labels, document labels |  |
| **spacy.lower_case.v1** | Create a data augmentation callback that converts documents to lowercase. | token labels, dependency parsing, entity labels, document labels |  |
| **spacy.orth_variants.v1** | Create a data augmentation callback that uses orth-variant replacement. | token labels, dependency parsing, entity labels, document labels |  |
| **spongebob.v1** | Create an augmneter that converts documents to SpOnGeBoB casing. | token labels, dependency parsing, entity labels, document labels |  |
| **token_replace.v1** | Creates an augmenter swaps a token with its synonym based on a dictionary. | token labels, dependency parsing, entity labels, document labels |  |
| **token_swap.v1** | Creates an augmenter that randomly swaps two neighbouring tokens. | token labels, dependency parsing, entity labels, document labels | Usage: [Wei and Zau (2019)](https://arxiv.org/abs/1901.11196?utm_campaign=Weekly%20Kaggle%20News&utm_medium=email&utm_source=Revue%20newsletter) |
| **upper_case.v1** | Create an augmenter that converts documents to uppercase. | token labels, dependency parsing, entity labels, document labels |  |
| **wordnet_synonym.v1** | Creates an augmenter swaps a token with its synonym based on a dictionary. | token labels, dependency parsing, entity labels, document labels | Data: [Miller (1998) (1998)](https://www.google.com/books?hl=da&lr=&id=Rehu8OOzMIMC&oi=fnd&pg=PR11&dq=WordNet:+An+electronic+lexical+database&ots=IsieQmWUg8&sig=06asxxcQ1I3i9C1TcEcz7bv62Kw), Package: [Steven (2006)](https://www.nltk.org), Usage: [Wei and Zau (2019)](https://arxiv.org/abs/1901.11196?utm_campaign=Weekly%20Kaggle%20News&utm_medium=email&utm_source=Revue%20newsletter) |