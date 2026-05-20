class OpenManusError(Exception):
    """Base exception for all OpenManus errors"""


class ToolError(OpenManusError):
    """Raised when a tool encounters an error."""

    def __init__(self, message):
        self.message = message


class LLMProviderError(OpenManusError):
    """Exception raised when an LLM provider encounters an error"""


class TokenLimitExceeded(LLMProviderError):
    """Exception raised when the token limit is exceeded"""


class ConfigError(OpenManusError):
    """Exception raised for configuration-related errors"""


class AgentError(OpenManusError):
    """Exception raised for agent-related errors"""


class AgentStuckError(AgentError):
    """Exception raised when the agent is stuck in a loop"""


class FlowError(OpenManusError):
    """Exception raised for flow-related errors"""


class MCPConnectionError(OpenManusError):
    """Exception raised for MCP connection errors"""


class SecurityError(OpenManusError):
    """Exception raised for security violations"""


class ValidationError(SecurityError):
    """Exception raised for validation errors"""


class RateLimitError(SecurityError):
    """Exception raised when a rate limit is exceeded"""
