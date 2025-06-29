from __future__ import annotations

import argparse
import asyncio
import os
from typing import List

from .sheet import fetch_questions
from .cluster import cluster_questions
from .gemini import GeminiClient
from .cache import load_cache, save_cache


async def process(sheet_url: str, max_questions: int, gemini_key: str | None, calls_per_minute: int):
    df, sheet_id, modified_time = fetch_questions(sheet_url, max_questions)

    cached = load_cache(sheet_id, modified_time)
    if cached is not None:
        return cached

    questions = df['Question'].astype(str).tolist()
    clusters = cluster_questions(questions)

    gemini = GeminiClient(api_key=gemini_key, calls_per_minute=calls_per_minute)
    results = []
    try:
        for idx, cluster in enumerate(clusters, 1):
            top3 = cluster.questions[:3]
            summary, answer = await gemini.generate(top3)
            results.append({
                'cluster_no': idx,
                'questions': top3,
                'summary': summary,
                'answer': answer,
            })
    finally:
        await gemini.close()

    save_cache(sheet_id, modified_time, results)
    return results


def output_markdown(results: List[dict]):
    for r in results:
        print(f"## 質問クラスター {r['cluster_no']}")
        for q in r['questions']:
            print(f"- {q}")
        print(r['answer'])
        print()


def main():
    parser = argparse.ArgumentParser(description='Question summarizer')
    parser.add_argument('--sheet-url', required=True)
    parser.add_argument('--max-questions', type=int, default=1000)
    parser.add_argument('--gemini-key')
    parser.add_argument('--calls-per-minute', type=int, default=int(os.getenv('CALLS_PER_MINUTE', '60')))
    args = parser.parse_args()

    results = asyncio.run(process(args.sheet_url, args.max_questions, args.gemini_key, args.calls_per_minute))
    output_markdown(results)


if __name__ == '__main__':
    main()
