from augmenty.token.static_embedding_util import static_embedding

import spacy

import pytest

@pytest.fixture()
def nlp():
    nlp = spacy.load("en_core_web_md")
    return nlp


def test_static_embedding_util(nlp):
    empty_embedding = static_embedding()

    empty_embedding.update_from_vocab(nlp.vocab)
    assert empty_embedding.vocab is not None
    assert "testing" in empty_embedding.most_similar("test", n=10)

    emb = static_embedding.from_vocab(nlp.vocab)

    assert "testing" in emb.most_similar("test", n=10)
    
