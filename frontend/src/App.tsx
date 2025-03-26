// src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import NewProject from './pages/NewProject';
import GenerationProgress from './pages/GenerationProgress';
import ProjectResult from './pages/ProjectResult';
// Importa otras páginas si existen o crea placeholders
// import ProjectsList from './pages/ProjectsList';
// import Library from './pages/Library';
// import Settings from './pages/Settings';

function PlaceholderPage({ title }: { title: string }) {
  return <div className='p-6'><h1 className='text-xl'>{title} - Próximamente</h1></div>;
}


function App() {
  return (
    <Router>
      <Routes>
        {/* Rutas principales */}
        <Route path="/" element={<Dashboard />} />
        <Route path="/new-project" element={<NewProject />} />
        <Route path="/project-progress" element={<GenerationProgress />} />
        <Route path="/project-result" element={<ProjectResult />} />

        {/* Rutas adicionales del Sidebar (con placeholders) */}
        <Route path="/projects" element={<PlaceholderPage title="Mis Proyectos" />} />
        <Route path="/library" element={<PlaceholderPage title="Biblioteca de Contenido" />} />
        <Route path="/settings" element={<PlaceholderPage title="Configuración" />} />


        {/* Redirección para rutas no encontradas */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;