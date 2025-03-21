import logging
from typing import Optional, Dict, Any
from crewai import Agent, Task, Crew, LLM
import os
import json
from tools.FluxImageGeneratorTool import FluxImageGeneratorTool, ImageFormat
from dotenv import load_dotenv

load_dotenv()


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class Mininos:
    def __init__(self, topic: Optional[str] = None, config_path: str = 'config'):
        self.topic = topic
        self.config_path = config_path
        self.agents_config = {}
        self.tasks_config = {}
        self.llm = None
        self.image_generator_tool = FluxImageGeneratorTool()
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
        """Initializes the language model."""
        model = os.getenv('MODEL')
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not model or not api_key:
            logger.error("Model and/or API key not found in .env file")
            raise ValueError("Model and API key must be set in the .env file")

        from crewai.llm import Gemini
        return Gemini(model=model, api_key=api_key)

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
        
        if agent_type == 'image_generator':
            return Agent(
                llm=self._initialize_llm(),
                tools=[self.image_generator_tool],
                **formatted_config
            )
        
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
        """Saves the content to a markdown file."""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)
            logger.info(f"Markdown file saved: {filename}")
        except Exception as e:
            logger.error(f"Error saving markdown file {filename}: {e}")
            raise

    def _process_formatter_output(self, output: str) -> Dict[str, str]:
      """Process formatter output string to a dict"""
      try:
          return json.loads(output)
      except json.JSONDecodeError as e:
          logger.error(f"Error decoding JSON output: {e}, output: {output}")
          return {}

    def _save_json(self, filename: str, data: dict) -> None:
        """Saves the data to a JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            logger.info(f"JSON file saved: {filename}")
        except Exception as e:
            logger.error(f"Error saving JSON file {filename}: {e}")
            raise

    def crew(self) -> Crew:
        """Creates and configures the crew with tasks and agents"""
        
        # Create agents
        writer_agent = self.create_agent('writer')
        reviewer_agent = self.create_agent('reviewer')
        formatter_agent = self.create_agent('formatter')
        image_generator_agent = self.create_agent('image_generator')

        # Create tasks
        write_task = self.create_task('write_draft', writer_agent)
        review_task = self.create_task('review_draft', reviewer_agent)
        format_task = self.create_task('format_post', formatter_agent)
        generate_images_task = self.create_task('generate_images', image_generator_agent)
        
        # Create the crew
        crew = Crew(
            agents=[writer_agent, reviewer_agent, formatter_agent, image_generator_agent],
            tasks=[write_task, review_task, format_task, generate_images_task],
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
            
            if generate_images_task.output:
                logger.info(f"Generated Images: {generate_images_task.output}")
                
            return crew
            
        except Exception as e:
            logger.error(f"Error during crew execution: {e}")
            raise