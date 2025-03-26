from gradio_client import Client
from typing import Optional, Tuple, Dict, List
from enum import Enum
import os
import pathlib
from crewai.tools import BaseTool
# from langchain.tools import Tool # No parece usarse aquí

# Define la raíz del proyecto backend
# Asume que este archivo está en backend/src/tools/
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.parent
DEFAULT_SAVE_DIR = PROJECT_ROOT / "output" / "images" # Ruta absoluta o relativa al proyecto


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
    description: str = """Generates high-quality images using FLUX.1-schnell model with preset formats.
    Input must be a string with arguments separated by commas. Key arguments:
    - 'prompt': (Required) The description of the image.
    - 'format': (Optional) The desired format name (e.g., 'instagram_square', 'hd'). Defaults to 'square'.
    - 'steps': (Optional) Number of inference steps (e.g., 4). Defaults to 4.
    - 'seed': (Optional) Specific seed for reproducibility. Defaults to random.
    - 'randomize': (Optional) 'true' or 'false' to randomize seed. Defaults to 'true'.
    - 'width', 'height': (Optional, only for 'custom' format) Specify exact dimensions.

    Example: "prompt: A futuristic cat coding on a holographic keyboard, format: hd, steps: 8"
    Example: "prompt: Minimalist logo for an AI company, format: custom, width: 512, height: 512"

    Returns a string containing the path to the saved image file and generation details upon success, or an error message.
    """

    FORMAT_PRESETS: Dict[ImageFormat, Dict[str, int]] = {
        ImageFormat.INSTAGRAM_SQUARE: {"width": 1080, "height": 1080},
        ImageFormat.INSTAGRAM_PORTRAIT: {"width": 1080, "height": 1350},
        ImageFormat.INSTAGRAM_LANDSCAPE: {"width": 1080, "height": 566},
        ImageFormat.INSTAGRAM_STORY: {"width": 1080, "height": 1920},
        ImageFormat.TWITTER_POST: {"width": 1200, "height": 675},
        ImageFormat.TWITTER_CARD: {"width": 1200, "height": 600},
        ImageFormat.LINKEDIN_POST: {"width": 1200, "height": 628},
        ImageFormat.LINKEDIN_BANNER: {"width": 1584, "height": 396},
        ImageFormat.FACEBOOK_POST: {"width": 1200, "height": 628},
        ImageFormat.FACEBOOK_COVER: {"width": 1640, "height": 624},
        ImageFormat.WIDE_BANNER: {"width": 2100, "height": 900},
        ImageFormat.HD: {"width": 1920, "height": 1080},
        ImageFormat.SQUARE: {"width": 1024, "height": 1024},
    }

    client: Client = None # Inicializar en __init__

    def __init__(self,
                 save_dir: str = str(DEFAULT_SAVE_DIR),
                 default_format: ImageFormat = ImageFormat.SQUARE,
                 default_steps: int = 4):
        super().__init__()
        try:
            self.client = Client("black-forest-labs/FLUX.1-schnell")
        except Exception as e:
            print(f"Error initializing Gradio client: {e}. Image generation will fail.")
            # Consider raising an error or handling this more gracefully
        self.save_dir = pathlib.Path(save_dir)
        self.default_format = default_format
        self.default_steps = default_steps

        # Create save directory if it doesn't exist
        try:
            self.save_dir.mkdir(parents=True, exist_ok=True)
            print(f"Image save directory set to: {self.save_dir.resolve()}")
        except OSError as e:
            print(f"Error creating save directory {self.save_dir}: {e}")
            # Handle error appropriately, maybe fallback to a temp dir

    def _process_args(self, arguments: str) -> dict:
        args_dict = {
            'format': self.default_format,
            'num_inference_steps': self.default_steps,
            'randomize_seed': True,
            'seed': 0
        }
        try:
            args_pairs = [pair.strip() for pair in arguments.split(',')]
            current_prompt_parts = []
            in_prompt = False

            # More robust parsing to handle commas within prompts
            key = None
            value_buffer = []
            for part in arguments.split(','):
                part = part.strip()
                if ':' in part and not in_prompt: # Potential new key-value pair
                    # Process previous key-value if exists
                    if key and value_buffer:
                         value = ','.join(value_buffer).strip()
                         if key == 'prompt':
                            args_dict['prompt'] = value
                         elif key == 'format':
                             try: args_dict['format'] = ImageFormat(value.lower())
                             except ValueError: print(f"Warning: Invalid format '{value}', using default.")
                         elif key == 'steps': args_dict['num_inference_steps'] = int(value)
                         elif key == 'seed': args_dict['seed'] = int(value)
                         elif key == 'randomize': args_dict['randomize_seed'] = value.lower() == 'true'
                         elif key == 'width': args_dict['width'] = int(value)
                         elif key == 'height': args_dict['height'] = int(value)

                    # Start new key-value
                    key, first_val_part = part.split(':', 1)
                    key = key.strip().lower()
                    value_buffer = [first_val_part.strip()]
                    in_prompt = (key == 'prompt') # Check if this key is 'prompt'

                elif key: # Continuation of the previous value
                    value_buffer.append(part)
                    if in_prompt:
                        # If the part ends a quoted prompt, signal end
                        if part.endswith('"'): # Simple check, might need improvement
                             in_prompt = False

            # Process the last key-value pair
            if key and value_buffer:
                value = ','.join(value_buffer).strip()
                if key == 'prompt': args_dict['prompt'] = value
                elif key == 'format':
                     try: args_dict['format'] = ImageFormat(value.lower())
                     except ValueError: print(f"Warning: Invalid format '{value}', using default.")
                elif key == 'steps': args_dict['num_inference_steps'] = int(value)
                elif key == 'seed': args_dict['seed'] = int(value)
                elif key == 'randomize': args_dict['randomize_seed'] = value.lower() == 'true'
                elif key == 'width': args_dict['width'] = int(value)
                elif key == 'height': args_dict['height'] = int(value)

            if 'prompt' not in args_dict or not args_dict['prompt']:
                 raise ValueError("Missing required argument: 'prompt'")

        except Exception as e:
            raise ValueError(f"Error processing arguments: '{arguments}'. Error: {str(e)}")

        return args_dict

    def _generate_filename(self, prompt: str, image_format: ImageFormat) -> str:
        clean_prompt = "".join(c if c.isalnum() else '_' for c in prompt[:30]).rstrip('_')
        # Use a more unique identifier
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_hex = os.urandom(3).hex()
        return f"{clean_prompt}_{image_format.value}_{timestamp}_{random_hex}.webp"

    def _run(self, arguments: str) -> str:
        if not self.client:
            return "Error: Gradio client not initialized."
        try:
            args = self._process_args(arguments)
            image_format = args.get('format', self.default_format)

            if image_format == ImageFormat.CUSTOM:
                dimensions = {'width': args.get('width', 1024), 'height': args.get('height', 1024)}
            elif image_format in self.FORMAT_PRESETS:
                dimensions = self.FORMAT_PRESETS[image_format]
            else: # Fallback if format somehow became invalid
                dimensions = self.FORMAT_PRESETS[self.default_format]
                image_format = self.default_format

            generation_params = {
                'prompt': args.get('prompt'),
                'width': dimensions['width'],
                'height': dimensions['height'],
                'num_inference_steps': args.get('num_inference_steps'),
                'seed': args.get('seed'),
                'randomize_seed': args.get('randomize_seed'),
                'api_name': "/infer"
            }

            print(f"Generating image with params: {generation_params}")
            result: Tuple[str, float] = self.client.predict(**generation_params) # result is (filepath, seed)
            print(f"Gradio client returned: {result}")

            temp_image_path_str = result[0]
            used_seed = result[1]
            temp_image_path = pathlib.Path(temp_image_path_str)

            if not temp_image_path.exists():
                 raise FileNotFoundError(f"Generated image file not found at temporary path: {temp_image_path_str}")

            new_filename = self._generate_filename(generation_params['prompt'], image_format)
            new_filepath = self.save_dir / new_filename

            import shutil
            shutil.copy2(temp_image_path, new_filepath)
            print(f"Image copied to: {new_filepath}")

            # Return the *relative* path from the project root or a server path if serving static files
            # This makes it easier for the frontend if the backend serves the files.
            # Assuming 'output/images' is served at '/generated_images/'
            relative_path = f"/generated_images/{new_filename}" # IMPORTANT: Match this with StaticFiles mount point

            return (f"Image generated successfully. Path: {relative_path}\n"
                   f"Format: {image_format.value}\n"
                   f"Dimensions: {dimensions['width']}x{dimensions['height']}\n"
                   f"Seed used: {used_seed}")

        except Exception as e:
            import traceback
            print(f"Error generating image: {traceback.format_exc()}")
            return f"Error generating image: {str(e)}"

# Need datetime for filename generation
import datetime