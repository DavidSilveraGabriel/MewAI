// src/components/Layout.tsx
import React from 'react';
import Sidebar from './Sidebar';
import Header from './Header';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="flex h-screen"> {/* Fondo gris claro sólido */}
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-x-hidden overflow-y-auto p-6 pt-16"> {/* Added pt-16 for top padding */}
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;
