import os
import logging
import asyncio
from typing import Dict, Any, Optional, Callable

# Use standard import now that pyproject.toml is configured
from src.crew import Mininos

class MewAIService:
    def __init__(self,
                 generation_id: str = None,
                 progress_callback: Callable[[str, Dict], None] = None):
        self.setup_logging()
        self.generation_id = generation_id
        self.progress_callback = progress_callback

    def setup_logging(self):
        # Basic logging setup, consider more robust configuration for production
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
        self.logger = logging.getLogger("MewAIService")
        self.logger.info("MewAIService initialized.")

    async def generate_content(self, topic: str, settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generates content using MewAI agents by running the crew in a separate thread.

        Args:
            topic: The topic for content generation.
            settings: Additional settings (currently unused but available).

        Returns:
            A dictionary containing the generated content or an error message.
        """
        self.logger.info(f"[{self.generation_id}] Starting content generation for topic: {topic}")

        try:
            # Create Mininos instance, passing callbacks
            mininos = Mininos(
                topic=topic,
                generation_id=self.generation_id,
                progress_callback=self.progress_callback
            )

            # Get the current asyncio event loop
            loop = asyncio.get_running_loop()

            # Run the blocking 'run_crew_and_get_results' method in the default thread pool executor
            # 'None' uses the default ThreadPoolExecutor
            self.logger.info(f"[{self.generation_id}] Scheduling crew execution in background thread...")
            results = await loop.run_in_executor(
                None,  # Executor (None for default)
                mininos.run_crew_and_get_results # The synchronous function to run
            )
            self.logger.info(f"[{self.generation_id}] Background thread execution completed.")

            return results

        except Exception as e:
            self.logger.error(f"[{self.generation_id}] Error during service-level generation: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Service error: {str(e)}"
            }