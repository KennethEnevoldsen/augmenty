from typing import List, Optional

import numpy as np
from pydantic import BaseModel
from spacy.vocab import Vocab


class static_embedding(BaseModel):
    """A utility object for computing most similar word vectors using
    precomputed normalized vectors.

    Args:
        unit_vectors: The normalized word vectors
        keys: The mapping from vectors to hash values
        vocab: A SpaCy vocabulary
    """

    class Config:
        arbitrary_types_allowed = True

    unit_vectors: Optional[np.ndarray] = None  # type: ignore
    keys: Optional[List[int]] = None  # type: ignore
    vocab: Optional[Vocab] = None  # type: ignore

    def most_similar(self, target: str, n: int) -> List[str]:  # type: ignore
        """Calculate most similar vectors using cosine similarity.

        Args:
            target: Target in the vocabulary
            n: The number of words of interest.

        Returns:
            A list of most similar word.
        """
        target = self.vocab.get_vector(target)  # type: ignore
        unit_target = target / np.linalg.norm(target)  # type: ignore
        distances = np.dot(self.unit_vectors, unit_target)  # type: ignore
        d = distances.argsort()[::-1][:n]
        return [self.vocab.strings[self.keys[w]] for w in d]  # type: ignore

    @staticmethod
    def from_vocab(vocab: Vocab) -> "static_embedding":
        keys = list(vocab.vectors.keys())

        vectors = vocab.vectors.data
        unit_vectors = vectors.copy()
        lengths = np.linalg.norm(unit_vectors, axis=-1)  # type: ignore
        # only normalise non-zero length (to avoid zero division errors)
        unit_vectors[lengths > 0] = unit_vectors / lengths[lengths > 0][:, np.newaxis]
        return static_embedding(unit_vectors=unit_vectors, keys=keys, vocab=vocab)

    def update_from_vocab(self, vocab: Vocab):
        emb = self.from_vocab(vocab)
        self.vocab = emb.vocab
        self.keys = emb.keys
        self.unit_vectors = emb.unit_vectors

    def __contains__(self, key: str) -> bool:
        if key in self.vocab:  # type: ignore
            v = self.vocab.get_vector(key)  # type: ignore
            if np.linalg.norm(v) > 0:  # type: ignore
                return True
        return False
