import pytest
from app.exceptions import (
    OpenManusError, ToolError, ConfigError, LLMProviderError,
    TokenLimitExceeded, AgentError, AgentStuckError, FlowError,
    MCPConnectionError, SecurityError, ValidationError, RateLimitError
)


class TestExceptionHierarchy:
    def test_openmanus_error_base(self):
        assert issubclass(ToolError, OpenManusError)
        assert issubclass(ConfigError, OpenManusError)
        assert issubclass(LLMProviderError, OpenManusError)
        assert issubclass(AgentError, OpenManusError)
        assert issubclass(FlowError, OpenManusError)
        assert issubclass(MCPConnectionError, OpenManusError)
        assert issubclass(SecurityError, OpenManusError)

    def test_token_limit_inheritance(self):
        assert issubclass(TokenLimitExceeded, LLMProviderError)

    def test_agent_stuck_inheritance(self):
        assert issubclass(AgentStuckError, AgentError)

    def test_validation_inheritance(self):
        assert issubclass(ValidationError, SecurityError)

    def test_rate_limit_inheritance(self):
        assert issubclass(RateLimitError, SecurityError)

    def test_tool_error_message(self):
        err = ToolError("Something went wrong")
        assert str(err) == "Something went wrong"
        assert err.message == "Something went wrong"

    def test_security_error_raise(self):
        with pytest.raises(SecurityError):
            raise SecurityError("Unauthorized access")
