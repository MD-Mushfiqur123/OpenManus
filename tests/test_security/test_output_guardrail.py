import pytest
from app.tool.security.output_guardrail import OutputGuardrail
from app.tool.base import ToolResult
from app.schema import Message


class TestOutputGuardrail:
    def setup_method(self):
        self.guardrail = OutputGuardrail()

    def test_filter_output_normal(self):
        result = self.guardrail.filter_output("Hello world")
        assert result == "Hello world"

    def test_filter_output_truncates_long(self):
        long = "x" * 200000
        result = self.guardrail.filter_output(long, max_length=1000)
        assert len(result) <= 1000

    def test_filter_output_strips_ansi(self):
        result = self.guardrail.filter_output("\x1b[31mRed\x1b[0m")
        assert "Red" in result

    def test_filter_tool_result(self):
        tr = ToolResult(output="Safe output")
        result = self.guardrail.filter_tool_result(tr)
        assert result.output == "Safe output"

    def test_filter_message(self):
        msg = Message.user_message("Safe message")
        result = self.guardrail.filter_message(msg)
        assert result.content == "Safe message"
