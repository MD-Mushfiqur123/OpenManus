from unittest.mock import MagicMock
from typing import Dict, Optional
from app.config import LLMSettings, AppConfig


def create_mock_config():
    """Create a mock config for testing"""
    config = MagicMock()

    config.llm = {
        "default": LLMSettings(
            model="gpt-4o",
            base_url="https://api.openai.com/v1",
            api_key="sk-mock-key",
            max_tokens=4096,
            temperature=0.0,
            api_type="openai",
            api_version="",
        )
    }

    config.browser_config = None
    config.search_config = None
    config.mcp_config = None
    config.run_flow_config = None
    config.daytona = MagicMock()
    config.daytona.daytona_api_key = ""
    config.daytona.VNC_password = "test123"
    config.sandbox = MagicMock()
    config.sandbox.use_sandbox = False
    config.workspace_root = MagicMock()
    config.root_path = MagicMock()

    return config


def patch_config(monkeypatch, mock_config=None):
    """Patch the global config with a mock"""
    if mock_config is None:
        mock_config = create_mock_config()
    import app.config as config_module
    monkeypatch.setattr(config_module, "config", mock_config)
    return mock_config
