from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import uuid
import asyncio
from threading import Lock

# Relative import for the service
from ..services.mewai_service import MewAIService

router = APIRouter(prefix="/api/generation", tags=["generation"])

# --- Data Models ---
class GenerationRequest(BaseModel):
    topic: str
    platforms: List[str] = ["blog", "instagram", "twitter", "linkedin"]
    tone: Optional[str] = "casual"
    length: Optional[str] = "medium"
    generate_images: bool = True

class GenerationResponse(BaseModel):
    id: str
    status: str
    message: str = "Generación iniciada"

class StatusResponse(BaseModel):
    id: str
    status: str
    progress: int
    topic: str
    settings: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    message: Optional[str] = None # For progress updates

# --- In-Memory Storage (Replace with DB/Redis for Production) ---
generation_tasks: Dict[str, Dict] = {}
tasks_lock = Lock() # Lock for thread-safe access to the dictionary

# --- Callback Function ---
def update_progress_callback(generation_id: str, progress_update: Dict):
    """
    Callback function passed to the service/crew to update task status.
    This function is called from the background thread via call_soon_threadsafe.
    """
    with tasks_lock:
        if generation_id in generation_tasks:
            # Update progress and message, but don't override final status prematurely
            current_status = generation_tasks[generation_id].get("status")
            if current_status not in ["completed", "error"]:
                 # Merge update, prioritizing new progress and message
                 generation_tasks[generation_id].update(progress_update)
                 # Ensure status doesn't revert from 'in_progress' if callback is slow
                 if current_status == "pending":
                     generation_tasks[generation_id]["status"] = "in_progress"

            logger.info(f"Callback updated task {generation_id}: {progress_update}")
        else:
            logger.warning(f"Callback received for unknown generation_id: {generation_id}")

# --- Background Task Processor ---
async def process_generation(generation_id: str, topic: str, settings: Dict[str, Any]):
    """Processes the generation in the background."""
    logger.info(f"[{generation_id}] Background task started for topic: {topic}")
    global generation_tasks
    try:
        # Set initial 'in_progress' status safely
        with tasks_lock:
            if generation_id in generation_tasks:
                generation_tasks[generation_id]["status"] = "in_progress"
                generation_tasks[generation_id]["progress"] = 5 # Small initial progress
            else:
                 logger.error(f"[{generation_id}] Task details not found at start of processing.")
                 return # Exit if task vanished somehow

        # Create service instance, passing the ID and callback
        service = MewAIService(
            generation_id=generation_id,
            progress_callback=update_progress_callback # Pass the callback function
        )

        # Execute the generation (this now handles async correctly)
        result = await service.generate_content(topic, settings)

        # Update with final result or error status
        with tasks_lock:
            if generation_id in generation_tasks:
                 if result.get("status") == "success":
                     generation_tasks[generation_id].update({
                         "status": "completed",
                         "progress": 100,
                         "result": result,
                         "message": "Generación completada con éxito.",
                         "error": None
                     })
                 else: # Handle errors reported by the service/crew
                     generation_tasks[generation_id].update({
                         "status": "error",
                         # Keep last known progress or reset? Resetting might be clearer.
                         "progress": generation_tasks[generation_id].get("progress", 0),
                         "result": None,
                         "error": result.get("message", "Error desconocido durante la generación."),
                         "message": "La generación falló."
                     })
                 logger.info(f"[{generation_id}] Final status updated: {generation_tasks[generation_id]['status']}")

    except Exception as e:
        logger.error(f"[{generation_id}] Unexpected error in background task: {str(e)}", exc_info=True)
        # Update task with unexpected error status
        with tasks_lock:
            if generation_id in generation_tasks:
                 generation_tasks[generation_id].update({
                    "status": "error",
                    "progress": generation_tasks[generation_id].get("progress", 0),
                    "result": None,
                    "error": f"Error inesperado en el servidor: {str(e)}",
                    "message": "Error crítico en el proceso de generación."
                 })

# --- API Endpoints ---
@router.post("/start", response_model=GenerationResponse)
async def start_generation_endpoint(request: GenerationRequest, background_tasks: BackgroundTasks):
    """Initiates a new content generation task."""
    generation_id = str(uuid.uuid4())
    logger.info(f"Received generation request for topic: '{request.topic}'. Assigned ID: {generation_id}")

    with tasks_lock:
        generation_tasks[generation_id] = {
            "id": generation_id,
            "status": "pending",
            "progress": 0,
            "topic": request.topic,
            "settings": request.dict(),
            "result": None,
            "error": None,
            "message": "Generación en cola."
        }

    # Add the processing function to background tasks
    background_tasks.add_task(
        process_generation,
        generation_id=generation_id,
        topic=request.topic,
        settings=request.dict()
    )
    logger.info(f"[{generation_id}] Task added to background processing.")

    return GenerationResponse(
        id=generation_id,
        status="pending"
    )

@router.get("/{generation_id}", response_model=StatusResponse)
async def get_generation_status_endpoint(generation_id: str):
    """Retrieves the status and result of a generation task."""
    logger.debug(f"Status request for ID: {generation_id}")
    with tasks_lock:
        task = generation_tasks.get(generation_id)

    if task is None:
        logger.warning(f"Status request for non-existent ID: {generation_id}")
        raise HTTPException(status_code=404, detail="Tarea de generación no encontrada")

    # Return a copy to avoid potential mutation issues if needed elsewhere
    return StatusResponse(**task)

# Add logger instance for this module
import logging
logger = logging.getLogger(__name__)
# Configure logger level if needed (can be done in main.py as well)
# logger.setLevel(logging.INFO)