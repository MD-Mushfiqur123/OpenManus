from app.tool.base import BaseTool, ToolResult
from typing import Any


class MockTool(BaseTool):
    """Mock tool for testing agent behavior"""
    name: str = "mock_tool"
    description: str = "A mock tool for testing"

    async def execute(self, **kwargs) -> Any:
        return ToolResult(output=f"Mock executed with: {kwargs}")

    @property
    def execution_count(self) -> int:
        return 1


class FailingTool(BaseTool):
    """Tool that always fails for testing error handling"""
    name: str = "failing_tool"
    description: str = "A tool that always fails"

    async def execute(self, **kwargs) -> Any:
        return ToolResult(error="Intentional failure for testing")
