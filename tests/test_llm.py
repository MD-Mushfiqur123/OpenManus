import pytest
from app.schema import Message, ToolCall, Function


class TestLLMMessageFormatting:
    def test_message_creation(self):
        msg = Message.user_message("test")
        assert msg.role == "user"
        assert msg.content == "test"

    def test_message_to_dict(self):
        msg = Message.system_message("system test")
        d = msg.to_dict()
        assert d["role"] == "system"
        assert d["content"] == "system test"

    def test_tool_call_format(self):
        func = Function(name="bash", arguments='{"cmd": "ls"}')
        tc = ToolCall(id="call_1", type="function", function=func)
        msg = Message.from_tool_calls(tool_calls=[tc], content="using tools")
        assert msg.role == "assistant"
        assert msg.tool_calls is not None
        assert len(msg.tool_calls) == 1

    def test_message_list_concat(self):
        msg1 = Message.user_message("a")
        msg2 = Message.user_message("b")
        result = msg1 + [msg2]
        assert len(result) == 2

    def test_memory_max_messages(self):
        from app.schema import Memory
        mem = Memory(max_messages=3)
        for i in range(10):
            mem.add_message(Message.user_message(f"msg{i}"))
        assert len(mem.messages) == 3

    def test_tool_message_with_name(self):
        msg = Message.tool_message(content="output", name="bash", tool_call_id="call_1")
        assert msg.role == "tool"
        assert msg.name == "bash"
        assert msg.tool_call_id == "call_1"
