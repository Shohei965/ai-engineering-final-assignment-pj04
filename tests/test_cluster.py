import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qa_summarizer.cluster import cluster_questions


def test_cluster_basic():
    questions = [
        'What is AI?',
        'What is artificial intelligence?',
        'How to cook pasta?',
        'How do I cook pasta?'
    ]
    clusters = cluster_questions(questions, similarity_threshold=0.3)
    assert len(clusters) == 2
    sizes = sorted(len(c.questions) for c in clusters)
    assert sizes == [2, 2]
