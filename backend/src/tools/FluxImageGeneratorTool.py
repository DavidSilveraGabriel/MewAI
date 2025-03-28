# backend/src/tools/FluxImageGeneratorTool.py

from gradio_client import Client, utils as gradio_utils # Import utils para manejo de paths si es necesario
from typing import Optional, Tuple, Dict, List
from enum import Enum
import os
import pathlib
import datetime
import shutil
import logging # Usar logging es mejor que print para libs
import traceback # Para logs de error detallados

from crewai.tools import BaseTool
from pydantic import ConfigDict, Field # Field podría ser útil si añades más config

# Configurar un logger específico para esta herramienta
logger = logging.getLogger(__name__)

# Define la raíz del proyecto backend de forma robusta
# Asume que este archivo está en backend/src/tools/
try:
    PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
except NameError:
     # __file__ no está definido si se ejecuta interactivamente/embebido
     PROJECT_ROOT = pathlib.Path(".").resolve() # Usar directorio actual como fallback

DEFAULT_SAVE_DIR = PROJECT_ROOT / "output" / "images"

# --- Enum para Formatos de Imagen ---
class ImageFormat(Enum):
    INSTAGRAM_SQUARE = "instagram_square"        # 1:1
    INSTAGRAM_PORTRAIT = "instagram_portrait"    # 4:5
    INSTAGRAM_LANDSCAPE = "instagram_landscape"  # 1.91:1
    INSTAGRAM_STORY = "instagram_story"          # 9:16
    TWITTER_POST = "twitter_post"               # 16:9
    TWITTER_CARD = "twitter_card"               # 2:1
    LINKEDIN_POST = "linkedin_post"             # 1.91:1
    LINKEDIN_BANNER = "linkedin_banner"         # 4:1
    FACEBOOK_POST = "facebook_post"             # 1.91:1
    FACEBOOK_COVER = "facebook_cover"           # 2.7:1
    WIDE_BANNER = "wide_banner"                 # 21:9
    HD = "hd"                                   # 16:9
    SQUARE = "square"                           # 1:1
    CUSTOM = "custom"                           # Custom size

