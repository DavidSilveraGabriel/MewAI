import uvicorn
import os
from dotenv import load_dotenv
import multiprocessing # Importar el módulo multiprocessing

# Cargar variables de entorno ANTES de cualquier otra cosa
# Es seguro hacerlo aquí, fuera del if __name__ == '__main__'
load_dotenv()
print("Environment variables loaded.")

# El punto de entrada principal del script
if __name__ == "__main__":
    # Necesario para multiprocessing en Windows, especialmente si se congela la app
    # pero también buena práctica con spawn/reloaders.
    multiprocessing.freeze_support()

    print("Starting Uvicorn server...")
    # Esta línea ahora SÓLO se ejecuta cuando ejecutas 'python run.py' directamente
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True # El reloader ahora funcionará correctamente
    )