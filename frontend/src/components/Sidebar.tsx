// src/components/Sidebar.tsx
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import DashboardIcon from '@mui/icons-material/DashboardOutlined'; // Usar Outlined para look más ligero
import ListAltIcon from '@mui/icons-material/ListAltOutlined';
import CollectionsBookmarkIcon from '@mui/icons-material/CollectionsBookmarkOutlined';
import SettingsIcon from '@mui/icons-material/SettingsOutlined';

const navItems = [
  { name: 'Dashboard', href: '/', icon: DashboardIcon },
  { name: 'Proyectos', href: '/projects', icon: ListAltIcon }, // Considera si esta ruta existe
  { name: 'Biblioteca', href: '/library', icon: CollectionsBookmarkIcon }, // Considera si esta ruta existe
  { name: 'Configuración', href: '/settings', icon: SettingsIcon }, // Considera si esta ruta existe
];

const Sidebar: React.FC = () => {
  const location = useLocation();

  return (
    // Sidebar fijo
    <aside className="w-64 h-screen fixed top-0 left-0 z-30 flex flex-col border-r border-neutral-200 bg-white">
       {/* Logo Area - Alineado con Header */}
       <div className="flex items-center h-16 flex-shrink-0 px-4 border-b border-neutral-200">
          <img className="h-8 w-auto" src="/logo.png" alt="MewAI Logo" />
          <span className="ml-2 text-neutral-800 text-lg font-semibold">MewAI</span>
        </div>

      {/* Navigation Area */}
      <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
        {navItems.map((item) => {
          const isActive = location.pathname === item.href || (item.href !== '/' && location.pathname.startsWith(item.href));
          return (
            <Link
              key={item.name}
              to={item.href}
              className={`
                group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors duration-150
                ${
                  isActive
                    ? 'bg-primary-light/20 text-primary-dark' // Fondo muy sutil azul, texto azul oscuro
                    : 'text-neutral-600 hover:bg-neutral-100 hover:text-neutral-900'
                }
              `}
            >
              <item.icon
                className={`
                  mr-3 flex-shrink-0 h-5 w-5 transition-colors duration-150 // Tamaño con Tailwind
                  ${
                    isActive ? 'text-primary' : 'text-neutral-400 group-hover:text-neutral-500'
                  }
                `}
                aria-hidden="true"
              />
              {item.name}
            </Link>
          );
        })}
      </nav>

      {/* Footer Area (Opcional: User info, logout) */}
      {/* <div className="flex-shrink-0 p-4 border-t border-neutral-200">
          User Info / Logout
      </div> */}
    </aside>
  );
};

export default Sidebar;