import pytest
from app.tool.base import BaseTool
from app.tool.terminate import Terminate
from app.tool.tool_collection import ToolCollection


class TestBaseTool:
    def test_name_description(self):
        tool = Terminate()
        assert tool.name == "terminate"
        assert "terminate" in tool.description.lower()

    def test_to_param_format(self):
        tool = Terminate()
        param = tool.to_param()
        assert param["type"] == "function"
        assert param["function"]["name"] == "terminate"

    def test_success_response_str(self):
        tool = Terminate()
        result = tool.success_response("done")
        assert result.output == "done"
        assert result.error is None

    def test_success_response_dict(self):
        tool = Terminate()
        result = tool.success_response({"status": "ok"})
        assert "status" in result.output

    def test_fail_response(self):
        tool = Terminate()
        result = tool.fail_response("error msg")
        assert result.error == "error msg"


class TestToolCollection:
    def setup_method(self):
        self.collection = ToolCollection(Terminate())

    def test_tool_map_contains_tools(self):
        assert "terminate" in self.collection.tool_map

    def test_to_params_returns_list(self):
        params = self.collection.to_params()
        assert isinstance(params, list)
        assert len(params) >= 1

    def test_add_tool(self):
        from app.tool.create_chat_completion import CreateChatCompletion
        self.collection.add_tool(CreateChatCompletion(str))
        assert "create_chat_completion" in self.collection.tool_map

    @pytest.mark.asyncio
    async def test_execute_existing_tool(self):
        result = await self.collection.execute(name="terminate", tool_input={"status": "success"})
        assert result is not None

    @pytest.mark.asyncio
    async def test_execute_nonexistent_tool(self):
        result = await self.collection.execute(name="nonexistent", tool_input={})
        assert result is not None
