import sys
import types
from pathlib import Path
from unittest.mock import MagicMock

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _create_mock_package(name):
    """Create a mock package in sys.modules"""
    parts = name.split(".")
    for i in range(1, len(parts) + 1):
        partial = ".".join(parts[:i])
        if partial not in sys.modules:
            mod = types.ModuleType(partial)
            mod.__path__ = []
            mod.__package__ = partial
            mod.__file__ = f"<mock-{partial}>"
            sys.modules[partial] = mod


def _mock_module_with_attrs(name, attrs):
    """Create a mock module with specified attributes"""
    _create_mock_package(name)
    mod = sys.modules[name]
    for attr_name in attrs:
        setattr(mod, attr_name, MagicMock())


_mock_specs = {
    "browser_use": ["Browser", "BrowserConfig"],
    "browser_use.browser.context": ["BrowserContext", "BrowserContextConfig"],
    "browser_use.dom.service": ["DomService"],
    "baidusearch.baidusearch": ["search"],
    "googlesearch": ["search"],
    "duckduckgo_search": ["DDGS"],
    "docker": ["APIClient"],
    "docker.errors": ["NotFound", "APIError", "ImageNotFound"],
    "docker.models.containers": ["Container"],
    "daytona": ["Daytona", "DaytonaConfig", "Sandbox", "SandboxState",
                 "CreateSandboxFromImageParams", "Resources", "SessionExecuteRequest"],
}

for mod_name, names in _mock_specs.items():
    _mock_module_with_attrs(mod_name, names)

_mock_packages = [
    "browser_use.dom", "browser_use.controller", "browser_use.agent",
    "crawl4ai", "playwright", "playwright.async_api",
    "gymnasium", "browsergym",
    "baidusearch",
]

for mod_name in _mock_packages:
    if mod_name not in sys.modules:
        _create_mock_package(mod_name)


@pytest.fixture
def mock_config(monkeypatch):
    """Fixture providing a mock config for testing"""
    from tests.mocks.mock_config import create_mock_config, patch_config
    mock = create_mock_config()
    patch_config(monkeypatch, mock)
    return mock


@pytest.fixture
def mock_llm():
    """Fixture providing a mock LLM"""
    from tests.mocks.mock_llm import MockLLM
    return MockLLM()
