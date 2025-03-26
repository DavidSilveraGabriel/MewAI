// src/pages/Dashboard.tsx
import React from 'react';
import { useNavigate } from 'react-router-dom'; // Importar useNavigate
import Layout from '../components/Layout';
import Button from '../components/Button';

const Dashboard: React.FC = () => {
  const navigate = useNavigate(); // Usar hook

  return (
    <Layout>
      {/* Limitar ancho del contenido del dashboard */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8"> {/* Aumentar margen inferior */}
          <h1 className="text-2xl font-semibold text-neutral-900">Panel de Control</h1>
          <p className="mt-1 text-sm text-neutral-600">
            Bienvenido a MewAI. Comienza creando un nuevo proyecto o revisa tus proyectos recientes.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Card Estilo Minimalista */}
          <div className="bg-white rounded-lg shadow-card p-6 border border-neutral-200">
            <h2 className="text-lg font-medium text-neutral-800 mb-3">Crear Nuevo Contenido</h2>
            <p className="text-sm text-neutral-600 mb-4">
              Genera contenido para tu blog y redes sociales fácilmente.
            </p>
            <Button
              variant="primary"
              onClick={() => navigate('/new-project')} // Usar navigate
            >
              Nuevo Proyecto
            </Button>
          </div>

          <div className="bg-white rounded-lg shadow-card p-6 border border-neutral-200">
            <h2 className="text-lg font-medium text-neutral-800 mb-3">Proyectos Recientes</h2>
            <div className="space-y-3">
              {/* Mejorar visualización cuando no hay proyectos */}
              <div className="text-center py-6 border border-dashed border-neutral-300 rounded-md">
                 <p className="text-sm text-neutral-500">Aún no tienes proyectos recientes.</p>
                 {/* Podrías añadir un icono aquí */}
              </div>
            </div>
          </div>
        </div>

        {/* Estadísticas - Estilo más limpio */}
        <div className="bg-white rounded-lg shadow-card p-6 border border-neutral-200">
          <h2 className="text-lg font-medium text-neutral-800 mb-4">Estadísticas de Uso</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Usar divs simples, sin borde extra si ya está en la card */}
            <div className="p-4 text-center">
              <p className="text-xs text-neutral-500 uppercase tracking-wider mb-1">Contenidos Generados</p>
              <p className="text-3xl font-semibold text-neutral-800">0</p>
            </div>
            <div className="p-4 text-center">
              <p className="text-xs text-neutral-500 uppercase tracking-wider mb-1">Imágenes Creadas</p>
              <p className="text-3xl font-semibold text-neutral-800">0</p>
            </div>
            <div className="p-4 text-center">
              <p className="text-xs text-neutral-500 uppercase tracking-wider mb-1">Proyectos Totales</p>
              <p className="text-3xl font-semibold text-neutral-800">0</p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;