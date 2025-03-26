// src/hooks/useGeneration.ts
import { useState, useCallback } from 'react';
import { generationService, GenerationSettings, GenerationResponse } from '../api/generation'; // Asume que GenerationResponse está definida en api/generation

// Definir tipos o constantes para el estado
type GenerationHookStatus = 'idle' | 'generating' | 'polling' | 'completed' | 'error';

export const useGeneration = () => {
  const [status, setStatus] = useState<GenerationHookStatus>('idle');
  const [error, setError] = useState<string | null>(null);
  const [generationId, setGenerationId] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);

  const startPolling = useCallback((id: string) => {
    setStatus('polling');
    const interval = setInterval(async () => {
      try {
        const statusResponse = await generationService.getGenerationStatus(id); // Asume que devuelve GenerationStatusResponse
        setProgress(statusResponse.progress || 0);

        if (['completed', 'error'].includes(statusResponse.status)) {
          clearInterval(interval);
          setStatus(statusResponse.status as GenerationHookStatus); // 'completed' o 'error'
          if (statusResponse.status === 'error') {
             setError(statusResponse.message || 'Error durante la generación.');
          }
        }
        // Si sigue en 'in_progress' o 'pending', el estado 'polling' se mantiene
      } catch (err: any) {
        console.error('Error polling generation status:', err);
        setError('Error al obtener estado de generación: ' + (err.message || 'Error de red'));
        setStatus('error');
        clearInterval(interval);
      }
    }, 3000); // Poll cada 3 segundos

    // Devolver función de limpieza
    return () => clearInterval(interval);
  }, []); // useCallback sin dependencias externas

  const startGeneration = useCallback(async (settings: GenerationSettings): Promise<GenerationResponse> => {
    setStatus('generating');
    setError(null);
    setGenerationId(null);
    setProgress(0);

    try {
      const response = await generationService.startGeneration(settings);
      setGenerationId(response.id);

      if (response.id && response.status !== 'error') {
         startPolling(response.id); // Inicia el polling si la creación fue exitosa
      } else {
          // Si la API devuelve error al iniciar
          setError(response.message || 'Error al iniciar la generación.');
          setStatus('error');
      }

      return response; // Devuelve la respuesta inicial de startGeneration
    } catch (err: any) {
      console.error('Error starting generation:', err);
      const errorMessage = err.response?.data?.message || err.message || 'Error desconocido al iniciar.';
      setError(errorMessage);
      setStatus('error');
      throw new Error(errorMessage); // Relanzar para que el componente también lo maneje si es necesario
    }
  }, [startPolling]); // Depende de startPolling

  return {
    generationStatus: status, // Renombrado para claridad
    isGenerating: status === 'generating' || status === 'polling', // Estado combinado
    error,
    generationId,
    progress,
    startGeneration
  };
};