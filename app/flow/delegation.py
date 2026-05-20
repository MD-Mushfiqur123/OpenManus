from app.flow.base import BaseFlow


class DelegationFlow(BaseFlow):
    """Primary agent delegates sub-tasks to specialized agents"""

    name: str = "delegation"
    description: str = "Delegate tasks to specialized agents"
    max_delegations: int = 5

    async def execute(self, input_text: str) -> str:
        from app.logger import logger

        primary = self.primary_agent
        if not primary:
            return "Error: No primary agent configured"

        logger.info(f"🚀 DelegationFlow starting with primary agent: {primary.name}")
        logger.info(f"  Available delegates: {list(self.agents.keys())}")

        result = await primary.run(input_text)
        return f"# Delegation Flow Result\n\n{result}"

    async def delegate_to(self, agent_key: str, task: str) -> str:
        """Delegate a sub-task to a specialized agent"""
        from app.logger import logger

        agent = self.get_agent(agent_key)
        if not agent:
            logger.error(f"Delegate agent '{agent_key}' not found")
            return f"Error: Agent '{agent_key}' not available"

        logger.info(f"Delegating task to '{agent_key}': {task[:100]}...")
        try:
            result = await agent.run(task)
            logger.info(f"Delegation to '{agent_key}' completed")
            return result
        except Exception as e:
            logger.error(f"Delegation to '{agent_key}' failed: {e}")
            return f"Error: Delegation to '{agent_key}' failed: {e}"
