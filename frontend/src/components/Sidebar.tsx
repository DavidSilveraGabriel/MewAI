// src/components/Sidebar.tsx
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import DashboardIcon from '@mui/icons-material/Dashboard';
import ListAltIcon from '@mui/icons-material/ListAlt';
import CollectionsBookmarkIcon from '@mui/icons-material/CollectionsBookmark';
import SettingsIcon from '@mui/icons-material/Settings';

const Sidebar: React.FC = () => {
  const location = useLocation();
  
  const navItems = [
    { name: 'Dashboard', href: '/', icon: DashboardIcon },
    { name: 'Proyectos', href: '/projects', icon: ListAltIcon },
    { name: 'Biblioteca', href: '/library', icon: CollectionsBookmarkIcon },
    { name: 'Configuración', href: '/settings', icon: SettingsIcon },
  ];

  return (
    <div className="flex md:flex-shrink-0">
      <div className="flex flex-col w-64">
        <div className="flex flex-col h-0 flex-1 bg-gray-100 border-r border-gray-200">
          <div className="flex items-center h-16 flex-shrink-0 px-4">
            <img className="h-8 w-auto" src="/logo.png" alt="MewAI Logo" />
            <span className="ml-2 text-gray-800 text-lg font-semibold">MewAI</span>
          </div>
          <div className="flex-1 flex flex-col overflow-y-auto">
            <nav className="flex-1 px-2 py-4 space-y-1">
              {navItems.map((item) => {
                const isActive = location.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`${
                      isActive
                        ? 'bg-blue-pastel/20 text-gray-900'
                        : 'text-gray-700 hover:bg-gray-200'
                    } group flex items-center px-2 py-2 text-sm font-medium rounded-md`}
                  >
                    <item.icon 
                      className={`${
                        isActive ? 'text-gray-900' : 'text-gray-500 group-hover:text-gray-700'
                      } mr-3`}
                      style={{ fontSize: '1.5rem' }} // Adjust icon size here
                    />
                    {item.name}
                  </Link>
                );
              })}
            </nav>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
