from gradio_client import Client
from typing import Optional, Tuple, Dict
from enum import Enum
import os
from crewai.tools import BaseTool
from langchain.tools import Tool

class ImageFormat(Enum):
    # Instagram formats
    INSTAGRAM_SQUARE = "instagram_square"        # 1:1
    INSTAGRAM_PORTRAIT = "instagram_portrait"    # 4:5
    INSTAGRAM_LANDSCAPE = "instagram_landscape"  # 1.91:1
    INSTAGRAM_STORY = "instagram_story"          # 9:16
    
    # Twitter/X formats
    TWITTER_POST = "twitter_post"               # 16:9
    TWITTER_CARD = "twitter_card"               # 2:1
    
    # LinkedIn formats
    LINKEDIN_POST = "linkedin_post"             # 1.91:1
    LINKEDIN_BANNER = "linkedin_banner"         # 4:1
    
    # Facebook formats
    FACEBOOK_POST = "facebook_post"             # 1.91:1
    FACEBOOK_COVER = "facebook_cover"           # 2.7:1
    
    # Generic formats
    WIDE_BANNER = "wide_banner"                 # 21:9
    HD = "hd"                                   # 16:9
    SQUARE = "square"                           # 1:1
    CUSTOM = "custom"                           # Custom size

class FluxImageGeneratorTool(BaseTool):
    name: str = "FLUX Image Generator"
    description: str = """Generates high-quality images using FLUX.1-schnell model with preset formats for social media.
    Available formats:
    - Instagram: square, portrait, landscape, story
    - Twitter: post, card
    - LinkedIn: post, banner
    - Facebook: post, cover
    - Generic: wide_banner, hd, square, custom
    
    Usage: Provide arguments as a string with format:
    "prompt: your image description, format: format_name"
    Example: "prompt: A beautiful sunset in Paris, format: instagram_square"
    """

    # Define image format presets
    FORMAT_PRESETS: Dict[ImageFormat, Dict[str, int]] = {
        ImageFormat.INSTAGRAM_SQUARE: {"width": 1080, "height": 1080},      # 1:1
        ImageFormat.INSTAGRAM_PORTRAIT: {"width": 1080, "height": 1350},    # 4:5
        ImageFormat.INSTAGRAM_LANDSCAPE: {"width": 1080, "height": 566},    # 1.91:1
        ImageFormat.INSTAGRAM_STORY: {"width": 1080, "height": 1920},       # 9:16
        
        ImageFormat.TWITTER_POST: {"width": 1200, "height": 675},          # 16:9
        ImageFormat.TWITTER_CARD: {"width": 1200, "height": 600},          # 2:1
        
        ImageFormat.LINKEDIN_POST: {"width": 1200, "height": 628},         # 1.91:1
        ImageFormat.LINKEDIN_BANNER: {"width": 1584, "height": 396},       # 4:1
        
        ImageFormat.FACEBOOK_POST: {"width": 1200, "height": 628},         # 1.91:1
        ImageFormat.FACEBOOK_COVER: {"width": 1640, "height": 624},        # 2.7:1
        
        ImageFormat.WIDE_BANNER: {"width": 2100, "height": 900},          # 21:9
        ImageFormat.HD: {"width": 1920, "height": 1080},                  # 16:9
        ImageFormat.SQUARE: {"width": 1024, "height": 1024},              # 1:1
    }

    def __init__(self, 
                 save_dir: str = "./generated_images",
                 default_format: ImageFormat = ImageFormat.SQUARE,
                 default_steps: int = 4):
        """
        Initialize the FLUX image generator tool.
        
        Args:
            save_dir (str): Directory to save generated images
            default_format (ImageFormat): Default image format to use
            default_steps (int): Default number of inference steps
        """
        super().__init__()
        self.client = Client("black-forest-labs/FLUX.1-schnell")
        self.save_dir = save_dir
        self.default_format = default_format
        self.default_steps = default_steps
        
        # Create save directory if it doesn't exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

    def _process_args(self, arguments: str) -> dict:
        """Process the arguments string into a dictionary of parameters."""
        args_dict = {}
        try:
            # Split by comma and strip whitespace
            args_pairs = [pair.strip() for pair in arguments.split(',')]
            
            for pair in args_pairs:
                if ':' in pair:
                    key, value = pair.split(':', 1)
                    key = key.strip().lower()
                    value = value.strip()
                    
                    if key == 'prompt':
                        args_dict['prompt'] = value
                    elif key == 'format':
                        try:
                            args_dict['format'] = ImageFormat(value.lower())
                        except ValueError:
                            args_dict['format'] = self.default_format
                    elif key == 'steps':
                        args_dict['num_inference_steps'] = int(value)
                    elif key == 'seed':
                        args_dict['seed'] = int(value)
                    elif key == 'randomize':
                        args_dict['randomize_seed'] = value.lower() == 'true'
                    elif key == 'width' and args_dict.get('format') == ImageFormat.CUSTOM:
                        args_dict['width'] = int(value)
                    elif key == 'height' and args_dict.get('format') == ImageFormat.CUSTOM:
                        args_dict['height'] = int(value)
                        
        except Exception as e:
            raise ValueError(f"Error processing arguments: {str(e)}")
            
        return args_dict

    def _generate_filename(self, prompt: str, image_format: ImageFormat) -> str:
        """Generate a filename based on the prompt and format"""
        clean_prompt = "".join(c if c.isalnum() else '_' for c in prompt[:30])
        return f"{clean_prompt}_{image_format.value}_{os.urandom(4).hex()}.webp"

    def _run(self, arguments: str) -> str:
        """
        Required implementation of the abstract _run method from BaseTool.
        This is the main method that will be called by the CrewAI framework.
        """
        try:
            # Process arguments
            args = self._process_args(arguments)
            
            # Get image format
            image_format = args.get('format', self.default_format)
            
            # Get dimensions based on format
            if image_format == ImageFormat.CUSTOM:
                dimensions = {
                    'width': args.get('width', 1024),
                    'height': args.get('height', 1024)
                }
            else:
                dimensions = self.FORMAT_PRESETS[image_format]
            
            # Set generation parameters
            generation_params = {
                'prompt': args.get('prompt', 'A beautiful landscape'),
                'width': dimensions['width'],
                'height': dimensions['height'],
                'num_inference_steps': args.get('num_inference_steps', self.default_steps),
                'seed': args.get('seed', 0),
                'randomize_seed': args.get('randomize_seed', True),
                'api_name': "/infer"
            }
            
            # Generate the image
            result: Tuple[str, float] = self.client.predict(**generation_params)
            
            # Get the generated image path
            temp_image_path = result[0]
            
            # Create a new filename and path in our save directory
            new_filename = self._generate_filename(generation_params['prompt'], image_format)
            new_filepath = os.path.join(self.save_dir, new_filename)
            
            # Copy the file to our save directory
            import shutil
            shutil.copy2(temp_image_path, new_filepath)
            
            return (f"Image generated successfully at: {new_filepath}\n"
                   f"Format: {image_format.value}\n"
                   f"Dimensions: {dimensions['width']}x{dimensions['height']}\n"
                   f"Seed used: {result[1]}")
            
        except Exception as e:
            return f"Error generating image: {str(e)}"
        
        
# Example usage in CrewAI:
"""
from crewai import Agent, Task, Crew
from tools.flux_image_generator import FluxImageGeneratorTool, ImageFormat

# Initialize the tool
image_generator = FluxImageGeneratorTool(
    save_dir="./my_images",
    default_format=ImageFormat.INSTAGRAM_SQUARE
)

# Create an agent that uses the tool
artist_agent = Agent(
    role='Social Media Artist',
    goal='Generate images optimized for different social media platforms',
    backstory='An AI artist specialized in creating social media content',
    tools=[image_generator]
)

# Example tasks for different platforms:
instagram_task = Task(
    description="Generate an image for Instagram",
    agent=artist_agent,
    expected_output="Path to the generated image",
    tools=[image_generator]
)

# The agent can now use the tool with arguments like:
# "prompt: A beautiful sunset in the city, format: instagram_square"
# "prompt: A scenic landscape, format: twitter_post"
# "prompt: A professional business scene, format: linkedin_banner"
"""