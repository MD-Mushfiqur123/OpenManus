import asyncio
import time

from app.logger import logger


class RateLimiter:

    def __init__(self, default_tokens: int = 60, default_window: float = 60.0):
        self.default_tokens = default_tokens
        self.default_window = default_window
        self._buckets: dict[str, dict] = {}
        self._lock = asyncio.Lock()

    async def acquire(self, tool_name: str, tokens: int = 1) -> bool:
        async with self._lock:
            now = time.time()
            if tool_name not in self._buckets:
                self._buckets[tool_name] = {
                    "tokens": self.default_tokens,
                    "last_refill": now,
                    "max_tokens": self.default_tokens,
                    "window": self.default_window,
                }

            bucket = self._buckets[tool_name]
            elapsed = now - bucket["last_refill"]
            refill_rate = bucket["max_tokens"] / bucket["window"]
            bucket["tokens"] = min(
                bucket["max_tokens"],
                bucket["tokens"] + elapsed * refill_rate,
            )
            bucket["last_refill"] = now

            if bucket["tokens"] >= tokens:
                bucket["tokens"] -= tokens
                return True

            logger.warning(f"Rate limit hit for tool '{tool_name}'")
            return False

    def get_remaining(self, tool_name: str) -> int:
        if tool_name not in self._buckets:
            return self.default_tokens
        return int(self._buckets[tool_name]["tokens"])

    def reset(self, tool_name: str):
        self._buckets.pop(tool_name, None)
