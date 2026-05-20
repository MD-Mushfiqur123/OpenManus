import pytest
from app.tool.base import ToolResult, CLIResult, ToolFailure


class TestToolResult:
    def test_output_field(self):
        r = ToolResult(output="hello")
        assert r.output == "hello"

    def test_error_field(self):
        r = ToolResult(error="something broke")
        assert r.error == "something broke"

    def test_bool_true_with_output(self):
        assert bool(ToolResult(output="data")) is True

    def test_bool_false_empty(self):
        assert bool(ToolResult()) is False

    def test_str_output(self):
        assert str(ToolResult(output="data")) == "data"

    def test_str_error(self):
        r = ToolResult(error="fail")
        assert "Error: fail" in str(r)

    def test_add_two_results(self):
        r1 = ToolResult(output="hello ")
        r2 = ToolResult(output="world")
        r3 = r1 + r2
        assert r3.output == "hello world"

    def test_add_with_error(self):
        r1 = ToolResult(output="hello")
        r2 = ToolResult(error="fail")
        r3 = r1 + r2
        assert r3.output == "hello"
        assert r3.error == "fail"

    def test_replace_output(self):
        r = ToolResult(output="old")
        r2 = r.replace(output="new")
        assert r2.output == "new"


class TestCLIResult:
    def test_inherits_tool_result(self):
        r = CLIResult(output="cli output")
        assert isinstance(r, ToolResult)
        assert r.output == "cli output"


class TestToolFailure:
    def test_inherits_tool_result(self):
        r = ToolFailure(error="failed")
        assert isinstance(r, ToolResult)
        assert r.error == "failed"
