// src/pages/NewProject.tsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import Button from '../components/Button';
import { useGeneration } from '../hooks/useGeneration';
// Importar tipos y constantes si se crean
// import { Platform, Tone, Length, Status } from '../types/generation';

// Podrías definir constantes para evitar strings mágicos
const PLATFORMS = { instagram: 'Instagram', twitter: 'Twitter', linkedin: 'LinkedIn' };
const TONES = { formal: 'Formal', casual: 'Casual', technical: 'Técnico' };
const LENGTHS = { short: 'Corta', medium: 'Media', long: 'Larga' };

const NewProject: React.FC = () => {
  const navigate = useNavigate();
  const [topic, setTopic] = useState('');
  // Usar un estado más simple para plataformas seleccionadas
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(['instagram', 'twitter', 'linkedin']);
  const [tone, setTone] = useState('casual');
  const [length, setLength] = useState('medium');
  const [generateImages, setGenerateImages] = useState(true);
  const { startGeneration, isGenerating, error } = useGeneration(); // Capturar error del hook

  const handlePlatformChange = (platform: string) => {
    setSelectedPlatforms(prev =>
      prev.includes(platform)
        ? prev.filter(p => p !== platform)
        : [...prev, platform]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedPlatforms.length === 0) {
        // Añadir validación o feedback al usuario
        alert("Por favor, selecciona al menos una plataforma.");
        return;
    }

    try {
      const response = await startGeneration({
        topic,
        platforms: selectedPlatforms,
        tone,
        length,
        generate_images: generateImages
      });
      navigate(`/project-progress?id=${response.id}`);
    } catch (err) {
      // Mostrar error al usuario (podría ser una notificación toast)
      console.error('Error al crear el proyecto:', err);
      // Ejemplo simple: alert(error || 'Error al iniciar la generación.');
    }
  };

  return (
    <Layout>
      <div className="max-w-3xl mx-auto"> {/* Centrado */}
          <div className="bg-white rounded-lg shadow-card p-6 md:p-8 border border-neutral-200"> {/* Card con más padding */}
              <h1 className="text-2xl font-semibold text-neutral-900 mb-6">Nuevo Proyecto</h1>

              {/* Mostrar error si existe */}
              {error && (
                <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-md text-sm">
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                  <div className="space-y-6">
                  {/* Campo Tema */}
                  <div>
                      <label htmlFor="topic" className="block text-sm font-medium text-neutral-700 mb-1">
                      Tema Principal
                      </label>
                      <input
                      type="text"
                      id="topic"
                      value={topic}
                      onChange={(e) => setTopic(e.target.value)}
                      // Estilos mejorados por @tailwindcss/forms
                      className="mt-1 block w-full border-neutral-300 rounded-md shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
                      placeholder="Ej. El futuro de la IA en marketing"
                      required
                      />
                      <p className="mt-1 text-xs text-neutral-500">Describe el tema central sobre el que MewAI generará contenido.</p>
                  </div>

                  {/* Campo Plataformas */}
                  <div>
                      <span className="block text-sm font-medium text-neutral-700 mb-2">Plataformas</span>
                      <div className="grid grid-cols-2 sm:grid-cols-3 gap-x-4 gap-y-2">
                          {Object.entries(PLATFORMS).map(([key, name]) => (
                          <label key={key} className="flex items-center space-x-2 cursor-pointer">
                              <input
                                type="checkbox"
                                checked={selectedPlatforms.includes(key)}
                                onChange={() => handlePlatformChange(key)}
                                // Estilos mejorados por @tailwindcss/forms
                                className="h-4 w-4 text-primary focus:ring-primary border-neutral-300 rounded"
                              />
                              <span className="text-sm text-neutral-700">{name}</span>
                          </label>
                          ))}
                      </div>
                  </div>

                   {/* Campo Tono */}
                  <div>
                      <span className="block text-sm font-medium text-neutral-700 mb-2">Tono de Voz</span>
                       <div className="flex flex-wrap gap-x-4 gap-y-2">
                          {Object.entries(TONES).map(([key, name]) => (
                            <label key={key} className="flex items-center space-x-2 cursor-pointer">
                                <input
                                type="radio"
                                value={key}
                                checked={tone === key}
                                onChange={() => setTone(key)}
                                // Estilos mejorados por @tailwindcss/forms
                                className="h-4 w-4 text-primary focus:ring-primary border-neutral-300"
                                />
                                <span className="text-sm text-neutral-700">{name}</span>
                            </label>
                          ))}
                      </div>
                  </div>

                  {/* Campo Extensión */}
                   <div>
                      <span className="block text-sm font-medium text-neutral-700 mb-2">Extensión del Contenido</span>
                      <div className="flex flex-wrap gap-x-4 gap-y-2">
                          {Object.entries(LENGTHS).map(([key, name]) => (
                          <label key={key} className="flex items-center space-x-2 cursor-pointer">
                              <input
                                type="radio"
                                value={key}
                                checked={length === key}
                                onChange={() => setLength(key)}
                                className="h-4 w-4 text-primary focus:ring-primary border-neutral-300"
                              />
                              <span className="text-sm text-neutral-700">{name}</span>
                          </label>
                          ))}
                      </div>
                  </div>

                  {/* Campo Generar Imágenes */}
                  <div>
                      <label className="flex items-center space-x-2 cursor-pointer">
                          <input
                          type="checkbox"
                          checked={generateImages}
                          onChange={() => setGenerateImages(!generateImages)}
                          className="h-4 w-4 text-primary focus:ring-primary border-neutral-300 rounded"
                          />
                          <span className="text-sm text-neutral-700">Generar imágenes relacionadas</span>
                      </label>
                  </div>

                  {/* Botones de Acción */}
                  <div className="pt-5 border-t border-neutral-200 mt-8"> {/* Separador sutil */}
                      <div className="flex justify-end space-x-3">
                      <Button
                          type="button"
                          variant="outline"
                          onClick={() => navigate(-1)} // Usar navigate para volver atrás
                          disabled={isGenerating}
                      >
                          Cancelar
                      </Button>
                      <Button
                          type="submit"
                          variant="primary"
                          isLoading={isGenerating}
                          disabled={isGenerating || selectedPlatforms.length === 0 || !topic}
                      >
                          {isGenerating ? 'Generando...' : 'Iniciar Generación'}
                      </Button>
                      </div>
                  </div>
                  </div>
              </form>
          </div>
      </div>
    </Layout>
  );
};

export default NewProject;