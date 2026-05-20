import pytest
from app.tool.security.sanitizer import Sanitizer
from app.exceptions import SecurityError


class TestSanitizer:
    def test_sanitize_command_normal(self):
        result = Sanitizer.sanitize_command("echo hello")
        assert result == "echo hello"

    def test_sanitize_command_rm_rf(self):
        with pytest.raises(SecurityError):
            Sanitizer.sanitize_command("rm -rf /")

    def test_sanitize_command_dd(self):
        with pytest.raises(SecurityError):
            Sanitizer.sanitize_command("dd if=/dev/zero of=/dev/sda")

    def test_sanitize_path_normal(self):
        result = Sanitizer.sanitize_path("/workspace/file.txt")
        assert isinstance(result, str)
        assert "file.txt" in result
        assert ".." not in result

    def test_sanitize_path_traversal(self):
        result = Sanitizer.sanitize_path("/workspace/../../etc/passwd")
        assert ".." not in result

    def test_sanitize_shell_args(self):
        result = Sanitizer.sanitize_shell_args(["echo", "hello; rm -rf /"])
        assert ";" not in result[1]

    def test_sanitize_filename_normal(self):
        result = Sanitizer.sanitize_filename("test.txt")
        assert result == "test.txt"

    def test_sanitize_filename_path_separators(self):
        result = Sanitizer.sanitize_filename("../../test.txt")
        assert "/" not in result
