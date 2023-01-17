from augmenty.token.static_embedding_util import static_embedding

from .fixtures import nlp_en_md  # noqa


def test_static_embedding_util(nlp_en_md):  # noqa F811
    empty_embedding = static_embedding()

    empty_embedding.update_from_vocab(nlp_en_md.vocab)
    assert empty_embedding.vocab is not None
    assert "exams".lower() in empty_embedding.most_similar("test", n=10)

    emb = static_embedding.from_vocab(nlp_en_md.vocab)

    assert "exams" in emb.most_similar("test", n=10)