# --- Herramienta FLUX Image Generator ---
class FluxImageGeneratorTool(BaseTool):
    """
    Herramienta para generar imágenes de alta calidad utilizando el modelo FLUX.1-schnell
    a través de Gradio Client, con formatos preestablecidos para redes sociales.
    """
    # Configuración Pydantic para permitir tipos arbitrarios como gradio_client.Client
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = "FLUX Image Generator"
    description: str = """Genera imágenes de alta calidad usando FLUX.1-schnell con formatos predefinidos.
    La entrada DEBE ser una cadena de texto con argumentos separados por comas. Argumentos clave:
    - 'prompt': (Obligatorio) La descripción de la imagen.
    - 'format': (Opcional) Nombre del formato deseado (ej: 'instagram_square', 'hd'). Por defecto: 'square'.
    - 'steps': (Opcional) Número de pasos de inferencia (ej: 4). Por defecto: 4.
    - 'seed': (Opcional) Semilla específica para reproducibilidad. Por defecto: aleatoria.
    - 'randomize': (Opcional) 'true' o 'false' para aleatorizar semilla. Por defecto: 'true'.
    - 'width', 'height': (Opcional, solo para formato 'custom') Dimensiones exactas.

    Ejemplo: "prompt: Un gato futurista programando en un teclado holográfico, format: hd, steps: 8"
    Ejemplo: "prompt: Logo minimalista para una empresa IA, format: custom, width: 512, height: 512"

    Retorna una cadena con la ruta URL relativa de la imagen guardada y detalles de generación, o un mensaje de error.
    """

    # Presets de dimensiones para cada formato
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

    # Atributos con valores por defecto
    save_dir: pathlib.Path = Field(default=DEFAULT_SAVE_DIR)
    default_format: ImageFormat = Field(default=ImageFormat.SQUARE)
    default_steps: int = Field(default=4)
    # El cliente se inicializa en __init__
    client: Optional[Client] = Field(default=None, exclude=True) # Excluir de la validación/serialización Pydantic si es posible

    def __init__(self,
                 save_dir: Optional[str] = None,
                 default_format: Optional[ImageFormat] = None,
                 default_steps: Optional[int] = None,
                 **kwargs):
        """
        Inicializa la herramienta FluxImageGenerator.

        Args:
            save_dir: Directorio para guardar las imágenes generadas.
            default_format: Formato de imagen por defecto.
            default_steps: Número de pasos de inferencia por defecto.
            **kwargs: Argumentos adicionales para BaseTool.
        """
        # Usar valores pasados o los defaults de la clase
        resolved_save_dir = pathlib.Path(save_dir) if save_dir else DEFAULT_SAVE_DIR
        resolved_default_format = default_format if default_format else ImageFormat.SQUARE
        resolved_default_steps = default_steps if default_steps is not None else 4

        # Llamar a super().__init__ primero, pasando los valores resueltos si BaseTool los necesita
        # o simplemente **kwargs si BaseTool no maneja estos campos directamente.
        # Adaptar según cómo BaseTool maneje los campos definidos.
        # Asumiendo que BaseTool usa los Field defaults, solo pasamos kwargs.
        super().__init__(**kwargs)

        # Asignar los valores después de super().__init__
        self.save_dir = resolved_save_dir
        self.default_format = resolved_default_format
        self.default_steps = resolved_default_steps

        # Inicializar el cliente Gradio
        try:
            # Aquí podrías necesitar pasar credenciales (hf_token) si el Space es privado
            self.client = Client(src="black-forest-labs/FLUX.1-schnell")
            logger.info("Gradio client for FLUX.1-schnell initialized successfully.")
        except Exception as e:
            logger.error(f"Error initializing Gradio client: {e}. Image generation will fail.", exc_info=True)
            self.client = None # Asegurar que sea None si falla

        # Crear directorio de guardado
        try:
            self.save_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Image save directory ensured at: {self.save_dir.resolve()}")
        except OSError as e:
            logger.error(f"Error creating save directory {self.save_dir}: {e}")

    def _process_args(self, arguments: str) -> dict:
        """Procesa la cadena de argumentos en un diccionario de parámetros."""
        args_dict = {
            'format': self.default_format,
            'num_inference_steps': self.default_steps,
            'randomize_seed': True,
            'seed': 0,
            'width': None, # Para formato custom
            'height': None # Para formato custom
        }
        try:
            # Separar por coma, respetando posibles comas dentro de un prompt (simplificado)
            # Una solución más robusta usaría regex o parsing más avanzado si los prompts son complejos.
            args_pairs = [pair.strip() for pair in arguments.split(',')]
            key = None
            value_buffer = []

            for part in args_pairs:
                if ':' in part: # Potencialmente un nuevo par clave:valor
                    # Procesar el par anterior si existe
                    if key and value_buffer:
                        value = ','.join(value_buffer).strip()
                        if key == 'prompt': args_dict['prompt'] = value.strip('"\' ') # Limpiar comillas
                        elif key == 'format':
                            try: args_dict['format'] = ImageFormat(value.lower())
                            except ValueError: logger.warning(f"Invalid format '{value}', using default {self.default_format.value}.")
                        elif key == 'steps': args_dict['num_inference_steps'] = int(value)
                        elif key == 'seed': args_dict['seed'] = int(value)
                        elif key == 'randomize': args_dict['randomize_seed'] = value.lower() == 'true'
                        elif key == 'width': args_dict['width'] = int(value)
                        elif key == 'height': args_dict['height'] = int(value)

                    # Empezar nuevo par
                    try:
                         key_part, first_val_part = part.split(':', 1)
                         key = key_part.strip().lower()
                         value_buffer = [first_val_part.strip()]
                    except ValueError: # Si no hay ':' pero se esperaba
                         logger.warning(f"Malformed argument part, skipping: '{part}'")
                         key = None
                         value_buffer = []

                elif key: # Continuación del valor anterior (ej: parte de un prompt con comas)
                    value_buffer.append(part)

            # Procesar el último par clave:valor
            if key and value_buffer:
                value = ','.join(value_buffer).strip()
                if key == 'prompt': args_dict['prompt'] = value.strip('"\' ') # Limpiar comillas
                elif key == 'format':
                    try: args_dict['format'] = ImageFormat(value.lower())
                    except ValueError: logger.warning(f"Invalid format '{value}', using default {self.default_format.value}.")
                elif key == 'steps': args_dict['num_inference_steps'] = int(value)
                elif key == 'seed': args_dict['seed'] = int(value)
                elif key == 'randomize': args_dict['randomize_seed'] = value.lower() == 'true'
                elif key == 'width': args_dict['width'] = int(value)
                elif key == 'height': args_dict['height'] = int(value)


            if 'prompt' not in args_dict or not args_dict['prompt']:
                 raise ValueError("Missing required argument: 'prompt'")

            # Validar dimensiones para formato custom
            if args_dict['format'] == ImageFormat.CUSTOM:
                if args_dict['width'] is None or args_dict['height'] is None:
                    logger.warning("Custom format selected but width/height not specified. Using default 1024x1024.")
                    args_dict['width'] = args_dict.get('width', 1024)
                    args_dict['height'] = args_dict.get('height', 1024)

        except Exception as e:
            logger.error(f"Error processing arguments: '{arguments}'. Error: {e}", exc_info=True)
            raise ValueError(f"Error processing arguments: {str(e)}")

        return args_dict

    def _generate_filename(self, prompt: str, image_format: ImageFormat) -> str:
        """Genera un nombre de archivo único basado en el prompt y formato."""
        # Limpiar prompt para nombre de archivo
        clean_prompt = "".join(c if c.isalnum() else '_' for c in prompt[:30]).rstrip('_')
        if not clean_prompt: clean_prompt = "image" # Fallback si el prompt es muy raro
        # Añadir timestamp y random hex para unicidad
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_hex = os.urandom(3).hex()
        return f"{clean_prompt}_{image_format.value}_{timestamp}_{random_hex}.webp"

    def _run(self, arguments: str) -> str:
        """
        Ejecuta la generación de imagen.
        Este es el método principal llamado por CrewAI.
        """
        if not self.client:
            logger.error("Gradio client not initialized. Cannot generate image.")
            return "Error: El cliente Gradio no está inicializado."
        try:
            # 1. Procesar argumentos
            args = self._process_args(arguments)
            logger.info(f"Processing image generation with args: {args}")
            image_format = args.get('format') # Ya tiene default desde _process_args

            # 2. Determinar dimensiones
            if image_format == ImageFormat.CUSTOM:
                dimensions = {'width': args['width'], 'height': args['height']}
            elif image_format in self.FORMAT_PRESETS:
                dimensions = self.FORMAT_PRESETS[image_format]
            else:
                logger.warning(f"Format {image_format} not in presets, falling back to default.")
                dimensions = self.FORMAT_PRESETS[self.default_format]
                image_format = self.default_format # Corregir formato si hubo fallback

            # 3. Preparar parámetros para Gradio Client
            generation_params = {
                'prompt': args.get('prompt'),
                'width': dimensions['width'],
                'height': dimensions['height'],
                'num_inference_steps': args.get('num_inference_steps'),
                'seed': args.get('seed'),
                'randomize_seed': args.get('randomize_seed'),
                'api_name': "/infer" # Endpoint específico del Space Gradio
            }
            logger.info(f"Calling Gradio client with parameters: {generation_params}")

            # 4. Llamar al cliente Gradio
            # El resultado es una tupla: (filepath_str, seed_float)
            result: Tuple[str, float] = self.client.predict(**generation_params)
            logger.info(f"Gradio client predict returned: {result}")

            temp_image_path_str = result[0]
            used_seed = result[1]

            # Gradio puede devolver rutas temporales, necesitamos copiarlas
            # Usa gradio_utils.download_file si es una URL o maneja rutas locales
            if temp_image_path_str.startswith('http'):
                 temp_image_path = pathlib.Path(gradio_utils.download_file(temp_image_path_str))
            else:
                 temp_image_path = pathlib.Path(temp_image_path_str)


            if not temp_image_path.exists():
                 logger.error(f"Generated image file not found at temporary path: {temp_image_path_str}")
                 raise FileNotFoundError(f"Generated image file not found at path: {temp_image_path_str}")

            # 5. Generar nombre de archivo final y copiar
            new_filename = self._generate_filename(generation_params['prompt'], image_format)
            new_filepath = self.save_dir / new_filename

            shutil.copy2(temp_image_path, new_filepath)
            logger.info(f"Image successfully copied to: {new_filepath.resolve()}")

            # 6. Limpiar archivo temporal si es necesario (opcional)
            try:
                if temp_image_path.exists() and not str(new_filepath.resolve()) == str(temp_image_path.resolve()):
                    temp_image_path.unlink()
                    logger.debug(f"Temporary file removed: {temp_image_path}")
            except OSError as e:
                logger.warning(f"Could not remove temporary file {temp_image_path}: {e}")


            # 7. Devolver la RUTA URL RELATIVA para el frontend
            # Asumiendo que FastAPI sirve el directorio 'output/images' en '/generated_images/'
            relative_url_path = f"/generated_images/{new_filename}"

            success_message = (
                f"Image generated successfully.\n"
                f"URL Path: {relative_url_path}\n"
                f"Format: {image_format.value}\n"
                f"Dimensions: {dimensions['width']}x{dimensions['height']}\n"
                f"Seed used: {int(used_seed)}" # Convertir seed a int para claridad
            )
            logger.info(success_message.replace('\n', ' | ')) # Log en una línea
            return success_message

        except ValueError as ve: # Errores de procesamiento de argumentos
             logger.error(f"Argument processing error: {ve}")
             return f"Error en los argumentos: {ve}"
        except FileNotFoundError as fnfe:
            logger.error(f"File handling error: {fnfe}", exc_info=True)
            return f"Error de archivo: {fnfe}"
        except Exception as e:
            logger.error(f"Unexpected error during image generation: {e}", exc_info=True)
            # Capturar traceback para debugging
            # error_trace = traceback.format_exc()
            return f"Error inesperado al generar imagen: {str(e)}"