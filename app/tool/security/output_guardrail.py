from __future__ import annotations

import re
from typing import Any

from app.exceptions import SecurityError
from app.logger import logger

BASE64_BLOB_THRESHOLD = 100 * 1024
MAX_BASE64_IMAGE_SIZE = 10 * 1024 * 1024

BASE64_PATTERN = re.compile(
    r"(?:[A-Za-z0-9+/]{4}){20,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?"
)

ANSI_NON_COLOR = re.compile(r"\x1b\[[0-9;]*[A-HJKSTfminsu]")


class OutputGuardrail:

    def filter_output(self, output: str, max_length: int = 100000) -> str:
        if not isinstance(output, str):
            return output

        filtered = ANSI_NON_COLOR.sub("", output)

        if len(filtered) > max_length:
            logger.warning(
                f"Output truncated from {len(filtered)} to {max_length} characters"
            )
            filtered = filtered[:max_length]

        matches = BASE64_PATTERN.findall(filtered)
        for match in matches:
            if len(match) > BASE64_BLOB_THRESHOLD:
                logger.warning(
                    f"Large base64-encoded blob detected in output ({len(match)} bytes)"
                )
                break

        return filtered

    def filter_tool_result(self, result: Any) -> Any:
        if hasattr(result, "output") and result.output is not None:
            result.output = self.filter_output(str(result.output))

        if (
            hasattr(result, "base64_image")
            and result.base64_image
            and isinstance(result.base64_image, str)
            and len(result.base64_image) > MAX_BASE64_IMAGE_SIZE
        ):
            logger.warning(
                f"Base64 image truncated from {len(result.base64_image)} to {MAX_BASE64_IMAGE_SIZE} bytes"
            )
            result.base64_image = result.base64_image[:MAX_BASE64_IMAGE_SIZE]

        return result

    def filter_message(self, message: Any) -> Any:
        if hasattr(message, "content") and message.content is not None:
            message.content = self.filter_output(str(message.content))

        if (
            hasattr(message, "base64_image")
            and message.base64_image
            and isinstance(message.base64_image, str)
            and len(message.base64_image) > MAX_BASE64_IMAGE_SIZE
        ):
            logger.warning(
                f"Message base64 image truncated from {len(message.base64_image)} to {MAX_BASE64_IMAGE_SIZE} bytes"
            )
            message.base64_image = message.base64_image[:MAX_BASE64_IMAGE_SIZE]

        return message
