import pytest
from app.schema import (
    Role, ToolChoice, AgentState, Function, ToolCall,
    Message, Memory, ROLE_VALUES, TOOL_CHOICE_VALUES
)


class TestRole:
    def test_enum_values(self):
        assert Role.SYSTEM == "system"
        assert Role.USER == "user"
        assert Role.ASSISTANT == "assistant"
        assert Role.TOOL == "tool"

    def test_all_values_in_tuple(self):
        assert all(r.value in ROLE_VALUES for r in Role)


class TestToolChoice:
    def test_enum_values(self):
        assert ToolChoice.NONE == "none"
        assert ToolChoice.AUTO == "auto"
        assert ToolChoice.REQUIRED == "required"


class TestAgentState:
    def test_enum_values(self):
        assert AgentState.IDLE == "IDLE"
        assert AgentState.RUNNING == "RUNNING"
        assert AgentState.FINISHED == "FINISHED"
        assert AgentState.ERROR == "ERROR"


class TestFunction:
    def test_create_function(self):
        func = Function(name="test", arguments='{"key": "value"}')
        assert func.name == "test"
        assert func.arguments == '{"key": "value"}'


class TestToolCall:
    def test_create_tool_call(self):
        func = Function(name="bash", arguments='{"cmd": "ls"}')
        tc = ToolCall(id="call_123", type="function", function=func)
        assert tc.id == "call_123"
        assert tc.function.name == "bash"


class TestMessage:
    def test_user_message(self):
        msg = Message.user_message("Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"

    def test_system_message(self):
        msg = Message.system_message("System instruction")
        assert msg.role == "system"
        assert msg.content == "System instruction"

    def test_assistant_message(self):
        msg = Message.assistant_message("Assistant response")
        assert msg.role == "assistant"
        assert msg.content == "Assistant response"

    def test_tool_message(self):
        msg = Message.tool_message(content="Tool output", name="bash", tool_call_id="call_123")
        assert msg.role == "tool"
        assert msg.content == "Tool output"
        assert msg.name == "bash"

    def test_message_addition_with_list(self):
        msg1 = Message.user_message("Hello")
        result = msg1 + [Message.user_message("World")]
        assert len(result) == 2

    def test_message_raddition(self):
        msg = Message.user_message("World")
        result = [Message.user_message("Hello")] + msg
        assert len(result) == 2

    def test_to_dict(self):
        msg = Message.user_message("Hello")
        d = msg.to_dict()
        assert d["role"] == "user"
        assert d["content"] == "Hello"


class TestMemory:
    def test_add_message(self):
        mem = Memory()
        msg = Message.user_message("Hello")
        mem.add_message(msg)
        assert len(mem.messages) == 1

    def test_add_messages(self):
        mem = Memory()
        msgs = [Message.user_message("Hello"), Message.assistant_message("Hi")]
        mem.add_messages(msgs)
        assert len(mem.messages) == 2

    def test_max_messages(self):
        mem = Memory(max_messages=2)
        for i in range(5):
            mem.add_message(Message.user_message(f"msg{i}"))
        assert len(mem.messages) == 2
        assert mem.messages[-1].content == "msg4"

    def test_clear(self):
        mem = Memory()
        mem.add_message(Message.user_message("Hello"))
        mem.clear()
        assert len(mem.messages) == 0

    def test_get_recent(self):
        mem = Memory()
        for i in range(10):
            mem.add_message(Message.user_message(f"msg{i}"))
        recent = mem.get_recent_messages(3)
        assert len(recent) == 3
        assert recent[-1].content == "msg9"
