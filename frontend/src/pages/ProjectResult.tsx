// src/pages/ProjectResult.tsx
import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import Button from '../components/Button';
import { generationService } from '../api/generation';
import CircularProgress from '@mui/material/CircularProgress'; // O un spinner simple de Tailwind/CSS
import Alert from '@mui/material/Alert'; // O un componente Alert simple

// --- Definir Interfaces ---
interface SocialMediaContent {
  instagram?: string;
  twitter?: string;
  linkedin?: string;
  // Añade otras plataformas si existen
}

interface GenerationResultData {
  blog_raw?: string; // Contenido original
  blog_reviewed?: string; // Contenido revisado/final para el blog
  social_media?: SocialMediaContent;
  images?: string[]; // URLs de las imágenes
  // Añade otros campos que tu API devuelva
  topic?: string; // Podría ser útil mostrar el tema original
}

interface GenerationStatusResponse {
  id: string;
  status: 'pending' | 'in_progress' | 'completed' | 'error';
  progress?: number;
  result?: GenerationResultData; // Usar la interfaz definida
  message?: string; // Mensaje de error
}

// Componente ContentView usando @tailwindcss/typography
const ContentView: React.FC<{ content: string | undefined; platform: string }> = ({ content }) => {
  if (!content) {
    return <p className="text-neutral-500 text-sm italic">No hay contenido disponible para esta sección.</p>;
  }
  // Asegúrate que el contenido es seguro antes de usar dangerouslySetInnerHTML
  // Aquí asumimos que viene de una fuente confiable o ya está sanitizado.
  // El plugin @tailwindcss/typography se encargará del estilo base.
  return (
    <div
      className="prose prose-sm max-w-none prose-neutral" // Clases de Tailwind Typography
      dangerouslySetInnerHTML={{ __html: content.replace(/\n/g, '<br />') }} // Mantener reemplazo de saltos de línea si es necesario
    />
  );
};

// Plataformas disponibles (podrían venir de la API o ser constantes)
const AVAILABLE_PLATFORMS = ['blog', 'instagram', 'twitter', 'linkedin', 'images'];

