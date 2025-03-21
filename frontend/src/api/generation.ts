// src/api/generation.ts
import api from './api';

export interface GenerationSettings {
  topic: string;
  platforms: string[];
  tone: string;
  length: string;
  generate_images: boolean;
}

export interface GenerationResponse {
  id: string;
  status: string;
  message?: string;
}

export const generationService = {
  startGeneration: async (settings: GenerationSettings): Promise<GenerationResponse> => {
    const response = await api.post('/api/generation/start', settings);
    return response.data;
  },
  
  getGenerationStatus: async (id: string): Promise<any> => {
    const response = await api.get(`/api/generation/${id}`);
    return response.data;
  }
};