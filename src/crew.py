import json
import os
from typing import Dict, Optional, Any, List
import logging
from pathlib import Path
import re

from crewai import Agent, Task, Crew
from crewai.llm import LLM
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class Mininos:
    def __init__(self, topic: Optional[str] = None, config_path: str = 'config'):
        self.topic = topic
        self.config_path = config_path
        self.agents_config = {}
        self.tasks_config = {}
        self.llm = None
        self._load_configurations()

    def _load_configurations(self) -> None:
        """Load agent and task configurations from YAML files."""
        self.agents_config = self._load_yaml(f'{self.config_path}/agents.yaml')
        self.tasks_config = self._load_yaml(f'{self.config_path}/tasks.yaml')
        logger.info("Configurations loaded.")

    def _load_yaml(self, filename: str) -> dict:
        """Loads a YAML file and returns its contents."""
        try:
            import yaml
            with open(filename, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.error(f"File not found: {filename}")
            return {}
        except yaml.YAMLError as e:
            logger.error(f"Error loading YAML file {filename}: {e}")
            return {}

    def _initialize_llm(self) -> LLM:
        """Initialize the LLM model with environment variables"""
        model_name = os.getenv("MODEL")
        api_key = os.getenv("GOOGLE_API_KEY")
        
        logging.info(f"Model name: {model_name}")
        logging.info(f"API key present: {bool(api_key)}")  # Don't log the actual key
        
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
            
        logging.info(f"Initializing LLM with model: {model_name}")

        llm = LLM(
            model=model_name,
            api_key=api_key,
            provider="gemini",
            temperature=0.7,
            timeout=120,
            max_tokens=4000,
            top_p=0.9,
            frequency_penalty=0.1,
            presence_penalty=0.1,
            response_format={"type": "json"},
            seed=42
        )

        return llm

    def _format_config(self, config: Dict[str, Any], agent_type: str) -> Dict[str, Any]:
         """Format configurations for agents."""
         
         if config.get('backstory'):
                config['backstory'] = config['backstory'].format(topic=self.topic)
         if config.get('goal'):
            config['goal'] = config['goal'].format(topic=self.topic)
        
         return config

    def create_agent(self, agent_type: str) -> Agent:
        """Creates an agent based on the provided agent type."""
        agent_config = self.agents_config.get(agent_type, {})
        formatted_config = self._format_config(agent_config, agent_type)
        return Agent(
            llm=self._initialize_llm(),
            **formatted_config
        )

    def create_task(self, task_type: str, agent: Agent) -> Task:
        """Creates a task for the specified agent."""
        task_config = self.tasks_config.get(task_type, {})
        
        task_description = task_config.get('description', '').format(topic=self.topic)
        
        return Task(
            description=task_description,
            agent=agent,
            expected_output=task_config.get('expected_output')
        )
    
    def _save_markdown(self, filename: str, content: str) -> None:
         """Saves content to a Markdown file."""
         Path("output").mkdir(exist_ok=True)
         filepath = Path("output") / filename
         try:
             with open(filepath, 'w', encoding='utf-8') as file:
                 file.write(content)
             logger.info(f"File saved: {filepath}")
         except Exception as e:
             logger.error(f"Error saving file {filepath}: {e}")

    def _process_formatter_output(self, output: str) -> Dict[str, str]:
        """Process and validate formatter output"""
        try:
            # Limpiar el output de caracteres especiales
            cleaned_output = output.replace('\\n', '\n').strip()
            if cleaned_output.startswith('```json'):
                cleaned_output = cleaned_output[7:]
            if cleaned_output.endswith('```'):
                cleaned_output = cleaned_output[:-3]
            # Limpiar caracteres especiales adicionales y espacios en blanco
            cleaned_output = re.sub(r'[\u200b-\u200f\ufeff]', '', cleaned_output)  # Eliminar caracteres de ancho cero
            cleaned_output = re.sub(r'\s+', ' ', cleaned_output).strip() # Eliminar espacios en blanco duplicados

            return json.loads(cleaned_output)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from formatter output: {e}")
            return {"error": "Invalid JSON format", "raw_output": output}


    def _save_json(self, filename: str, data: dict) -> None:
        """Saves data to a JSON file."""
        Path("output").mkdir(exist_ok=True)
        filepath = Path("output") / filename
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            logger.info(f"JSON file saved: {filepath}")
        except Exception as e:
            logger.error(f"Error saving JSON file {filepath}: {e}")

    def crew(self) -> Crew:
        """Creates and configures the crew with tasks and agents"""
        
        # Create agents
        writer_agent = self.create_agent('writer')
        reviewer_agent = self.create_agent('reviewer')
        formatter_agent = self.create_agent('formatter')

        # Create tasks
        write_task = self.create_task('write_draft', writer_agent)
        review_task = self.create_task('review_draft', reviewer_agent)
        format_task = self.create_task('format_post', formatter_agent)
        
        # Create the crew
        crew = Crew(
            agents=[writer_agent, reviewer_agent, formatter_agent],
            tasks=[write_task, review_task, format_task],
            verbose=True
        )
        
        try:
            # Kickoff and save results
            result = crew.kickoff()
            
            # Guardar los resultados de cada tarea
            if write_task.output:
                self._save_markdown("blog_draft.md", str(write_task.output))
            
            if review_task.output:
                self._save_markdown("blog_reviewed.md", str(review_task.output))
            
            if format_task.output:
                formatter_output = self._process_formatter_output(str(format_task.output))
                self._save_json("formatted_post.json", formatter_output)
            
            return crew
            
        except Exception as e:
            logger.error(f"Error during crew execution: {e}")
            raise