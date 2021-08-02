# Augmenters

This contains a list of augmenters to add as well as augmenters that are already added.


## Character augmentations
------

Character-based augmentation augments on a character level. Typically these include swapping and replacing characters.


| Status | Name            | Description                                   | References      |
| ------ | --------------- | --------------------------------------------- | --------------- |
| 💭     | Emoji EOS       |  replace end of sentence with an emojis e.g. using [tweeteval](https://huggingface.co/cardiffnlp/twitter-roberta-base-emoji?text=I+like+you.+I+love+you) | [Barbieri (2020)](https://arxiv.org/pdf/2010.12421.pdf) |
| ✅     | random_casing.v1      | random change casing of a character |  |
| ✅     | char_replace.v1      | An augmenter that replaces a character with a random character from replacement dict |  |
| ✅     | char_replace_random.v1      | Replaces a character with a random character from a defined keyboard. A special case of char_replace.v1 | |
| ✅     | keystroke_error.v1      | Replaces a character with a neightbouring character on the keyboard. A special case of char_replace.v1 |  |
| ✅     | remove_spacing.v1      | Removed spacing at random |  |
| ✅     | char_swap.v1      | Swaps two neightbouring characters in a sentence |  |


<br /> 

<details>
  <summary>What does the status mean?</summary>

💭 : Idea, will potentially be added

🕑 : Planned, will likely be added in the following update

✅ : Finished

</details>

<br /> 


## Token augmentations
------

Character-based augmentation augments on a token level. Typically these include swapping and replacing characters.

| Status | Name            | Description                                   | References      |
| ------ | --------------- | --------------------------------------------- | --------------- |
| ✅      | wordnet_synonym.v1      |  replace a word with its synonym based on wordnet. | Data: [Miller (1998)](https://www.google.com/books?hl=da&lr=&id=Rehu8OOzMIMC&oi=fnd&pg=PR11&dq=WordNet:+An+electronic+lexical+database&ots=IsieQmWUg8&sig=06asxxcQ1I3i9C1TcEcz7bv62Kw) Package: [Steven (2006)](https://www.nltk.org) Usage: [Wei and Zau (2019)](https://arxiv.org/abs/1901.11196?utm_campaign=Weekly%20Kaggle%20News&utm_medium=email&utm_source=Revue%20newsletter) |
| ✅     | token_replace.v1       |  replace a word with another based on a dictionary lookup. E.g. for synonym replacements. | Usage: [Wei and Zau (2019)](https://arxiv.org/abs/1901.11196?utm_campaign=Weekly%20Kaggle%20News&utm_medium=email&utm_source=Revue%20newsletter) |
| ✅     | random_starting_case.v1       |  Randomly case the starting case |  |
| ✅     | conditional_token_casing.v1       |   conditionally cases the first letter of a token |  |
| ✅     | grundtvigian_spacing.v1      |  Random use letter spacing to add e m p h a s i s  to words  |  |
| ✅     | spacing_insertion.v1      |  Randomly adds a space in a token  |  |
| ✅     | token_swap.v1      |  Randomly swaps two neighbouring tokens  | Usage: [Wei and Zau (2019)](https://arxiv.org/abs/1901.11196?utm_campaign=Weekly%20Kaggle%20News&utm_medium=email&utm_source=Revue%20newsletter) |


## Span augmentations
------
Span-based augmentation augments on a span level. These could include rephrasing a sentence or replacing and entity span.

| Status | Name            | Description                                   | References      |
| ------ | --------------- | --------------------------------------------- | --------------- |
| ✅     | ents_replace.v1       |  Replace an entity based on a dictionary. |  |
| ✅     | per_replace.v1       | replaces a name (PER) with a news sampled from the names dictionary. A special case of ents_replace.v1 |  |
| ✅     | ents_format.v1       | An augmenter which reorders and formats a entity to increase lexical diversity |  |
| 🕑     | usernames.v1       |  Replace a name with a usernanme. A special case of per.v1 |  |
| 🕑     | insertion.v1 | Randomly inserts a token. Unsure of how this would even be represented in a dependency tree or what POS tag to assign it to. Could work for span classification tasks though. | Usage: [Wei and Zau (2019)](https://arxiv.org/abs/1901.11196?utm_campaign=Weekly%20Kaggle%20News&utm_medium=email&utm_source=Revue%20newsletter) |
| 🕑     | deletion.v1 |  Random deletion of token. Unsure of how this would even be represented in a dependency tree or what POS tag to assign it to. Could work for span classification tasks though. | Usage: [Wei and Zau (2019)](https://arxiv.org/abs/1901.11196?utm_campaign=Weekly%20Kaggle%20News&utm_medium=email&utm_source=Revue%20newsletter) |

## Doc augmentations
------
Character-based augmentation augments on a token level. Typically these include swapping and replacing characters.

| Status | Name            | Description                                   | References      |
| ------ | --------------- | --------------------------------------------- | --------------- |
| ✅     | upper_case.v1      | Uppercases the entire document |  |
| ✅     | spongebob.v1      | converts document casing to SpOnGeBoB case |  |
| (✅ )     |  lower_case.v1     | lowercase the entire document. Included in spaCy. |  |

## Language-specific augmentations
------
Language-specific augmentations are augmenters intended for a language domain.

### DA: Danish

| Status | Name            | Description                                   | References      |
| ------ | --------------- | --------------------------------------------- | --------------- |
| ✅     | da_æøå_replace.v1      | Replace æ, ø and å with their spelling variations. A special case of char_replace_augmenter.v1 |  |
| ✅     | da_historical_noun_casing.v1      | Uppercases nouns, a special case of conditional_casing.v1 |  |


## Combined Augmenters
------
Combined augmenters are a group of augmenters intended for a specific purpose. These could for instance include augmenters intended to symbolise historic variations or a group of augmenters intended to approximate social media text patterns.

| Status | Name            | Description                                   | References      |
| ------ | --------------- | --------------------------------------------- | --------------- |
| 💭     | da_historic.v1      | A augmenter intended to reflect historic text patterns of Danish |  |
