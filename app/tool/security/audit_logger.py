from datetime import datetime, timezone

from app.logger import logger


class AuditLogger:

    def log_execution(
        self,
        tool_name: str,
        params: dict,
        result: str,
        duration: float,
        user: str = "system",
    ):
        param_summary = str(params)[:100] if params else "{}"
        result_summary = str(result)[:100] if result else ""
        logger.info(
            f"AUDIT | tool={tool_name} | duration={duration:.2f}s "
            f"| params={param_summary} | result={result_summary}"
        )

    def log_llm_call(
        self,
        model: str,
        tokens: int,
        duration: float,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
    ):
        logger.info(
            f"AUDIT | llm_call | model={model} | tokens={tokens} "
            f"| duration={duration:.2f}s "
            f"| prompt_tokens={prompt_tokens} | completion_tokens={completion_tokens}"
        )

    def log_security_event(
        self,
        event_type: str,
        details: str,
        severity: str = "WARNING",
    ):
        logger.log(
            "WARNING" if severity == "WARNING" else severity,
            f"AUDIT | security | {severity} | {event_type} | {details}",
        )
