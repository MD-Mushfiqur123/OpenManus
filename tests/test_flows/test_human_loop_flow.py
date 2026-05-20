import pytest
from app.flow.human_loop import HumanInTheLoopFlow
from app.agent.base import BaseAgent


class MockAgent(BaseAgent):
    name: str = "mock"
    description: str = "Mock agent"

    async def step(self) -> str:
        return "done"


@pytest.mark.asyncio
async def test_human_loop_executes():
    agent = MockAgent(name="primary")
    flow = HumanInTheLoopFlow(agents={"primary": agent})
    result = await flow.execute("test task")
    assert "Human-in-the-Loop Result" in result


@pytest.mark.asyncio
async def test_human_loop_no_primary():
    flow = HumanInTheLoopFlow(agents={})
    result = await flow.execute("test")
    assert "No primary agent" in result


@pytest.mark.asyncio
async def test_run_with_checkpoint():
    agent = MockAgent(name="worker")
    flow = HumanInTheLoopFlow(agents={"worker": agent})
    result = await flow.run_with_checkpoint("worker", "task", "checkpoint review")
    assert result is not None
