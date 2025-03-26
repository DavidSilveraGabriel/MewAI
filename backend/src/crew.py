import logging
import os
import json
import yaml # Make sure PyYAML is installed
import asyncio
import pathlib
from typing import Optional, Dict, Any, Callable


# --- Importación de LLM directamente desde crewai ---
from crewai import Agent, Task, Crew, LLM
# Ya no necesitamos importar desde langchain_google_genaie

# Import the tool using the new package structure
from src.tools.FluxImageGeneratorTool import FluxImageGeneratorTool

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define project root relative to this file (backend/src/crew.py)
PROJECT_ROOT = pathlib.Path(__file__).parent.parent
CONFIG_DIR = PROJECT_ROOT / "src" / "config"
OUTPUT_DIR = PROJECT_ROOT / "output" # Define a consistent output directory if saving files

class Mininos:
    def __init__(self,
                 topic: Optional[str] = None,
                 config_path: str = str(CONFIG_DIR),
                 generation_id: str = None,
                 progress_callback: Callable[[str, Dict], None] = None):
        self.topic = topic
        self.config_path = pathlib.Path(config_path)
        self.generation_id = generation_id
        self.progress_callback = progress_callback
        self.agents_config = {}
        self.tasks_config = {}
        # --- LLM se inicializa aquí ---
        self.llm = self._initialize_llm()
        self.image_generator_tool = FluxImageGeneratorTool(save_dir=str(OUTPUT_DIR / "images"))
        self._load_configurations()
        self.total_tasks = 0


    def _load_configurations(self) -> None:
        """Load agent and task configurations from YAML files."""
        agents_file = self.config_path / 'agents.yaml'
        tasks_file = self.config_path / 'tasks.yaml'
        self.agents_config = self._load_yaml(agents_file)
        self.tasks_config = self._load_yaml(tasks_file)
        self.total_tasks = len(self.tasks_config) # Get total number of tasks for progress
        logger.info(f"Configurations loaded from {self.config_path}")

    def _load_yaml(self, filename: pathlib.Path) -> dict:
        """Loads a YAML file and returns its contents."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {filename}")
            return {}
        except yaml.YAMLError as e:
            logger.error(f"Error loading YAML file {filename}: {e}")
            return {}
        except Exception as e:
             logger.error(f"Unexpected error loading {filename}: {e}")
             return {}

    # --- Método _initialize_llm ACTUALIZADO ---
    def _initialize_llm(self) -> LLM: # Cambiar tipo de retorno a crewai.LLM
        """Initializes the language model using crewai.LLM wrapper."""
        model_name = os.getenv('MODEL')
        api_key = os.getenv('GEMINI_API_KEY')
        # Opcional: Leer temperatura desde .env o usar un default
        try:
            temperature = float(os.getenv('LLM_TEMPERATURE', 0.6))
        except ValueError:
            logger.warning("Invalid LLM_TEMPERATURE in .env, using default 0.6")
            temperature = 0.6

        if not model_name or not api_key:
            logger.error("MODEL and/or GEMINI_API_KEY not found in .env file")
            raise ValueError("MODEL and GEMINI_API_KEY must be set in the .env file")

        # Asegurarse de que el nombre del modelo tenga el prefijo 'gemini/' para LiteLLM
        if not model_name.startswith("gemini/"):
            llm_model_name = f"gemini/{model_name}"
            logger.warning(f"MODEL env var '{model_name}' is missing the 'gemini/' prefix. Using '{llm_model_name}' for LiteLLM.")
        else:
            llm_model_name = model_name

        logger.info(f"Initializing crewai.LLM wrapper for model: {llm_model_name} with temperature: {temperature}")
        try:
            # --- Usar crewai.LLM ---
            llm = LLM(
                model=llm_model_name, # Pasar el nombre del modelo como espera LiteLLM
                api_key=api_key,
                temperature=temperature
                # Puedes añadir más parámetros aquí si son soportados por LiteLLM para Gemini
                # Por ejemplo: config={'max_tokens': 4096}
            )
            # Opcional: Probar una llamada simple si es posible/necesario
            # llm.invoke("Test prompt")
            logger.info("crewai.LLM initialized successfully.")
            return llm
        except Exception as e:
             logger.error(f"Failed to initialize crewai.LLM: {e}", exc_info=True)
             # Podrías intentar capturar errores específicos de LiteLLM si ocurren
             raise

    def _format_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
         """Format configurations using the topic."""
         formatted = {}
         for key, value in config.items():
             if isinstance(value, str):
                 try:
                     formatted[key] = value.format(topic=self.topic)
                 except KeyError: # Handle cases where topic might not be needed
                     formatted[key] = value
             else:
                 formatted[key] = value
         return formatted

    def create_agent(self, agent_type: str) -> Agent:
        """Creates an agent based on the provided agent type."""
        agent_config = self.agents_config.get(agent_type, {})
        if not agent_config:
             raise ValueError(f"Agent configuration for '{agent_type}' not found.")

        formatted_config = self._format_config(agent_config)
        logger.debug(f"Creating agent '{agent_type}' with config: {formatted_config}")

        tools = []
        if agent_type == 'image_generator':
            tools = [self.image_generator_tool]

        # --- Pasar el LLM ya inicializado al Agente ---
        return Agent(
            llm=self.llm, # Usar el LLM de la instancia de Mininos
            tools=tools,
            **formatted_config
        )

    def create_task(self, task_type: str, agent: Agent, context_tasks: list = None) -> Task:
        """Creates a task for the specified agent."""
        task_config = self.tasks_config.get(task_type, {})
        if not task_config:
            raise ValueError(f"Task configuration for '{task_type}' not found.")

        formatted_config = self._format_config(task_config)
        logger.debug(f"Creating task '{task_type}' with config: {formatted_config}")

        # Add context if provided (for task dependencies)
        context = context_tasks if context_tasks else []

        return Task(
            description=formatted_config.get('description', ''),
            agent=agent,
            expected_output=formatted_config.get('expected_output', ''),
            context=context
        )

    def _step_callback(self, agent_output):
        """Callback triggered after each agent step."""
        # This callback receives an AgentFinish object which might not be ideal for progress.
        # We'll rely more on the task callback for overall progress.
        if self.progress_callback and self.generation_id:
            # agent_name = agent_output.agent_name # Check exact attribute name in CrewAI docs
            message = f"Agent step completed. Output: {str(agent_output)[:100]}..."
            progress_info = { "message": message }
            try:
                loop = asyncio.get_running_loop()
                loop.call_soon_threadsafe(self.progress_callback, self.generation_id, progress_info)
            except RuntimeError: # If no loop is running (e.g., direct script execution)
                 logger.warning("No running asyncio loop found for step callback.")
            except Exception as e:
                 logger.error(f"Error in step callback: {e}")


    def _task_callback(self, task_output):
         """Callback triggered after each task is completed."""
         if self.progress_callback and self.generation_id:
             task_index = -1
             try:
                 # Try to find the index of the completed task to estimate progress
                 task_description_prefix = task_output.task.description[:30]
                 for i, task_key in enumerate(self.tasks_config.keys()):
                     if self.tasks_config[task_key].get('description', '').format(topic=self.topic).startswith(task_description_prefix):
                         task_index = i
                         break
             except Exception as e:
                 logger.warning(f"Could not determine task index for progress: {e}")

             progress_percentage = 10 # Default start
             if task_index != -1 and self.total_tasks > 0:
                 # Calculate progress: add 1 because index is 0-based, ensure small progress even for first task
                 progress_percentage = max(10, int(((task_index + 1) / self.total_tasks) * 95)) # Leave last 5% for final wrap-up

             message = f"Task '{task_output.description[:50]}...' completed."
             progress_info = {
                 "message": message,
                 "progress": progress_percentage,
                 "task_result_summary": str(task_output.raw_output)[:200] # Example summary
             }
             try:
                 loop = asyncio.get_running_loop()
                 # Use call_soon_threadsafe to schedule the callback on the main event loop
                 loop.call_soon_threadsafe(self.progress_callback, self.generation_id, progress_info)
                 logger.info(f"Sent progress update via callback: {progress_info}")
             except RuntimeError:
                 logger.warning("No running asyncio loop found for task callback.")
             except Exception as e:
                 logger.error(f"Error in task callback: {e}")


    def configure_crew(self) -> Crew:
        """Creates and configures the crew with tasks and agents."""
        try:
            writer_agent = self.create_agent('writer')
            reviewer_agent = self.create_agent('reviewer')
            formatter_agent = self.create_agent('formatter')
            image_generator_agent = self.create_agent('image_generator')

            # Define tasks with dependencies (context)
            write_task = self.create_task('write_draft', writer_agent)
            # Review task depends on the write task
            review_task = self.create_task('review_draft', reviewer_agent, context_tasks=[write_task])
             # Format task depends on the review task
            format_task = self.create_task('format_post', formatter_agent, context_tasks=[review_task])
            # Image generation depends on the reviewed content (review_task)
            generate_images_task = self.create_task('generate_images', image_generator_agent, context_tasks=[review_task])

            # Order tasks correctly for execution flow
            self.tasks = [write_task, review_task, format_task, generate_images_task]

            crew = Crew(
                agents=[writer_agent, reviewer_agent, formatter_agent, image_generator_agent],
                tasks=self.tasks,
                verbose=2, # Use level 2 for detailed logs
                # step_callback=self._step_callback, # step_callback can be very verbose
                task_callback=self._task_callback # Use task_callback for progress milestones
            )
            return crew
        except Exception as e:
            logger.error(f"Error configuring crew: {e}", exc_info=True)
            raise

    def _process_formatter_output(self, output: str) -> Dict[str, str]:
        """Process formatter output string (potentially JSON in markdown) to a dict."""
        logger.debug(f"Processing formatter output: {output[:500]}...") # Log snippet
        try:
             # Remove potential markdown code fences
             if output.startswith("```json"):
                 output = output.strip()[7:-3].strip()
             elif output.startswith("```"):
                 output = output.strip()[3:-3].strip()

             # Handle potential escape sequences if needed (e.g., \\n -> \n)
             # output = output.encode().decode('unicode_escape') # Use with caution

             # Replace invalid control characters if necessary (less common)
             # output = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', output)

             data = json.loads(output)
             if isinstance(data, dict):
                 return data
             else:
                 logger.warning(f"Formatter output parsed but is not a dictionary: {type(data)}")
                 return {"raw_output": str(data)} # Return as raw if not dict
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON output: {e}. Raw output: '{output[:500]}...'")
            # Attempt to find JSON within the string if decode fails directly
            try:
                match = json.search(r'\{.*\}', output, json.DOTALL)
                if match:
                    logger.info("Found JSON object within raw output, attempting parse again.")
                    return json.loads(match.group(0))
            except Exception as inner_e:
                 logger.error(f"Could not extract valid JSON after initial failure: {inner_e}")

            # Fallback: Return the raw string with an error key
            return {"error": "Failed to parse JSON", "raw_output": output}
        except Exception as e:
             logger.error(f"Unexpected error processing formatter output: {e}")
             return {"error": f"Unexpected error: {e}", "raw_output": output}

    # --- Methods for saving files (Optional, can be used for debugging/backup) ---
    def _save_output(self, filename: str, content: Any) -> None:
        """Saves content to a file in the OUTPUT_DIR."""
        try:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            filepath = OUTPUT_DIR / filename
            mode = 'w'
            encoding = 'utf-8'
            if isinstance(content, dict) or isinstance(content, list):
                 with open(filepath, mode, encoding=encoding) as f:
                     json.dump(content, f, indent=4, ensure_ascii=False)
            elif isinstance(content, str):
                 with open(filepath, mode, encoding=encoding) as f:
                     f.write(content)
            else:
                 # Try converting to string as a fallback
                 with open(filepath, mode, encoding=encoding) as f:
                      f.write(str(content))
            logger.info(f"Output saved to: {filepath}")
        except Exception as e:
            logger.error(f"Error saving output file {filename}: {e}")

    def run_crew_and_get_results(self) -> Dict[str, Any]:
        """
        Synchronous method to configure, run the crew, and collect results.
        Designed to be called within `run_in_executor`.
        """
        logger.info(f"[{self.generation_id}] Configuring and starting Crew execution...")
        try:
            crew = self.configure_crew()
            logger.info(f"[{self.generation_id}] Kicking off crew...")
            # This is the blocking call
            kickoff_result = crew.kickoff()
            logger.info(f"[{self.generation_id}] Crew kickoff completed.")

            # --- Collect results directly from task outputs ---
            results = {
                "status": "success",
                "kickoff_raw_result": str(kickoff_result) if kickoff_result else None, # Crew output if any
                "blog_draft": None,
                "blog_reviewed": None,
                "social_media": None,
                "images": None
            }

            # Safely access task outputs using the configured task order
            task_outputs = {task.description[:30]: task.output for task in crew.tasks if task.output}

            if crew.tasks and len(crew.tasks) > 0 and crew.tasks[0].output:
                 results["blog_draft"] = str(crew.tasks[0].output.raw_output) # Access raw_output
                 # self._save_output(f"{self.generation_id}_blog_draft.md", results["blog_draft"]) # Optional save

            if crew.tasks and len(crew.tasks) > 1 and crew.tasks[1].output:
                 results["blog_reviewed"] = str(crew.tasks[1].output.raw_output)
                 # self._save_output(f"{self.generation_id}_blog_reviewed.md", results["blog_reviewed"]) # Optional save

            if crew.tasks and len(crew.tasks) > 2 and crew.tasks[2].output:
                 formatter_output_str = str(crew.tasks[2].output.raw_output)
                 processed_social = self._process_formatter_output(formatter_output_str)
                 results["social_media"] = processed_social
                 # self._save_output(f"{self.generation_id}_social_media.json", results["social_media"]) # Optional save

            if crew.tasks and len(crew.tasks) > 3 and crew.tasks[3].output:
                 # The image tool returns a string; capture it. Consider modifying tool for list of paths.
                 results["images"] = str(crew.tasks[3].output.raw_output)
                 # No file saving here as tool already saves images

            logger.info(f"[{self.generation_id}] Results collected successfully.")
            return results

        except Exception as e:
            logger.error(f"[{self.generation_id}] Error during crew execution or result processing: {e}", exc_info=True)
            # Return error status and message
            return {
                "status": "error",
                "message": f"Crew execution failed: {str(e)}"
            }