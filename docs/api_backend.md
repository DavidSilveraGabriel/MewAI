# Propuesta de API Backend para MewAI

## Estructura de API REST

### Autenticación
```
POST /api/auth/register         # Registro de usuario
POST /api/auth/login            # Inicio de sesión
POST /api/auth/refresh          # Renovar token
GET  /api/auth/me               # Obtener datos del usuario actual
PUT  /api/auth/me               # Actualizar datos del usuario
```

### Proyectos
```
GET    /api/projects            # Listar proyectos del usuario
POST   /api/projects            # Crear nuevo proyecto
GET    /api/projects/{id}       # Obtener proyecto específico
PUT    /api/projects/{id}       # Actualizar proyecto
DELETE /api/projects/{id}       # Eliminar proyecto
```

### Generación de Contenido
```
POST   /api/generation/start    # Iniciar proceso de generación
GET    /api/generation/{id}     # Obtener estado de generación
POST   /api/generation/{id}/stop # Detener generación en curso
```

### Contenido
```
GET    /api/content             # Listar todo el contenido generado
GET    /api/content/{id}        # Obtener contenido específico
PUT    /api/content/{id}        # Actualizar contenido
DELETE /api/content/{id}        # Eliminar contenido
POST   /api/content/{id}/export # Exportar contenido (PDF, MD, etc.)
```

### Imágenes
```
GET    /api/images              # Listar imágenes generadas
POST   /api/images/generate     # Generar nueva imagen
GET    /api/images/{id}         # Obtener imagen específica
DELETE /api/images/{id}         # Eliminar imagen
```

### Configuración
```
GET    /api/config/agents       # Obtener configuración de agentes
PUT    /api/config/agents       # Actualizar configuración de agentes
GET    /api/config/presets      # Obtener preajustes guardados
POST   /api/config/presets      # Crear nuevo preajuste
DELETE /api/config/presets/{id} # Eliminar preajuste
```

## Modelos de Datos

### Usuario
```json
{
  "id": "string",
  "username": "string",
  "email": "string",
  "profile": {
    "name": "string",
    "bio": "string",
    "avatar_url": "string"
  },
  "subscription": {
    "plan": "free|basic|premium",
    "expires_at": "datetime",
    "limits": {
      "projects_per_month": "number",
      "images_per_project": "number"
    }
  },
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Proyecto
```json
{
  "id": "string",
  "user_id": "string",
  "title": "string",
  "description": "string",
  "topic": "string",
  "status": "draft|in_progress|completed",
  "settings": {
    "tone": "formal|casual|technical",
    "length": "short|medium|long",
    "platforms": ["instagram", "twitter", "linkedin"],
    "generate_images": "boolean"
  },
  "content_ids": ["string"],
  "image_ids": ["string"],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Contenido
```json
{
  "id": "string",
  "project_id": "string",
  "type": "blog|instagram|twitter|linkedin",
  "title": "string",
  "body": "string",
  "metadata": {
    "word_count": "number",
    "reading_time": "number",
    "keywords": ["string"]
  },
  "version": "number",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Imagen
```json
{
  "id": "string",
  "project_id": "string",
  "prompt": "string",
  "url": "string",
  "format": "instagram_square|twitter_post|etc",
  "dimensions": {
    "width": "number",
    "height": "number"
  },
  "created_at": "datetime"
}
```

## Integración con MewAI Core

La API se comunicará con el sistema de agentes de MewAI a través de una capa de servicios:

1. **GenerationService**: Interfaz entre API y sistema de agentes
   - Método `start_generation(topic, settings)`: Inicia el proceso con Mininos
   - Método `get_generation_status(id)`: Consulta estado actual
   - Método `stop_generation(id)`: Detiene proceso en curso

2. **ContentService**: Gestión de contenido generado
   - Método `save_content(project_id, content_data)`: Almacena resultados
   - Método `format_for_platform(content_id, platform)`: Adapta contenido

3. **ImageService**: Gestión de imágenes generadas
   - Método `generate_image(prompt, format)`: Genera imagen con FluxImageGeneratorTool
   - Método `save_image(project_id, image_data)`: Guarda en almacenamiento 