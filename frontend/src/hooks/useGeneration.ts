// src/hooks/useGeneration.ts
import { useState } from 'react';
import { generationService, GenerationSettings } from '../api/generation';

export const useGeneration = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [generationId, setGenerationId] = useState<string | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);

  const startGeneration = async (settings: GenerationSettings) => {
    setIsGenerating(true);
    setError(null);
    
    try {
      const response = await generationService.startGeneration(settings);
      setGenerationId(response.id);
      setStatus(response.status);
      
      // Iniciar polling para obtener actualizaciones
      if (response.id) {
        startPolling(response.id);
      }
      
      return response;
    } catch (err) {
      setError('Error al iniciar la generación.');
      console.error(err);
      throw err;
    }
  };

  const startPolling = (id: string) => {
    const interval = setInterval(async () => {
      try {
        const statusResponse = await generationService.getGenerationStatus(id);
        setStatus(statusResponse.status);
        setProgress(statusResponse.progress || 0);
        
        if (['completed', 'error'].includes(statusResponse.status)) {
          setIsGenerating(false);
          clearInterval(interval);
        }
      } catch (err) {
        console.error('Error polling generation status', err);
        setError('Error al obtener estado de generación.');
        setIsGenerating(false);
        clearInterval(interval);
      }
    }, 2000);
    
    return () => clearInterval(interval);
  };

  return {
    isGenerating,
    error,
    generationId,
    status,
    progress,
    startGeneration
  };
};