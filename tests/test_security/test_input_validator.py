import pytest
from app.tool.security.input_validator import InputValidator
from app.exceptions import ValidationError


class TestInputValidator:
    def setup_method(self):
        self.validator = InputValidator()

    def test_validate_tool_input_passes_valid_params(self):
        params = {"cmd": "echo hello", "path": "/workspace/file.txt", "text": "some content"}
        result = self.validator.validate_tool_input("bash", params)
        assert result == params

    def test_validate_tool_input_detects_dangerous_command(self):
        params = {"cmd": "rm -rf /"}
        with pytest.raises(ValidationError):
            self.validator.validate_tool_input("bash", params)

    def test_validate_tool_input_detects_path_traversal(self):
        params = {"path": "../../etc/passwd"}
        with pytest.raises(ValidationError):
            self.validator.validate_tool_input("file_operators", params)

    def test_validate_tool_input_empty_params(self):
        result = self.validator.validate_tool_input("bash", {})
        assert result == {}

    def test_validate_llm_input_normal_prompt(self):
        result = self.validator.validate_llm_input("Tell me a story")
        assert "Tell me a story" in result

    def test_validate_llm_input_truncates_long_prompt(self):
        long = "x" * 200000
        result = self.validator.validate_llm_input(long)
        assert len(result) <= 100000
