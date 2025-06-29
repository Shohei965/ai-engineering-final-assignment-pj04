from __future__ import annotations

import os
import json
import aiohttp
import asyncio
from typing import List, Tuple
from tenacity import retry, stop_after_attempt, wait_exponential

API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent'
TIMEOUT = aiohttp.ClientTimeout(total=30)


class RateLimiter:
    def __init__(self, calls_per_minute: int):
        self._sem = asyncio.Semaphore(calls_per_minute)
        self._period = 60

    async def __aenter__(self):
        await self._sem.acquire()
        asyncio.get_event_loop().call_later(self._period, self._sem.release)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass


class GeminiClient:
    def __init__(self, api_key: str | None = None, calls_per_minute: int = 60):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise RuntimeError('GEMINI_API_KEY not set')
        self.rate_limiter = RateLimiter(calls_per_minute)
        self.session = aiohttp.ClientSession(timeout=TIMEOUT)

    async def close(self):
        await self.session.close()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2))
    async def generate(self, questions: List[str]) -> Tuple[str, str]:
        prompt = self._build_prompt(questions)
        params = {
            'contents': [
                {
                    'role': 'user',
                    'parts': [{'text': prompt}]
                }
            ]
        }
        async with self.rate_limiter:
            async with self.session.post(f'{API_URL}?key={self.api_key}', json=params) as resp:
                data = await resp.json()
                if 'candidates' not in data:
                    raise RuntimeError(str(data))
                text = data['candidates'][0]['content']['parts'][0]['text']
                result = json.loads(text)
                summary = result.get('summary', '')
                answer = result.get('answer', '')
                return summary, answer

    def _build_prompt(self, questions: List[str]) -> str:
        joined = '\n'.join(f'- {q}' for q in questions)
        return (
            '以下の質問を要約し、講師が回答すべき要点を整理し、400字以内で回答を生成してください。'\
            '\n質問:\n' + joined + '\n' +
            'JSONで {"summary":"要約","answer":"回答"} の形式で出力してください。')
