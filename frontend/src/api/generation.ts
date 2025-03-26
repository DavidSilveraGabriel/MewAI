// src/api/generation.ts
import api from './api';

export interface GenerationSettings {
  topic: string;
  platforms: string[];
  tone: string;
  length: string;
  generate_images: boolean;
}

// Respuesta inicial al comenzar la generación
export interface GenerationResponse {
  id: string;
  status: string; // Podría ser 'pending', 'queued', etc.
  message?: string;
}

// --- Interfaz detallada para el estado/resultado ---
interface SocialMediaContent {
  instagram?: string;
  twitter?: string;
  linkedin?: string;
}
interface GenerationResultData {
  blog_raw?: string;
  blog_reviewed?: string;
  social_media?: SocialMediaContent;
  images?: string[];
  topic?: string;
}
export interface GenerationStatusResponse {
  id: string;
  status: 'pending' | 'in_progress' | 'completed' | 'error';
  progress?: number;
  result?: GenerationResultData;
  message?: string; // Mensaje en caso de error o informativo
}
// --- Fin Interfaces ---


export const generationService = {
  startGeneration: async (settings: GenerationSettings): Promise<GenerationResponse> => {
    const response = await api.post<GenerationResponse>('/api/generation/start', settings);
    return response.data;
  },

  // Especificar el tipo de retorno
  getGenerationStatus: async (id: string): Promise<GenerationStatusResponse> => {
    const response = await api.get<GenerationStatusResponse>(`/api/generation/${id}`);
    return response.data;
  }
};