import pytest
from app.config import LLMSettings, DaytonaSettings, BrowserSettings


class TestLLMSettings:
    def test_required_fields(self):
        settings = LLMSettings(
            model="gpt-4o",
            base_url="https://api.openai.com/v1",
            api_key="sk-test",
            api_type="openai",
            api_version="",
        )
        assert settings.model == "gpt-4o"
        assert settings.max_tokens == 4096

    def test_default_max_tokens(self):
        settings = LLMSettings(
            model="gpt-4o",
            base_url="https://api.openai.com/v1",
            api_key="sk-test",
            api_type="openai",
            api_version="",
        )
        assert settings.max_tokens == 4096


class TestDaytonaSettings:
    def test_default_api_key_is_empty(self):
        settings = DaytonaSettings()
        assert settings.daytona_api_key == ""

    def test_custom_api_key(self):
        settings = DaytonaSettings(daytona_api_key="sk-test-key")
        assert settings.daytona_api_key == "sk-test-key"

    def test_default_server_url(self):
        settings = DaytonaSettings()
        assert "daytona.io" in settings.daytona_server_url


class TestToolResult:
    def test_tool_result_truthy(self):
        from app.tool.base import ToolResult
        r = ToolResult(output="hello")
        assert bool(r) is True

    def test_tool_result_falsy(self):
        from app.tool.base import ToolResult
        r = ToolResult()
        assert bool(r) is False

    def test_tool_result_str_error(self):
        from app.tool.base import ToolResult
        r = ToolResult(error="fail")
        assert "Error: fail" in str(r)

    def test_tool_result_str_output(self):
        from app.tool.base import ToolResult
        r = ToolResult(output="success")
        assert str(r) == "success"
