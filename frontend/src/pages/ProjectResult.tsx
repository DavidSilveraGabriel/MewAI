// src/pages/ProjectResult.tsx
import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import Button from '../components/Button';
import { generationService } from '../api/generation';

// Componente para visualizar el contenido según la plataforma
const ContentView: React.FC<{ content: string; platform: string }> = ({ content, platform }) => {
  return (
    <div className="prose prose-sm max-w-none">
      <div dangerouslySetInnerHTML={{ __html: content.replace(/\n/g, '<br />') }} />
    </div>
  );
};

const ProjectResult: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('blog');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);

  // Obtener el ID de la generación de la URL
  const searchParams = new URLSearchParams(location.search);
  const generationId = searchParams.get('id');

  useEffect(() => {
    const fetchResult = async () => {
      if (!generationId) {
        navigate('/');
        return;
      }

      try {
        setLoading(true);
        const response = await generationService.getGenerationStatus(generationId);
        
        if (response.status === 'completed' && response.result) {
          setResult(response.result);
        } else {
          setError('No se encontraron resultados o la generación aún no ha terminado.');
        }
      } catch (err) {
        console.error('Error fetching generation result', err);
        setError('Error al obtener los resultados de la generación.');
      } finally {
        setLoading(false);
      }
    };

    fetchResult();
  }, [generationId, navigate]);

  const handleExport = (format: string) => {
    alert(`Exportando en formato ${format}...`);
    // Implementar la lógica de exportación
  };

  const handleSave = () => {
    alert('Guardando proyecto...');
    // Implementar la lógica de guardado
  };

  if (loading) {
    return (
      <Layout>
        <div className="max-w-5xl mx-auto bg-white rounded-lg shadow p-6">
          <p className="text-center py-10">Cargando resultados...</p>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="max-w-5xl mx-auto bg-white rounded-lg shadow p-6">
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
          <div className="flex justify-center">
            <Button variant="outline" onClick={() => navigate('/')}>
              Volver al Dashboard
            </Button>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-5xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-semibold text-gray-900">Resultados del Proyecto</h1>
          <div className="flex space-x-3">
            <Button variant="outline" onClick={handleSave}>
              Guardar Proyecto
            </Button>
            <Button variant="primary" onClick={() => handleExport('pdf')}>
              Exportar
            </Button>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              <button
                className={`${
                  activeTab === 'blog'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                } whitespace-nowrap py-4 px-6 border-b-2 font-medium text-sm`}
                onClick={() => setActiveTab('blog')}
              >
                Blog
              </button>
              <button
                className={`${
                  activeTab === 'instagram'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                } whitespace-nowrap py-4 px-6 border-b-2 font-medium text-sm`}
                onClick={() => setActiveTab('instagram')}
              >
                Instagram
              </button>
              <button
                className={`${
                  activeTab === 'twitter'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                } whitespace-nowrap py-4 px-6 border-b-2 font-medium text-sm`}
                onClick={() => setActiveTab('twitter')}
              >
                Twitter
              </button>
              <button
                className={`${
                  activeTab === 'linkedin'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                } whitespace-nowrap py-4 px-6 border-b-2 font-medium text-sm`}
                onClick={() => setActiveTab('linkedin')}
              >
                LinkedIn
              </button>
              <button
                className={`${
                  activeTab === 'images'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                } whitespace-nowrap py-4 px-6 border-b-2 font-medium text-sm`}
                onClick={() => setActiveTab('images')}
              >
                Imágenes
              </button>
            </nav>
          </div>
          
          <div className="p-6">
            {activeTab === 'blog' && (
              <div>
                <h2 className="text-xl font-medium text-gray-900 mb-4">Contenido del Blog</h2>
                <ContentView 
                  content={result?.blog_reviewed || "No hay contenido disponible."} 
                  platform="blog" 
                />
              </div>
            )}
            
            {activeTab === 'instagram' && (
              <div>
                <h2 className="text-xl font-medium text-gray-900 mb-4">Contenido para Instagram</h2>
                <ContentView 
                  content={result?.social_media?.instagram || "No hay contenido disponible para Instagram."} 
                  platform="instagram" 
                />
              </div>
            )}
            
            {activeTab === 'twitter' && (
              <div>
                <h2 className="text-xl font-medium text-gray-900 mb-4">Contenido para Twitter</h2>
                <ContentView 
                  content={result?.social_media?.twitter || "No hay contenido disponible para Twitter."} 
                  platform="twitter" 
                />
              </div>
            )}
            
            {activeTab === 'linkedin' && (
              <div>
                <h2 className="text-xl font-medium text-gray-900 mb-4">Contenido para LinkedIn</h2>
                <ContentView 
                  content={result?.social_media?.linkedin || "No hay contenido disponible para LinkedIn."} 
                  platform="linkedin" 
                />
              </div>
            )}
            
            {activeTab === 'images' && (
              <div>
                <h2 className="text-xl font-medium text-gray-900 mb-4">Imágenes Generadas</h2>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {result?.images && result.images.length > 0 ? (
                    result.images.map((image: string, index: number) => (
                      <div key={index} className="border rounded-lg overflow-hidden">
                        <img src={image} alt={`Imagen generada ${index + 1}`} className="w-full h-auto" />
                      </div>
                    ))
                  ) : (
                    <p className="col-span-3 text-gray-500">No hay imágenes disponibles.</p>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default ProjectResult;