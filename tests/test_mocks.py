import pytest
from tests.mocks.mock_llm import MockLLM
from tests.mocks.mock_tool import MockTool, FailingTool
from tests.mocks.mock_config import create_mock_config
from app.schema import ToolCall, Function


class TestMockLLM:
    def test_default_response(self):
        llm = MockLLM()
        assert llm.call_count == 0

    def test_add_response(self):
        llm = MockLLM()
        llm.add_response("custom")
        assert len(llm.responses) == 1

    def test_add_tool_call_response(self):
        llm = MockLLM()
        llm.add_tool_call_response("bash", '{"cmd": "ls"}')
        assert len(llm.responses) == 1


class TestMockTool:
    @pytest.mark.asyncio
    async def test_execute(self):
        tool = MockTool()
        result = await tool.execute(test="value")
        assert result is not None

    def test_execution_count(self):
        tool = MockTool()
        assert tool.execution_count == 1


class TestFailingTool:
    @pytest.mark.asyncio
    async def test_execute_fails(self):
        tool = FailingTool()
        result = await tool.execute()
        assert result.error is not None


class TestMockConfig:
    def test_create(self):
        config = create_mock_config()
        assert config.llm is not None
        assert "default" in config.llm
