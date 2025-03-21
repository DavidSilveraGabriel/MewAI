import os
import sys
import logging
from typing import Dict, Any, Optional

# Asegurarnos que la ruta al directorio src es correcta y absoluta
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../../"))
src_dir = os.path.join(root_dir, "src")

# Añadir src al path si existe
if os.path.exists(src_dir):
    sys.path.append(src_dir)
    print(f"Añadido {src_dir} al path de Python")
else:
    print(f"ADVERTENCIA: No se encontró el directorio {src_dir}")

try:
    # Importar el módulo Mininos de MewAI
    from src.crew import Mininos
except ImportError as e:
    print(f"Error al importar Mininos: {e}")
    # Alternativa de importación si la anterior falla
    try:
        from src.crew import Mininos
    except ImportError:
        print("No se pudo importar el módulo crew. Verifique que existe en el directorio src.")

class MewAIService:
    def __init__(self):
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
        self.logger = logging.getLogger("MewAIService")
        
    async def generate_content(self, topic: str, settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Genera contenido usando los agentes de MewAI
        
        Args:
            topic: El tema para generar contenido
            settings: Configuración adicional
            
        Returns:
            Dict con el contenido generado
        """
        self.logger.info(f"Iniciando generación de contenido para tema: {topic}")
        
        try:
            # Crear instancia de Mininos con el tema
            mininos = Mininos(topic=topic)
            
            # Crear y ejecutar el crew
            crew = mininos.crew()
            
            # Recopilar resultados
            results = {
                "status": "success",
                "blog_draft": crew.tasks[0].output if len(crew.tasks) > 0 else None,
                "blog_reviewed": crew.tasks[1].output if len(crew.tasks) > 1 else None,
                "social_media": crew.tasks[2].output if len(crew.tasks) > 2 else None,
                "images": crew.tasks[3].output if len(crew.tasks) > 3 else None
            }
            
            self.logger.info(f"Generación completada para tema: {topic}")
            return results
            
        except Exception as e:
            self.logger.error(f"Error durante la generación: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": str(e)
            }