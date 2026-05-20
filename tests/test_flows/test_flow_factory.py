import pytest
from app.flow.flow_factory import FlowFactory
from app.flow.planning import PlanningFlow
from app.flow.parallel import ParallelFlow
from app.flow.delegation import DelegationFlow
from app.flow.human_loop import HumanInTheLoopFlow
from app.agent.base import BaseAgent


class MockAgent(BaseAgent):
    name: str = "mock"
    description: str = "Mock agent"

    async def step(self) -> str:
        return "step"


@pytest.fixture
def agents():
    return {"default": MockAgent()}


class TestFlowFactory:
    def test_create_planning_flow(self, agents):
        flow = FlowFactory.create_flow("planning", agents=agents)
        assert isinstance(flow, PlanningFlow)

    def test_create_parallel_flow(self, agents):
        flow = FlowFactory.create_flow("parallel", agents=agents)
        assert isinstance(flow, ParallelFlow)

    def test_create_delegation_flow(self, agents):
        flow = FlowFactory.create_flow("delegation", agents=agents)
        assert isinstance(flow, DelegationFlow)

    def test_create_human_loop_flow(self, agents):
        flow = FlowFactory.create_flow("human_loop", agents=agents)
        assert isinstance(flow, HumanInTheLoopFlow)

    def test_create_unknown_flow(self, agents):
        with pytest.raises(ValueError):
            FlowFactory.create_flow("unknown", agents=agents)

    def test_register_custom_flow(self, agents):
        FlowFactory.register_flow("custom", PlanningFlow)
        flow = FlowFactory.create_flow("custom", agents=agents)
        assert isinstance(flow, PlanningFlow)
