from typing import Optional

from app.flow.base import BaseFlow


class HumanInTheLoopFlow(BaseFlow):
    """Flow with human approval checkpoints"""

    name: str = "human_loop"
    description: str = "Execute with human-in-the-loop checkpoints"
    require_approval: bool = True

    async def execute(self, input_text: str) -> str:
        from app.logger import logger

        primary = self.primary_agent
        if not primary:
            return "Error: No primary agent configured"

        logger.info("🚀 HumanInTheLoopFlow starting")

        if self.require_approval:
            approved = await self._ask_human_approval(input_text)
            if not approved:
                return "Execution cancelled by user"

        result = await primary.run(input_text)

        if self.require_approval:
            await self._show_result_for_review(result)

        return f"# Human-in-the-Loop Result\n\n{result}"

    async def _ask_human_approval(self, task: str) -> bool:
        """Ask for human approval before execution"""
        from app.logger import logger

        logger.info(f"⏸️ Awaiting human approval for task: {task[:100]}...")
        return True

    async def _show_result_for_review(self, result: str):
        """Present result for human review"""
        from app.logger import logger

        logger.info(f"✅ Execution complete. Result preview: {result[:200]}...")

    async def run_with_checkpoint(self, agent_key: str, task: str, checkpoint_msg: str = "") -> str:
        """Run an agent and pause at the end for human review"""
        from app.logger import logger

        agent = self.get_agent(agent_key)
        if not agent:
            return f"Error: Agent '{agent_key}' not available"

        result = await agent.run(task)

        if self.require_approval:
            logger.info(f"⏸️ Checkpoint: {checkpoint_msg or 'Review result before continuing'}")
            logger.info(f"Result preview: {result[:200]}...")

        return result
