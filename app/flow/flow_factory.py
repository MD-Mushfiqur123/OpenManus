from typing import Dict, List, Type, Union

from app.agent.base import BaseAgent
from app.flow.base import BaseFlow
from app.flow.delegation import DelegationFlow
from app.flow.human_loop import HumanInTheLoopFlow
from app.flow.parallel import ParallelFlow
from app.flow.planning import PlanningFlow


class FlowFactory:
    """Factory for creating flow instances"""

    _flows: Dict[str, Type[BaseFlow]] = {
        "planning": PlanningFlow,
        "parallel": ParallelFlow,
        "delegation": DelegationFlow,
        "human_loop": HumanInTheLoopFlow,
    }

    @classmethod
    def create_flow(cls, flow_type: str, **kwargs) -> BaseFlow:
        flow_class = cls._flows.get(flow_type)
        if not flow_class:
            raise ValueError(f"Unknown flow type: {flow_type}. Available: {list(cls._flows.keys())}")
        return flow_class(**kwargs)

    @classmethod
    def register_flow(cls, flow_type: str, flow_class: Type[BaseFlow]):
        cls._flows[flow_type] = flow_class
