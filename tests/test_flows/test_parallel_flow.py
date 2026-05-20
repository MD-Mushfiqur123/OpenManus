import pytest
from unittest.mock import AsyncMock

from app.flow.parallel import ParallelFlow
from app.agent.base import BaseAgent


class MockAgent(BaseAgent):
    name: str = "mock"
    description: str = "Mock agent for testing"

    async def step(self) -> str:
        return "mock step"


@pytest.mark.asyncio
async def test_parallel_flow_executes_all_agents():
    agent1 = MockAgent(name="agent1")
    agent2 = MockAgent(name="agent2")
    flow = ParallelFlow(agents={"a1": agent1, "a2": agent2})
    result = await flow.execute("test input")
    assert "Parallel Execution Results" in result
    assert "agent1" in result or "a1" in result
    assert "agent2" in result or "a2" in result


@pytest.mark.asyncio
async def test_parallel_flow_empty_agents():
    flow = ParallelFlow(agents={})
    result = await flow.execute("test")
    assert "No agents configured" in result


@pytest.mark.asyncio
async def test_parallel_flow_single_agent():
    agent = MockAgent(name="single")
    flow = ParallelFlow(agents={"default": agent})
    result = await flow.execute("test")
    assert "Parallel Execution Results" in result
