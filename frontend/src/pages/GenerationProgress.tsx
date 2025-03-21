// src/pages/GenerationProgress.tsx
import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import { generationService } from '../api/generation';

const GenerationProgress: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [status, setStatus] = useState('pending');
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  // Obtener el ID de la generación de la URL
  const searchParams = new URLSearchParams(location.search);
  const generationId = searchParams.get('id');

  useEffect(() => {
    if (!generationId) {
      navigate('/');
      return;
    }

    const pollInterval = setInterval(async () => {
      try {
        const response = await generationService.getGenerationStatus(generationId);
        setStatus(response.status);
        setProgress(response.progress || 0);
        
        if (['completed', 'error'].includes(response.status)) {
          clearInterval(pollInterval);
          
          if (response.status === 'completed') {
            // Redirigir a la página de resultados
            setTimeout(() => {
              navigate(`/project-result?id=${generationId}`);
            }, 1000);
          }
        }
      } catch (err) {
        console.error('Error polling generation status', err);
        setError('Error al obtener estado de generación.');
        clearInterval(pollInterval);
      }
    }, 2000);
    
    return () => clearInterval(pollInterval);
  }, [generationId, navigate]);

  return (
    <Layout>
      <div className="max-w-3xl mx-auto bg-white rounded-lg shadow p-6">
        <h1 className="text-2xl font-semibold text-gray-900 mb-6">Generando Contenido</h1>
        
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}
        
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">
              {status === 'pending' && 'Preparando...'}
              {status === 'in_progress' && 'Generando contenido...'}
              {status === 'completed' && '¡Completado!'}
              {status === 'error' && 'Error'}
            </span>
            <span className="text-sm font-medium text-gray-700">{progress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div 
              className="bg-blue-600 h-2.5 rounded-full transition-all duration-300" 
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
        
        <div className="border rounded-lg p-4">
          <h2 className="text-lg font-medium text-gray-900 mb-2">Proceso de Generación</h2>
          <ul className="space-y-3">
            <li className="flex items-center">
              <span className={`h-6 w-6 rounded-full flex items-center justify-center mr-3 ${progress >= 20 ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-400'}`}>
                {progress >= 20 ? (
                  <svg className="h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                ) : '1'}
              </span>
              <span className={progress >= 20 ? 'text-gray-900' : 'text-gray-500'}>
                Escritor de Contenido: Creación del borrador
              </span>
            </li>
            <li className="flex items-center">
              <span className={`h-6 w-6 rounded-full flex items-center justify-center mr-3 ${progress >= 40 ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-400'}`}>
                {progress >= 40 ? (
                  <svg className="h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                ) : '2'}
              </span>
              <span className={progress >= 40 ? 'text-gray-900' : 'text-gray-500'}>
                Revisor de Contenido: Revisión y edición
              </span>
            </li>
            <li className="flex items-center">
              <span className={`h-6 w-6 rounded-full flex items-center justify-center mr-3 ${progress >= 60 ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-400'}`}>
                {progress >= 60 ? (
                  <svg className="h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                ) : '3'}
              </span>
              <span className={progress >= 60 ? 'text-gray-900' : 'text-gray-500'}>
                Formateador: Adaptación para redes sociales
              </span>
            </li>
            <li className="flex items-center">
              <span className={`h-6 w-6 rounded-full flex items-center justify-center mr-3 ${progress >= 80 ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-400'}`}>
                {progress >= 80 ? (
                  <svg className="h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                ) : '4'}
              </span>
              <span className={progress >= 80 ? 'text-gray-900' : 'text-gray-500'}>
                Generador de Imágenes: Creación de imágenes
              </span>
            </li>
          </ul>
        </div>
      </div>
    </Layout>
  );
};

export default GenerationProgress;