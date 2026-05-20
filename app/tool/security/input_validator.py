import re
from typing import Any, Dict

from app.exceptions import ValidationError
from app.logger import logger

DANGEROUS_CMD_PATTERNS = [
    re.compile(r"\brm\s+-rf\s+/"),
    re.compile(r"\bmkfs\b"),
    re.compile(r"\bdd\s+if="),
    re.compile(r"mv\s+/\s+/dev/null"),
    re.compile(r":\(\)\s*\{"),
    re.compile(r">\s*/dev/sda"),
    re.compile(r"\bchmod\s+-R\s+777\s+/"),
    re.compile(r"\bwget\s+.*\||\bcurl\s+.*\|"),
]

MAX_STRING_LENGTH = 10000
MAX_PROMPT_LENGTH = 100000

COMMAND_FIELD_NAMES = {"command", "cmd", "shell_command", "bash_command"}
PATH_FIELD_NAMES = {"path", "file_path", "directory", "dir", "folder"}


class InputValidator:

    def validate_tool_input(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        for key, value in params.items():
            if isinstance(value, str):
                if len(value) > MAX_STRING_LENGTH:
                    raise ValidationError(
                        f"Parameter '{key}' exceeds maximum length of {MAX_STRING_LENGTH} characters"
                    )

                if key in COMMAND_FIELD_NAMES:
                    self._check_dangerous_commands(value, key)

                if key in PATH_FIELD_NAMES:
                    self._check_path_traversal(value, key)

            elif isinstance(value, (list, dict)):
                serialized = str(value)
                if len(serialized) > MAX_STRING_LENGTH:
                    raise ValidationError(
                        f"Parameter '{key}' exceeds maximum serialized length of {MAX_STRING_LENGTH} characters"
                    )

        return params

    def validate_llm_input(self, prompt: str) -> str:
        if not isinstance(prompt, str):
            raise ValidationError("LLM input must be a string")

        if len(prompt) > MAX_PROMPT_LENGTH:
            logger.warning(f"LLM input truncated from {len(prompt)} to {MAX_PROMPT_LENGTH} characters")
            prompt = prompt[:MAX_PROMPT_LENGTH]

        suspicious_patterns = [
            re.compile(r"\{\{.*\{\{"),
            re.compile(r"<\s*script[^>]*>", re.IGNORECASE),
            re.compile(r"system\s*:\s*ignore", re.IGNORECASE),
        ]
        for pattern in suspicious_patterns:
            if pattern.search(prompt):
                logger.warning(f"Suspicious content detected in LLM input matching: {pattern.pattern}")

        return prompt

    def _check_dangerous_commands(self, value: str, key: str):
        for pattern in DANGEROUS_CMD_PATTERNS:
            if pattern.search(value):
                raise ValidationError(
                    f"Parameter '{key}' contains potentially dangerous command pattern: {pattern.pattern}"
                )

    def _check_path_traversal(self, value: str, key: str):
        normalized = value.replace("\\", "/")
        if ".." in normalized.split("/"):
            raise ValidationError(
                f"Parameter '{key}' contains path traversal sequence '..'"
            )
