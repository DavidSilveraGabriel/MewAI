from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar routers
from .api import generation

app = FastAPI(title="MewAI API", description="API para el sistema de agentes felinos MewAI")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, limitar a tu dominio frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "¡Bienvenido a la API de MewAI!"}

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

# Incluir routers
app.include_router(generation.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)