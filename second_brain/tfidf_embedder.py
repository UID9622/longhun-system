# -*- coding: utf-8 -*-
"""#龍芯⚡️2026-06-29-SECOND-BRAIN-TFIDF-EMBEDDER-v1.0
本地无网络降级嵌入：char-ngram TF-IDF + TruncatedSVD
用于 sentence-transformers 不可用或网络不可达时。
"""
import pickle
from pathlib import Path
from typing import List, Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD


class TfidfSvdEmbedder:
    def __init__(self, n_components: int = 128, cache_path: Path = None):
        self.n_components = n_components
        self.cache_path = cache_path
        self.vectorizer = TfidfVectorizer(
            analyzer="char",
            ngram_range=(2, 4),
            max_features=30000,
            sublinear_tf=True,
        )
        self.svd = TruncatedSVD(n_components=n_components, random_state=42)
        self._fitted = False
        if cache_path and cache_path.exists():
            self._load_cache()

    def _load_cache(self):
        with open(self.cache_path, "rb") as f:
            state = pickle.load(f)
        self.vectorizer = state["vectorizer"]
        self.svd = state["svd"]
        self._fitted = True

    def _save_cache(self):
        if self.cache_path:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_path, "wb") as f:
                pickle.dump({"vectorizer": self.vectorizer, "svd": self.svd}, f)

    def fit(self, texts: List[str]) -> "TfidfSvdEmbedder":
        if self._fitted:
            return self
        tfidf = self.vectorizer.fit_transform(texts)
        self.svd.fit(tfidf)
        self._fitted = True
        self._save_cache()
        return self

    def transform(self, texts: List[str]) -> Optional[List[List[float]]]:
        if not self._fitted:
            return None
        tfidf = self.vectorizer.transform(texts)
        dense = self.svd.transform(tfidf)
        return dense.tolist()

    @property
    def is_fitted(self) -> bool:
        return self._fitted
