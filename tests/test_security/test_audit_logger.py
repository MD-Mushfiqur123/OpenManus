import pytest
from app.tool.security.audit_logger import AuditLogger


class TestAuditLogger:
    def setup_method(self):
        self.audit = AuditLogger()

    def test_log_execution(self):
        self.audit.log_execution("bash", {"cmd": "ls"}, "success", 0.5)

    def test_log_llm_call(self):
        self.audit.log_llm_call("gpt-4o", 150, 2.5, 100, 50)

    def test_log_security_event(self):
        self.audit.log_security_event("validation_failure", "test event", "WARNING")

    def test_log_execution_with_error(self):
        self.audit.log_execution("bash", {"cmd": "ls"}, "ERROR: failed", 0.1)
