from spacy.language import Language

from augmenty.token.static_embedding_util import StaticEmbedding


def test_static_embedding_util(nlp_en_md: Language):
    empty_embedding = StaticEmbedding()
    empty_embedding.update_from_vocab(nlp_en_md.vocab)
    assert empty_embedding.vocab is not None
    assert "exams".lower() in empty_embedding.most_similar("test", n=10)

    emb = StaticEmbedding.from_vocab(nlp_en_md.vocab)

    assert "exams" in emb.most_similar("test", n=10)
