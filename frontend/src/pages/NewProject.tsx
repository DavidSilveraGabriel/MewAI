// src/pages/NewProject.tsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import Button from '../components/Button';
import { useGeneration } from '../hooks/useGeneration';


const NewProject: React.FC = () => {
  const [topic, setTopic] = useState('');
  const [platforms, setPlatforms] = useState({
    instagram: true,
    twitter: true,
    linkedin: true
  });
  const [tone, setTone] = useState('casual');
  const [length, setLength] = useState('medium');
  const [generateImages, setGenerateImages] = useState(true);
  const navigate = useNavigate();
  const { startGeneration, isGenerating } = useGeneration();
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      // Preparar los datos para la API
      const platformsList = Object.entries(platforms)
        .filter(([_, isSelected]) => isSelected)
        .map(([platform]) => platform);
      
      const response = await startGeneration({
        topic,
        platforms: platformsList,
        tone,
        length,
        generate_images: generateImages
      });
      
      // Redirigir a la página de progreso
      navigate(`/project-progress?id=${response.id}`);
    } catch (error) {
      console.error('Error al crear el proyecto:', error);
    }
  };

  return (
    <Layout>
      <div className="max-w-3xl mx-auto bg-white rounded-lg shadow p-6">
        <h1 className="text-2xl font-semibold text-gray-900 mb-6">Nuevo Proyecto</h1>
        
        <form onSubmit={handleSubmit}>
          <div className="space-y-6">
            <div>
              <label htmlFor="topic" className="block text-sm font-medium text-gray-700">
                Tema
              </label>
              <input
                type="text"
                id="topic"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="Ej. Inteligencia Artificial, Marketing Digital, etc."
                required
              />
            </div>
            
            <div>
              <span className="block text-sm font-medium text-gray-700 mb-2">Plataformas</span>
              <div className="grid grid-cols-3 gap-4">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={platforms.instagram}
                    onChange={() => setPlatforms({...platforms, instagram: !platforms.instagram})}
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-sm text-gray-700">Instagram</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={platforms.twitter}
                    onChange={() => setPlatforms({...platforms, twitter: !platforms.twitter})}
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-sm text-gray-700">Twitter</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={platforms.linkedin}
                    onChange={() => setPlatforms({...platforms, linkedin: !platforms.linkedin})}
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-sm text-gray-700">LinkedIn</span>
                </label>
              </div>
            </div>
            
            <div>
              <span className="block text-sm font-medium text-gray-700 mb-2">Tono</span>
              <div className="grid grid-cols-3 gap-4">
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="formal"
                    checked={tone === 'formal'}
                    onChange={() => setTone('formal')}
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300"
                  />
                  <span className="ml-2 text-sm text-gray-700">Formal</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="casual"
                    checked={tone === 'casual'}
                    onChange={() => setTone('casual')}
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300"
                  />
                  <span className="ml-2 text-sm text-gray-700">Casual</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="technical"
                    checked={tone === 'technical'}
                    onChange={() => setTone('technical')}
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300"
                  />
                  <span className="ml-2 text-sm text-gray-700">Técnico</span>
                </label>
              </div>
            </div>
            
            <div>
              <span className="block text-sm font-medium text-gray-700 mb-2">Extensión</span>
              <div className="grid grid-cols-3 gap-4">
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="short"
                    checked={length === 'short'}
                    onChange={() => setLength('short')}
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300"
                  />
                  <span className="ml-2 text-sm text-gray-700">Corta</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="medium"
                    checked={length === 'medium'}
                    onChange={() => setLength('medium')}
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300"
                  />
                  <span className="ml-2 text-sm text-gray-700">Media</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="long"
                    checked={length === 'long'}
                    onChange={() => setLength('long')}
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300"
                  />
                  <span className="ml-2 text-sm text-gray-700">Larga</span>
                </label>
              </div>
            </div>
            
            <div>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={generateImages}
                  onChange={() => setGenerateImages(!generateImages)}
                  className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                />
                <span className="ml-2 text-sm text-gray-700">Generar imágenes automáticamente</span>
              </label>
            </div>
            
            <div className="pt-5">
              <div className="flex justify-end">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => window.history.back()}
                  className="mr-3"
                >
                  Cancelar
                </Button>
                <Button
                  type="submit"
                  variant="primary"
                  isLoading={isGenerating}
                >
                  Iniciar Generación
                </Button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </Layout>
  );
};

export default NewProject;