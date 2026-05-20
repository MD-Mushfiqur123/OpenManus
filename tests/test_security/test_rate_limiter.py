import pytest
from app.tool.security.rate_limiter import RateLimiter


class TestRateLimiter:
    def setup_method(self):
        self.limiter = RateLimiter(default_tokens=5, default_window=60.0)

    @pytest.mark.asyncio
    async def test_acquire_allows_within_limit(self):
        for _ in range(3):
            assert await self.limiter.acquire("test_tool") is True

    @pytest.mark.asyncio
    async def test_acquire_exhausts_limit(self):
        for _ in range(5):
            assert await self.limiter.acquire("exhaust") is True
        assert await self.limiter.acquire("exhaust") is False

    @pytest.mark.asyncio
    async def test_acquire_separate_tools_independent(self):
        for _ in range(5):
            assert await self.limiter.acquire("tool_a") is True
        assert await self.limiter.acquire("tool_b") is True

    @pytest.mark.asyncio
    async def test_get_remaining_returns_count(self):
        for _ in range(3):
            await self.limiter.acquire("test_tool")
        remaining = self.limiter.get_remaining("test_tool")
        assert remaining < 5

    @pytest.mark.asyncio
    async def test_reset_restores_tokens(self):
        for _ in range(5):
            await self.limiter.acquire("test_tool")
        self.limiter.reset("test_tool")
        assert self.limiter.get_remaining("test_tool") == 5
