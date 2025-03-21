import logging
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from crew import Mininos

def setup_logging(log_file: Optional[str] = None) -> None:
    """Configure logging with optional file output"""
    config = {
        'level': logging.DEBUG,
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'handlers': [logging.StreamHandler()]
    }

    if log_file:
        Path('logs').mkdir(exist_ok=True)
        config['handlers'].append(logging.FileHandler(f'logs/{log_file}'))

    logging.basicConfig(**config)

def validate_environment() -> None:
    """Validate necessary environment variables are set."""
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable is not set")
    if not os.getenv("MODEL"):
        raise ValueError("MODEL environment variable is not set")

def main() -> None:
    try:
        setup_logging('crewai.log')
        load_dotenv()
        validate_environment()

        logging.info("Execution started")
        
        logging.info(f"GOOGLE_API_KEY: {os.getenv('GOOGLE_API_KEY')}") #Added this line
        logging.info(f"MODEL: {os.getenv('MODEL')}")#Added this line
        
        topic = os.getenv('TOPIC', 'AI LLMs')
        logging.info(f"Topic to explore: {topic}")

        mininos = Mininos(topic=topic)
        crew = mininos.crew()
        logging.info("Crew created successfully!")

        logging.info("Exploration completed! Files are saved in the output folder.")

    except Exception as e:
        logging.error("Error during topic exploration", exc_info=True)
        raise

if __name__ == "__main__":
    main()