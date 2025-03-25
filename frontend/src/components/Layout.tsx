// src/components/Layout.tsx
import React from 'react';
import Sidebar from './Sidebar';
import Header from './Header';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="flex h-screen bg-tech-gradient"> {/* Aplicamos el gradiente de fondo */}
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-x-hidden overflow-y-auto p-6"> {/* Eliminamos bg-gray-100 de main */}
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;
