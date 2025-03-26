// src/components/Layout.tsx
import React from 'react';
import Sidebar from './Sidebar';
import Header from './Header'; // Header ahora es fijo

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen flex bg-neutral-50"> {/* Fondo base */}
      <Sidebar /> {/* Sidebar es fijo */}
      <div className="flex-1 flex flex-col pl-64"> {/* Añade padding izquierdo para compensar Sidebar */}
        <Header /> {/* Header es fijo */}
        {/* El padding top ya está en global.css para 'main' */}
        <main className="flex-1 overflow-y-auto">
            {/* Contenedor opcional para limitar ancho y centrar si es necesario */}
            {/* <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"> */}
                 {children}
            {/* </div> */}
        </main>
      </div>
    </div>
  );
};

export default Layout;