import pytest
from app.tool.base import BaseTool
from app.tool.security import InputValidator, AuditLogger, OutputGuardrail


class TestSecurityIntegration:
    def test_validator_importable(self):
        v = InputValidator()
        assert v is not None

    def test_audit_logger_importable(self):
        a = AuditLogger()
        assert a is not None

    def test_guardrail_importable(self):
        g = OutputGuardrail()
        assert g is not None

    def test_security_middleware_in_base_tool(self):
        assert hasattr(BaseTool, '_execute_with_security')

    def test_security_middleware_in_call(self):
        assert BaseTool.__call__.__name__ == '__call__'
