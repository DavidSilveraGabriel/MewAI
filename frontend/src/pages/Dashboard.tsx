// src/pages/Dashboard.tsx
import React from 'react';
import Layout from '../components/Layout';
import Button from '../components/Button';

const Dashboard: React.FC = () => {
  return (
    <Layout>
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-2xl font-semibold text-gray-900">Panel de Control</h1>
          <p className="mt-1 text-sm text-gray-600">
            Bienvenido a MewAI. Comienza creando un nuevo proyecto o revisa tus proyectos recientes.
          </p>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-gray-200 rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-800 mb-3">Crear Nuevo Contenido</h2>
            <p className="text-gray-700 mb-4">
              Genera contenido para tu blog y redes sociales fácilmente.
            </p>
            <Button 
              variant="primary" 
              onClick={() => window.location.href = '/new-project'}
            >
              Nuevo Proyecto
            </Button>
          </div>
          
          <div className="bg-gray-200 rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-800 mb-3">Proyectos Recientes</h2>
            <div className="space-y-3">
              <p className="text-gray-500 text-sm">Aún no tienes proyectos recientes.</p>
            </div>
          </div>
        </div>
        
        <div className="bg-gray-200 rounded-lg p-6 mb-6">
          <h2 className="text-lg font-medium text-gray-800 mb-3">Estadísticas de Uso</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="rounded-lg p-4 text-center">
              <p className="text-sm text-gray-500">Contenidos Generados</p>
              <p className="text-2xl font-semibold text-gray-800">0</p>
            </div>
            <div className="rounded-lg p-4 text-center">
              <p className="text-sm text-gray-500">Imágenes Creadas</p>
              <p className="text-2xl font-semibold text-gray-800">0</p>
            </div>
            <div className="rounded-lg p-4 text-center">
              <p className="text-sm text-gray-500">Proyectos Totales</p>
              <p className="text-2xl font-semibold text-gray-800">0</p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;
