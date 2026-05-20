from unittest.mock import AsyncMock, MagicMock
from typing import Any, Optional, List

from app.llm import LLM
from app.schema import Message, ToolCall, Function


class MockLLM(LLM):
    """Mock LLM for testing agents without API calls"""

    def __new__(cls, *args, **kwargs):
        instance = super(LLM, cls).__new__(cls)
        return instance

    def __init__(self, responses: Optional[List[Any]] = None):
        self.responses = responses or []
        self.call_count = 0
        self.ask_history: List[dict] = []
        self.ask_tool_history: List[dict] = []

    async def ask(self, messages, system_msgs=None, **kwargs) -> Message:
        self.call_count += 1
        self.ask_history.append({"messages": messages, "system_msgs": system_msgs, "kwargs": kwargs})
        if self.responses:
            resp = self.responses.pop(0)
            return Message.assistant_message(resp) if isinstance(resp, str) else resp
        return Message.assistant_message("Mock response")

    async def ask_tool(self, messages, system_msgs=None, tools=None, tool_choice=None, **kwargs):
        self.call_count += 1
        self.ask_tool_history.append({
            "messages": messages, "system_msgs": system_msgs,
            "tools": tools, "tool_choice": tool_choice, "kwargs": kwargs
        })
        if self.responses:
            return self.responses.pop(0)
        msg = Message.assistant_message("Mock tool response")
        return msg

    def add_response(self, response: Any):
        self.responses.append(response)

    def add_tool_call_response(self, tool_name: str, tool_args: str = "{}", content: str = ""):
        """Add a response that includes a tool call"""
        tc = ToolCall(id="call_mock", type="function", function=Function(name=tool_name, arguments=tool_args))
        msg = Message.from_tool_calls(tool_calls=[tc], content=content)
        self.responses.append(msg)
