from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import uuid
import asyncio

from ..services.mewai_service import MewAIService

router = APIRouter(prefix="/api/generation", tags=["generation"])

# Modelo para la solicitud de generación
class GenerationRequest(BaseModel):
    topic: str
    platforms: List[str] = ["blog", "instagram", "twitter", "linkedin"]
    tone: Optional[str] = "casual"
    length: Optional[str] = "medium"
    generate_images: bool = True

# Modelo para respuesta de generación
class GenerationResponse(BaseModel):
    id: str
    status: str
    message: str = "Generación iniciada"

# Almacenamiento en memoria para las tareas en progreso
# En producción, usar una base de datos
generation_tasks = {}

@router.post("/start", response_model=GenerationResponse)
async def start_generation(request: GenerationRequest, background_tasks: BackgroundTasks):
    # Crear ID único para el trabajo
    generation_id = str(uuid.uuid4())
    
    # Guardar estado inicial
    generation_tasks[generation_id] = {
        "status": "pending",
        "progress": 0,
        "topic": request.topic,
        "settings": request.dict(),
        "result": None
    }
    
    # Añadir tarea en segundo plano
    background_tasks.add_task(
        process_generation, 
        generation_id=generation_id,
        topic=request.topic,
        settings=request.dict()
    )
    
    return GenerationResponse(
        id=generation_id,
        status="pending"
    )

@router.get("/{generation_id}")
async def get_generation_status(generation_id: str):
    if generation_id not in generation_tasks:
        raise HTTPException(status_code=404, detail="Tarea de generación no encontrada")
    
    return generation_tasks[generation_id]

async def process_generation(generation_id: str, topic: str, settings: Dict[str, Any]):
    """Procesa la generación en segundo plano"""
    try:
        # Actualizar estado
        generation_tasks[generation_id]["status"] = "in_progress"
        generation_tasks[generation_id]["progress"] = 10
        
        # Crear servicio
        service = MewAIService()
        
        # Simular progreso
        for progress in range(20, 100, 20):
            await asyncio.sleep(2)  # Simular trabajo
            generation_tasks[generation_id]["progress"] = progress
        
        # Ejecutar generación
        result = await service.generate_content(topic, settings)
        
        # Actualizar con resultado
        generation_tasks[generation_id]["status"] = "completed"
        generation_tasks[generation_id]["progress"] = 100
        generation_tasks[generation_id]["result"] = result
        
    except Exception as e:
        # Actualizar con error
        generation_tasks[generation_id]["status"] = "error"
        generation_tasks[generation_id]["error"] = str(e)