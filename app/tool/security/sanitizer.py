import os
import re
from pathlib import Path

from app.exceptions import SecurityError
from app.logger import logger

EXTREME_PATTERNS = [
    re.compile(r"\brm\s+-rf\s+/\s*(?:\s|$)"),
    re.compile(r"^\s*mkfs\b"),
    re.compile(r"^\s*dd\s+if="),
    re.compile(r":\(\)\s*\{"),
    re.compile(r"^\s*mv\s+/\s+/dev/null"),
]

SHELL_METACHARS = re.compile(r"[;&|`$(){}<>]")

MAX_FILENAME_LENGTH = 255

WORKSPACE_DIR = os.path.abspath(os.path.join(os.getcwd(), "workspace"))


class Sanitizer:

    @staticmethod
    def sanitize_command(cmd: str) -> str:
        for pattern in EXTREME_PATTERNS:
            if pattern.search(cmd.strip()):
                logger.warning(f"Extremely dangerous command blocked: {cmd[:100]}")
                raise SecurityError(f"Command blocked: matches dangerous pattern '{pattern.pattern}'")

        sanitized = cmd
        dangerous_patterns = [
            (re.compile(r"\brm\s+-rf\s+/\s*(?:\s|$)"), "[BLOCKED: rm -rf /]"),
            (re.compile(r"\bmkfs\b"), "[BLOCKED: mkfs]"),
            (re.compile(r"\bdd\s+if="), "[BLOCKED: dd if=]"),
            (re.compile(r":\(\)\s*\{"), "[BLOCKED: fork bomb]"),
            (re.compile(r"\bmv\s+/\s+/dev/null"), "[BLOCKED: mv / /dev/null]"),
        ]
        for pattern, replacement in dangerous_patterns:
            if pattern.search(sanitized):
                logger.warning(f"Dangerous command pattern detected and sanitized: {pattern.pattern}")
                sanitized = pattern.sub(replacement, sanitized)

        return sanitized

    @staticmethod
    def sanitize_path(path: str) -> str:
        normalized = path.replace("\\", "/")

        parts = []
        for part in normalized.split("/"):
            if part == "..":
                logger.warning(f"Path traversal attempt blocked in path: {path}")
                continue
            parts.append(part)
        cleaned = "/".join(parts)

        resolved = os.path.normpath(os.path.join(WORKSPACE_DIR, cleaned.lstrip("/")))

        if not resolved.startswith(os.path.normpath(WORKSPACE_DIR)):
            logger.warning(f"Path escape attempt blocked: {path} resolved to {resolved}")
            resolved = WORKSPACE_DIR

        return resolved

    @staticmethod
    def sanitize_shell_args(args: list) -> list:
        cleaned = []
        for arg in args:
            sanitized = SHELL_METACHARS.sub("", arg)
            if sanitized != arg:
                logger.warning(f"Shell metacharacters stripped from argument: '{arg}' -> '{sanitized}'")
            cleaned.append(sanitized)
        return cleaned

    @staticmethod
    def sanitize_filename(name: str) -> str:
        sanitized = name.replace("/", "_").replace("\\", "_")
        sanitized = sanitized.replace("\0", "")

        if sanitized != name:
            logger.warning(f"Filename sanitized: '{name}' -> '{sanitized}'")

        if len(sanitized) > MAX_FILENAME_LENGTH:
            logger.warning(f"Filename truncated from {len(sanitized)} to {MAX_FILENAME_LENGTH} characters")
            sanitized = sanitized[:MAX_FILENAME_LENGTH]

        return sanitized
