#!/usr/bin/env python
# coding: utf-8

# # Introduction to Augmenty
# Augmenty is an augmentation library based on spaCy for augmenting texts. Augmenty differs from other augmentation libraries in that it corrects (as far as possible) the token, 
# sentence and document labels under the augmentation.

# ## Installations
# Before we get ahead of ourselves let us just install the required packages:

# In[1]:


# !pip install augmenty[all]
# # install the spacy pipeline
# !python -m spacy download en_core_web_sm


# ## Introduction
# Augmenty is an augmnentation library for spaCy, consisting of many different augmenters. To get an idea of all the available augmenters you can always try out the use:

# In[3]:


import augmenty

augmenters = augmenty.augmenters()

for augmenter in augmenters:
    print(augmenter)


# To get get more information about an individual augmenter you can always simply use `help` for instance let is say you want to know more about the upper case augmenter you could run: `help(augmenters["upper_case.v1"])`.

# After you have an idea about the augmenter you wish to use loading in augmenters in augmenty is made easy using the `load` command given and given the arguments:

# In[4]:


upper_case_augmenter = augmenty.load("upper_case.v1", level=1.00)  # 100% uppercase


# # Applying the augmentation
# Augmenters in augmenty always take in a spaCy [Language pipeline](https://spacy.io/api/language) and an spaCy [Example](https://spacy.io/api/example) so that it can be easily used while training workflows, however, augmenty also allows for easy application of augmenters to raw text and spaCy [Docs](https://spacy.io/api/doc).
# 
# <br /> 
# 
# <details>
#   <summary>Why examples and not just raw text?</summary>
# 
#   A spaCy example consist of two documents, the labelled document, containing all the correct labels including document classification such as whether a tweet is positive or negative and token classiification such as Part-of-speech-tags and named entities. When augmenting the Example augmenty seeks to correct these tags in accordance with the augmentation. As the raw text does not include these labels it as naturally not possible. For instance if I was to swap two tokens I would want to swap their corresponding labels as well. When swapping tokens augmenty even respect entities and sentences as to not split an entity or swap tokens across sentence borders. You can naturally turn this of if you wish to.
# 
# </details>
# 
# <br />
#  

# ## Applying augmentations on Docs

# In[5]:


import spacy

nlp = spacy.load("en_core_web_sm")
docs = nlp.pipe(
    [
        "Augmentation is a wonderful tool for obtaining higher performance on limited data.",
        "You can also use it to see how robust your model is to changes.",
    ]
)

augmented_docs = augmenty.docs(docs, augmenter=upper_case_augmenter, nlp=nlp)

for doc in augmented_docs:
    print(doc)


# ## Applying augmentations on text
# We can also try it out on text. Let us also try out a new augmenter for replacing entities. Remember you can always use `help(augmenters["ents_replace.v1"])` to figure out which inputs the augmenter takes and see and example.

# In[6]:


texts = ["Augmenty is a wonderful tool for augmentation."]

ent_augmenter = augmenty.load(
    "ents_replace.v1", level=1.00, ent_dict={"ORG": [["SpaCy"], ["The SpaCy Universe"]]}
)

augmented_texts = augmenty.texts(texts, augmenter=ent_augmenter, nlp=nlp)

for text in augmented_texts:
    print(text)


# # Customizing augmenters
# Augmenty is more than a list of augmenters and also contains utilities for dealing with augmenters such as combining and moderating augmenters. 
# 
# # Combining augmenters
# We can start of by combing the entity augmenter with an augmenter which replaces words with their synonym based on wordnet.

# In[7]:


synonym_augmenter = augmenty.load("wordnet_synonym.v1", level=1, lang="en")

combined_aug = augmenty.combine([ent_augmenter, synonym_augmenter])


# In[8]:


augmented_texts = augmenty.texts(texts, augmenter=combined_aug, nlp=nlp)

for text in augmented_texts:
    print(text)


# ## Moderating Augmenters
# Certain augmenters apply augmentation at different levels. For instance the augmenter `keystroke_error.v1` augments examples based on keyboard distances, where each character has a chance to be replaced with a neightbouring character. However, we might wish to apply this augmentation to 5% of characters, but only apply it 50% of the training samples. Using `augmenty.set_doc_level` we can add this last part to any augmenter, thus allowing for more flexibility when using the model.

# In[9]:


keystroke_augmenter = augmenty.load(
    "keystroke_error.v1", keyboard="en_qwerty.v1", level=0.05
)  # 5% if characters

keystroke_augmenter = augmenty.set_doc_level(
    keystroke_augmenter, level=0.5
)  # 50% of texts


# In[10]:


texts = [
    "Augmenty is a wonderful tool for augmentation.",
    "Augmentation is a wonderful tool for obtaining higher performance on limited data.",
    "You can also use it to see how robust your model is to changes.",
]

augmented_texts = augmenty.texts(texts, augmenter=keystroke_augmenter, nlp=nlp)

for text in augmented_texts:
    print(text)


# Similarly one might wish the augment to instead of simply yielding the augmented example also yield the original, such that the trained model always see the actual data.

# In[12]:


token_swap_augmenter = augmenty.load("token_swap.v1", level=0.20)
token_swap_augmenter = augmenty.yield_original(
    token_swap_augmenter
)  # yield both the augmented and original example

augmented_texts = augmenty.texts(texts, augmenter=token_swap_augmenter, nlp=nlp)

for text in augmented_texts:
    print(text)


# # Applying augmentation to Examples or a Corpus
# Examples consists of two docs, one containing the predictions of the model, the other containing the gold labelled document. For this example we will load the DaNE dataset. DaNE include the Danish dependency treebank additionally tagged for named entities. Here we will use synonym replacement to augment a corpus.

# In[1]:


from dacy import datasets

train, dev, test = datasets.dane(splits=["train", "dev", "test"])

from spacy.lang.da import Danish

nlp_da = Danish()

synonym_augmenter = augmenty.load("wordnet_synonym.v1", level=0.2, lang="da")
augmented_corpus = [
    e for example in test(nlp_da) for e in synonym_augmenter(nlp_da, example)
]


# # Creating and Contributing Augmenters
# 
# After using augmenty you might want to create and contribute an augmenter. Most augmenters can be created based on already existing augmenters. For instance the augmenter `per_replace.v1`, which replaces names in a text is a spacial case of the augmenter `ents_replace.v1` with better handling of first and last names. If you want to create an augmenter from scratch following spaCy's [guide](https://spacy.io/usage/training#data-augmentation-custom) on creating custom augmenters is a good start. You can always use augmenters from augmenty as inspiration as well. If you find yourself in troubles feel free to ask in the [augmenty forums](missing). 
# 
# When you are satisfied with your augmenter feel free submit a [pull request](https://github.com/KennethEnevoldsen/augmenty/pulls) to add the augmenter to augmenty.
