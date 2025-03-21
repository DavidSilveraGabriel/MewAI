# Propuesta de Arquitectura Web para MewAI

## Componentes Frontend
- **Framework**: React.js con TypeScript
- **UI/UX**: TailwindCSS para diseño responsive + Shadcn UI para componentes
- **Estado**: Zustand (gestor de estado ligero)
- **Enrutamiento**: React Router

## Componentes Backend
- **API**: FastAPI (Python) - Interfaz REST para comunicación con el sistema de agentes
- **Autenticación**: JWT para gestión de sesiones
- **Base de datos**: MongoDB para almacenar proyectos, usuarios y contenido generado
- **Almacenamiento**: AWS S3 o similar para imágenes generadas

## Arquitectura Técnica
```
MewAI/
├── frontend/                    # Aplicación React
│   ├── src/
│   │   ├── components/          # Componentes reutilizables
│   │   ├── pages/               # Páginas principales
│   │   ├── hooks/               # Hooks personalizados
│   │   ├── context/             # Contextos React
│   │   ├── api/                 # Cliente API
│   │   ├── utils/               # Utilidades
│   │   └── App.tsx              # Componente raíz
│   └── ...
├── backend/
│   ├── app/                     # Aplicación FastAPI
│   │   ├── api/                 # Rutas de la API
│   │   ├── core/                # Configuración central
│   │   ├── db/                  # Modelos y conexión a BD
│   │   ├── services/            # Servicios de negocio
│   │   └── main.py              # Punto de entrada
│   └── ...
└── src/                         # Código original de MewAI
    ├── config/
    ├── knowledge/
    ├── tools/
    └── ...
```

## Flujo de Interacción

1. **Usuario** → interactúa con la interfaz web
2. **Frontend** → envía solicitudes a la API
3. **Backend (API)** → coordina los agentes de MewAI y gestiona la persistencia
4. **Agentes MewAI** → realizan las tareas de generación
5. **Resultados** → se devuelven al frontend para visualización 