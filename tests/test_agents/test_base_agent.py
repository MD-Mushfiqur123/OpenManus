import pytest
from app.schema import AgentState, Message
from tests.mocks.mock_llm import MockLLM


@pytest.fixture
def test_agent():
    from app.agent.base import BaseAgent

    class TestAgent(BaseAgent):
        name: str = "test_agent"

        async def step(self) -> str:
            return "test step"

    return TestAgent(llm=MockLLM())


class TestBaseAgent:
    def test_initial_state(self, test_agent):
        assert test_agent.state == AgentState.IDLE

    def test_initial_step(self, test_agent):
        assert test_agent.current_step == 0

    def test_update_memory(self, test_agent):
        test_agent.update_memory("user", "Hello")
        assert len(test_agent.memory.messages) == 1
        assert test_agent.memory.messages[0].role == "user"

    def test_update_memory_system(self, test_agent):
        test_agent.update_memory("system", "System instruction")
        assert test_agent.memory.messages[0].role == "system"

    def test_messages_property(self, test_agent):
        test_agent.update_memory("user", "Hello")
        assert len(test_agent.messages) == 1

    def test_messages_setter(self, test_agent):
        msgs = [Message.user_message("Hello")]
        test_agent.messages = msgs
        assert len(test_agent.messages) == 1

    @pytest.mark.asyncio
    async def test_state_context(self, test_agent):
        async with test_agent.state_context(AgentState.RUNNING):
            assert test_agent.state == AgentState.RUNNING
        assert test_agent.state == AgentState.IDLE

    @pytest.mark.asyncio
    async def test_state_context_error(self, test_agent):
        with pytest.raises(ValueError):
            async with test_agent.state_context("INVALID"):
                pass

    def test_duplicate_threshold_default(self, test_agent):
        assert test_agent.duplicate_threshold == 2

    def test_is_stuck_false_with_few_messages(self, test_agent):
        assert test_agent.is_stuck() is False

    def test_name(self, test_agent):
        assert test_agent.name == "test_agent"

    @pytest.mark.asyncio
    async def test_run_requires_idle(self, test_agent):
        test_agent.state = AgentState.RUNNING
        with pytest.raises(RuntimeError):
            await test_agent.run("test")
