from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import pathlib
import os # Import os for env vars

# Importar routers
from .api import generation

# Define la ruta base del backend (donde está este main.py)
# Asumiendo que main.py está en backend/app/
APP_ROOT = pathlib.Path(__file__).parent
BACKEND_ROOT = APP_ROOT.parent # Raíz del backend (backend/)
IMAGE_OUTPUT_DIR = BACKEND_ROOT / "output" / "images"

# Crear el directorio de imágenes si no existe al iniciar la app
IMAGE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


app = FastAPI(
    title="MewAI API",
    description="API para el sistema de agentes felinos MewAI",
    version="0.2.0"
)

# Configurar CORS
# Lea el origen del frontend desde una variable de entorno o use un comodín para desarrollo
frontend_origin = os.getenv("FRONTEND_ORIGIN", "*") # Default a "*" para dev si no está seteado

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin] if frontend_origin != "*" else ["*"], # Sé específico en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Montar directorio estático para servir imágenes generadas ---
# El primer argumento es la ruta URL ("/generated_images")
# El kwarg 'directory' es la ruta del sistema de archivos (IMAGE_OUTPUT_DIR)
app.mount("/generated_images", StaticFiles(directory=IMAGE_OUTPUT_DIR), name="generated_images")
print(f"Serving static files from: {IMAGE_OUTPUT_DIR.resolve()}")
print(f"Accessible at URL path: /generated_images")


@app.get("/")
async def root():
    return {"message": "¡Bienvenido a la API de MewAI v0.2.0!"}

@app.get("/api/health")
async def health_check():
    # Podría expandirse para verificar la conexión del LLM o DB en el futuro
    return {"status": "ok", "message": "MewAI API is healthy"}

# Incluir routers de la API
app.include_router(generation.router)

# Configuración de Logging (opcional, puede mejorar la visibilidad)
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger(__name__)
logger.info("MewAI API starting up...")
logger.info(f"CORS allowed origins: {frontend_origin}")


# No necesitas el bloque if __name__ == "__main__": aquí si usas run.py
# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)