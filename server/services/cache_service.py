import hashlib
import json
from typing import Optional


class CacheService:
    """Redis-backed cache for verification results."""

    def __init__(self, redis_url: str):
        self._redis = None
        self._redis_url = redis_url

    async def _get_redis(self):
        if self._redis is None:
            try:
                import redis.asyncio as aioredis

                self._redis = aioredis.from_url(self._redis_url)
                await self._redis.ping()
            except Exception:
                self._redis = None
        return self._redis

    def _key(self, claim_text: str) -> str:
        h = hashlib.sha256(claim_text.encode()).hexdigest()[:16]
        return f"yesveri:claim:{h}"

    async def get(self, claim_text: str) -> Optional[dict]:
        r = await self._get_redis()
        if not r:
            return None
        try:
            data = await r.get(self._key(claim_text))
            return json.loads(data) if data else None
        except Exception:
            return None

    async def set(self, claim_text: str, result: dict, ttl: int = 3600):
        r = await self._get_redis()
        if not r:
            return
        try:
            await r.setex(
                self._key(claim_text),
                ttl,
                json.dumps(result, default=str),
            )
        except Exception:
            pass

    async def is_healthy(self) -> bool:
        r = await self._get_redis()
        if not r:
            return False
        try:
            await r.ping()
            return True
        except Exception:
            return False
