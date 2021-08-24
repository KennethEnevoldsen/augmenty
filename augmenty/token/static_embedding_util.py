
from typing import  List, Optional

from spacy.vocab import Vocab

from pydantic import BaseModel
import numpy as np


class static_embedding(BaseModel):
    """A utility function for computing most similar word vectors using precomputed normalized vectors

    Args:
        unit_vectors (Optional[np.ndarray]): The normalized word vectors
        keys (Optional[List[int]]): The mapping from vectors to hash values
        vocab (Optional[Vocab]): A SpaCy vocabulary

    Returns:
        static_embedding: An utility class for efficiently calculating static word embeddings.
    """
    class Config:
        arbitrary_types_allowed = True

    unit_vectors: Optional[np.ndarray] = None
    keys: Optional[List[int]] = None
    vocab: Optional[Vocab] = None

    def most_similar(self, target: str, n: int) -> List[str]:
        """calculate most similar vectors using cosine similarity

        Args:
            target (str): Target in the vocabulary
            n (int): The number of words of interest.

        Returns:
            List[str]: A list of most similar word.
        """
        target = self.vocab.get_vector(target)
        unit_target = target / np.linalg.norm(target)
        distances = np.dot(self.unit_vectors, unit_target)
        d = distances.argsort()[::-1][:n]
        return [self.vocab.strings[self.keys[w]] for w in d]

    def __contains__(self, key: str) -> bool:
        if key in self.vocab:
            v = self.vocab.get_vector(key)
            if np.linalg.norm(v) > 0:
                return True
        return False



    @staticmethod
    def from_vocab(vocab: Vocab) -> "static_embedding":
        keys = list(vocab.vectors.keys())
        
        vectors = vocab.vectors.data
        unit_vectors = vectors.copy()
        lengths = np.linalg.norm(unit_vectors, axis=-1)
        # only normalise non-zero length (to avoid zero division errors)
        unit_vectors[lengths > 0] = unit_vectors / lengths[lengths > 0][:, np.newaxis]
        return static_embedding(unit_vectors=unit_vectors, keys=keys, vocab=vocab)

    def update_from_vocab(self, vocab: Vocab):
        emb = self.from_vocab(vocab)
        self.vocab = emb.vocab
        self.keys = emb.keys
        self.unit_vectors = emb.unit_vectors
