from app.flow.base import BaseFlow


class ParallelFlow(BaseFlow):
    """Executes multiple agents in parallel and collects all results"""

    name: str = "parallel"
    description: str = "Run multiple agents simultaneously"

    async def execute(self, input_text: str) -> str:
        import asyncio
        from app.logger import logger

        if not self.agents:
            return "Error: No agents configured for parallel execution"

        logger.info(f"🚀 ParallelFlow executing {len(self.agents)} agents")
        tasks = {}
        for key, agent in self.agents.items():
            logger.info(f"  Spawning agent '{key}' ({agent.name})")
            tasks[key] = asyncio.create_task(self._run_agent(key, agent, input_text))

        results = {}
        for key, task in tasks.items():
            try:
                result = await task
                results[key] = result
            except Exception as e:
                logger.error(f"Agent '{key}' failed: {e}")
                results[key] = f"Error: {e}"

        return self._format_results(results)

    async def _run_agent(self, key: str, agent, input_text: str) -> str:
        from app.logger import logger

        logger.info(f"Agent '{key}' starting execution")
        result = await agent.run(input_text)
        logger.info(f"Agent '{key}' completed")
        return result

    def _format_results(self, results: dict) -> str:
        parts = ["# Parallel Execution Results", ""]
        for key, result in results.items():
            parts.append(f"## Agent: {key}")
            parts.append(result)
            parts.append("")
        return "\n".join(parts)
