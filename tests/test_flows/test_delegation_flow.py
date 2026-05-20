import pytest
from app.flow.delegation import DelegationFlow
from app.agent.base import BaseAgent


class MockAgent(BaseAgent):
    name: str = "mock"
    description: str = "Mock agent for testing"

    async def step(self) -> str:
        return "mock step"


@pytest.mark.asyncio
async def test_delegation_flow_executes_primary():
    agent = MockAgent(name="primary")
    flow = DelegationFlow(agents={"primary": agent})
    result = await flow.execute("test")
    assert "Delegation Flow Result" in result


@pytest.mark.asyncio
async def test_delegation_flow_no_primary():
    flow = DelegationFlow(agents={})
    result = await flow.execute("test")
    assert "No primary agent" in result


@pytest.mark.asyncio
async def test_delegate_to_existing_agent():
    agent = MockAgent(name="worker")
    flow = DelegationFlow(agents={"primary": agent, "worker": agent})
    result = await flow.delegate_to("worker", "do something")
    assert result is not None


@pytest.mark.asyncio
async def test_delegate_to_nonexistent_agent():
    agent = MockAgent(name="primary")
    flow = DelegationFlow(agents={"primary": agent})
    result = await flow.delegate_to("missing", "do something")
    assert "not available" in result
