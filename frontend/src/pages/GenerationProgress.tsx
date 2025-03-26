// src/pages/GenerationProgress.tsx
import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import { generationService } from '../api/generation';
import CheckCircleIcon from '@mui/icons-material/CheckCircle'; // Icono de check
import HourglassEmptyIcon from '@mui/icons-material/HourglassEmpty'; // Icono de espera
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline'; // Icono de error
import Button from '../components/Button';

// Definir tipos para el estado y pasos
type GenerationStatus = 'pending' | 'in_progress' | 'completed' | 'error';
interface GenerationStep {
  id: string;
  name: string;
  status: 'pending' | 'in_progress' | 'completed' | 'error';
}

// Mapeo de estados a texto legible
const statusMessages: Record<GenerationStatus, string> = {
  pending: 'Iniciando proceso...',
  in_progress: 'Generando contenido...',
  completed: '¡Generación completada!',
  error: 'Ocurrió un error',
};

// Pasos (ejemplo, idealmente vendrían de la API o serían más dinámicos)
const initialSteps: GenerationStep[] = [
  { id: 'write', name: 'Escritura del borrador inicial', status: 'pending' },
  { id: 'review', name: 'Revisión y mejora del contenido', status: 'pending' },
  { id: 'format', name: 'Adaptación para redes sociales', status: 'pending' },
  { id: 'image', name: 'Generación de imágenes (si aplica)', status: 'pending' },
];

const GenerationProgress: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [status, setStatus] = useState<GenerationStatus>('pending');
  const [progress, setProgress] = useState(0); // Puede ser un % real o abstracto
  const [steps, setSteps] = useState<GenerationStep[]>(initialSteps);
  const [apiError, setApiError] = useState<string | null>(null);

  const searchParams = new URLSearchParams(location.search);
  const generationId = searchParams.get('id');

  useEffect(() => {
    if (!generationId) {
      navigate('/'); // Redirige si no hay ID
      return;
    }

    let isMounted = true;
    const pollInterval = setInterval(async () => {
      if (!isMounted) return;
      try {
        // Deberías tener una interfaz para esta respuesta
        const response = await generationService.getGenerationStatus(generationId);

        if (isMounted) {
          setStatus(response.status as GenerationStatus);
          setProgress(response.progress || 0);
          setApiError(response.status === 'error' ? (response.message || 'Error desconocido') : null);

          // Actualizar estado de los pasos (lógica de ejemplo, ajustar a tu backend)
          setSteps(prevSteps => {
             // Aquí necesitarías lógica real para mapear el progreso/estado de la API a los pasos
             // Ejemplo simplificado: marcar pasos como completados basados en progreso
             const currentProgress = response.progress || 0;
             return prevSteps.map((step, index) => {
                 const threshold = (index + 1) * (100 / prevSteps.length);
                 let newStatus: GenerationStep['status'] = step.status;
                 if (response.status === 'completed') {
                     newStatus = 'completed';
                 } else if (response.status === 'error') {
                      // Marcar el paso actual o el último como error
                      newStatus = (step.status === 'in_progress' || index === prevSteps.findIndex(s => s.status === 'in_progress')) ? 'error' : step.status;
                 } else if (currentProgress >= threshold) {
                     newStatus = 'completed';
                 } else if (currentProgress >= (index * (100 / prevSteps.length)) && step.status === 'pending') {
                     newStatus = 'in_progress';
                 }
                 return { ...step, status: newStatus };
             });
          });


          if (['completed', 'error'].includes(response.status)) {
            clearInterval(pollInterval);
            if (response.status === 'completed') {
              // Esperar un poco antes de redirigir para que el usuario vea el estado final
              setTimeout(() => {
                if (isMounted) navigate(`/project-result?id=${generationId}`);
              }, 1500);
            }
          }
        }
      } catch (err) {
        console.error('Error polling generation status:', err);
        if (isMounted) {
          setApiError('No se pudo conectar con el servicio de generación.');
          setStatus('error'); // Marcar como error en el frontend también
          clearInterval(pollInterval);
        }
      }
    }, 3000); // Aumentar intervalo de polling a 3s

    return () => {
      isMounted = false;
      clearInterval(pollInterval);
    };
  }, [generationId, navigate]);

  const renderStepIcon = (stepStatus: GenerationStep['status']) => {
    switch (stepStatus) {
      case 'completed':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
      case 'in_progress':
        return <HourglassEmptyIcon className="h-5 w-5 text-blue-500 animate-spin" />;
      case 'error':
        return <ErrorOutlineIcon className="h-5 w-5 text-red-500" />;
      case 'pending':
      default:
        return <div className="h-5 w-5 flex items-center justify-center text-xs font-medium text-neutral-400 border border-neutral-300 rounded-full">{/* Placeholder o número */}</div>;
    }
  };


  return (
    <Layout>
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-lg shadow-card p-6 md:p-8 border border-neutral-200">
          <h1 className="text-2xl font-semibold text-neutral-900 mb-2">{statusMessages[status]}</h1>
          <p className="text-sm text-neutral-600 mb-6">
            {status === 'in_progress' && 'Estamos trabajando en tu contenido. Puedes seguir el progreso a continuación.'}
            {status === 'pending' && 'El proceso de generación está a punto de comenzar.'}
            {status === 'completed' && 'Tu contenido ha sido generado exitosamente. Redirigiendo a los resultados...'}
            {status === 'error' && (apiError || 'No se pudo completar la generación.')}
          </p>

          {/* Barra de Progreso */}
          {status !== 'error' && status !== 'completed' && (
            <div className="mb-8">
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium text-primary">{/* Texto dinámico? */}</span>
                <span className="text-sm font-medium text-neutral-600">{progress}%</span>
              </div>
              <div className="w-full bg-neutral-200 rounded-full h-2">
                <div
                  className="bg-primary h-2 rounded-full transition-all duration-500 ease-out"
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
            </div>
          )}

          {/* Lista de Pasos */}
          <div className="border border-neutral-200 rounded-lg p-4">
            <h2 className="text-base font-medium text-neutral-800 mb-4">Detalle del Proceso</h2>
            <ul className="space-y-4">
              {steps.map((step, index) => (
                <li key={step.id} className="flex items-start">
                  <div className="flex-shrink-0 w-6 h-6 flex items-center justify-center mr-3">
                     {renderStepIcon(step.status)}
                  </div>
                  <span className={`text-sm ${
                    step.status === 'completed' ? 'text-neutral-800' :
                    step.status === 'error' ? 'text-red-600' :
                    step.status === 'in_progress' ? 'text-blue-700 font-medium':
                    'text-neutral-500'
                  }`}>
                    {step.name}
                    {step.status === 'error' && status === 'in_progress' && <span className="text-xs block text-red-500"> (Error en este paso)</span>}
                  </span>
                </li>
              ))}
            </ul>
          </div>

          {/* Botón para volver si hay error */}
          {status === 'error' && (
              <div className="mt-6 text-center">
                  <Button variant="outline" onClick={() => navigate('/new-project')}>
                      Intentar de Nuevo
                  </Button>
              </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default GenerationProgress;