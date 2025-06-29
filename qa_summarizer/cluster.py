from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering


def _preprocess(text: str) -> str:
    if not text:
        return ''
    return ' '.join(text.replace('\n', ' ').split())


@dataclass
class ClusterResult:
    questions: List[str]
    representative: str


def cluster_questions(questions: List[str], similarity_threshold: float = 0.75, max_clusters: int = 15) -> List[ClusterResult]:
    if not questions:
        return []

    processed = [_preprocess(q) for q in questions]
    vectorizer = TfidfVectorizer(max_features=1000)
    tfidf = vectorizer.fit_transform(processed)
    sim_matrix = cosine_similarity(tfidf)
    distance_matrix = 1 - sim_matrix

    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=1 - similarity_threshold,
        linkage='average',
        metric='precomputed'
    )
    labels = clustering.fit_predict(distance_matrix)

    clusters: Dict[int, List[int]] = {}
    for idx, label in enumerate(labels):
        clusters.setdefault(label, []).append(idx)

    results = []
    for label, idxs in clusters.items():
        cluster_questions = [questions[i] for i in idxs]
        if len(idxs) > 1:
            avg_sims = []
            for i in idxs:
                sim_sum = sum(sim_matrix[i][j] for j in idxs if i != j)
                avg_sims.append(sim_sum / (len(idxs) - 1))
            rep_idx = idxs[int(np.argmax(avg_sims))]
        else:
            rep_idx = idxs[0]
        representative = questions[rep_idx]
        results.append(ClusterResult(cluster_questions, representative))

    results.sort(key=lambda c: len(c.questions), reverse=True)
    if len(results) > max_clusters:
        results = results[:max_clusters]
    return results