const ProjectResult: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const searchParams = new URLSearchParams(location.search);
  const generationId = searchParams.get('id');

  // Estado con tipos definidos
  const [activeTab, setActiveTab] = useState<string>('blog');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<GenerationResultData | null>(null);

  useEffect(() => {
    const fetchResult = async () => {
      if (!generationId) {
        navigate('/');
        return;
      }

      setLoading(true);
      setError(null);
      try {
        const response: GenerationStatusResponse = await generationService.getGenerationStatus(generationId);

        if (response.status === 'completed' && response.result) {
          setResult(response.result);
          // Determinar la primera pestaña activa basada en el contenido disponible
          const firstAvailableTab = AVAILABLE_PLATFORMS.find(platform => {
              if (platform === 'blog') return !!response.result?.blog_reviewed;
              if (platform === 'images') return !!response.result?.images?.length;
              return !!response.result?.social_media?.[platform as keyof SocialMediaContent];
          });
          setActiveTab(firstAvailableTab || 'blog');

        } else if (response.status === 'error') {
          setError(response.message || 'La generación falló o no se encontraron resultados.');
        } else if (response.status !== 'completed') {
           // Si por alguna razón llegamos aquí y no está completado, redirigir al progreso
           navigate(`/project-progress?id=${generationId}`);
           return; // Evita que setLoading sea false prematuramente
        } else {
           setError('No se encontraron datos en el resultado de la generación.');
        }
      } catch (err: any) {
        console.error('Error fetching generation result:', err);
        setError(err.message || 'Error al cargar los resultados. Inténtalo de nuevo.');
      } finally {
        setLoading(false);
      }
    };

    fetchResult();
  }, [generationId, navigate]);

  const handleExport = (format: string) => {
    // TODO: Implementar lógica de exportación real
    console.log(`Exportando en formato ${format}...`);
    // Podrías mostrar una notificación toast aquí
    alert(`Funcionalidad de exportar a ${format} no implementada aún.`);
  };

  const handleSave = () => {
    // TODO: Implementar lógica de guardado real (API call?)
    console.log('Guardando proyecto...');
    alert('Funcionalidad de guardar proyecto no implementada aún.');
  };

  // --- Renderizado Condicional ---

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center items-center h-64">
          <CircularProgress color="primary" />
          <span className="ml-4 text-neutral-600">Cargando resultados...</span>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="max-w-3xl mx-auto">
          <Alert severity="error" className="mb-6">
            {error}
          </Alert>
          <div className="flex justify-center">
            <Button variant="outline" onClick={() => navigate('/')}>
              Volver al Dashboard
            </Button>
          </div>
        </div>
      </Layout>
    );
  }

  if (!result) {
     // Caso improbable si no hay error pero tampoco resultado
      return (
          <Layout>
              <div className="max-w-3xl mx-auto">
                  <Alert severity="warning" className="mb-6">
                      No se pudieron mostrar los resultados.
                  </Alert>
                   <div className="flex justify-center">
                      <Button variant="outline" onClick={() => navigate('/')}>
                          Volver al Dashboard
                      </Button>
                  </div>
              </div>
          </Layout>
      );
  }

  // Plataformas que realmente tienen contenido
  const availableTabs = AVAILABLE_PLATFORMS.filter(platform => {
      if (platform === 'blog') return !!result.blog_reviewed;
      if (platform === 'images') return !!result.images?.length;
      return !!result.social_media?.[platform as keyof SocialMediaContent];
  });


  return (
    <Layout>
      <div className="max-w-5xl mx-auto"> {/* Ancho máximo para resultados */}
        {/* Encabezado con Acciones */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
          <div>
              <h1 className="text-2xl font-semibold text-neutral-900">Resultados del Proyecto</h1>
              {result.topic && <p className="text-sm text-neutral-500 mt-1">Tema: "{result.topic}"</p>}
          </div>
          <div className="flex space-x-3 flex-shrink-0">
            {/* Deshabilitar botones si la funcionalidad no está lista */}
            <Button variant="outline" onClick={handleSave} disabled={true}>
              Guardar Proyecto
            </Button>
            <Button variant="primary" onClick={() => handleExport('pdf')} disabled={true}>
              Exportar (PDF)
            </Button>
          </div>
        </div>

        {/* Contenedor con Pestañas */}
        <div className="bg-white rounded-lg shadow-card border border-neutral-200 overflow-hidden">
          {/* Navegación de Pestañas */}
          <div className="border-b border-neutral-200">
            <nav className="-mb-px flex space-x-6 overflow-x-auto px-4 sm:px-6" aria-label="Tabs">
              {availableTabs.map((platform) => (
                <button
                  key={platform}
                  onClick={() => setActiveTab(platform)}
                  className={`
                    whitespace-nowrap py-3 px-1 border-b-2 font-medium text-sm transition-colors duration-150
                    ${
                      activeTab === platform
                        ? 'border-primary text-primary'
                        : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300'
                    }
                  `}
                  aria-current={activeTab === platform ? 'page' : undefined}
                >
                  {/* Capitalizar nombre para mostrar */}
                  {platform.charAt(0).toUpperCase() + platform.slice(1)}
                </button>
              ))}
            </nav>
          </div>

          {/* Contenido de la Pestaña Activa */}
          <div className="p-6">
            {activeTab === 'blog' && (
              <ContentView content={result.blog_reviewed} platform="blog" />
            )}

            {activeTab === 'instagram' && (
              <ContentView content={result.social_media?.instagram} platform="instagram" />
            )}

            {activeTab === 'twitter' && (
              <ContentView content={result.social_media?.twitter} platform="twitter" />
            )}

            {activeTab === 'linkedin' && (
              <ContentView content={result.social_media?.linkedin} platform="linkedin" />
            )}

            {activeTab === 'images' && (
              <div>
                <h2 className="text-lg font-medium text-neutral-900 mb-4">Imágenes Generadas</h2>
                {result.images && result.images.length > 0 ? (
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {result.images.map((imageUrl, index) => (
                      <div key={index} className="border border-neutral-200 rounded-md overflow-hidden aspect-square bg-neutral-100">
                        <img
                            src={imageUrl} // Asegúrate que las URLs son accesibles
                            alt={`Imagen generada ${index + 1}`}
                            className="w-full h-full object-cover"
                            loading="lazy" // Carga diferida para imágenes
                        />
                      </div>
                    ))}
                  </div>
                ) : (
                   <p className="text-neutral-500 text-sm italic">No se generaron imágenes para este proyecto.</p>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default ProjectResult;