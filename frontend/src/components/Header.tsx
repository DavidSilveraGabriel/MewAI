// src/components/Header.tsx
import React from 'react';
import { Link } from 'react-router-dom';
import Button from './Button'; // Asegúrate que la importación es correcta

const Header: React.FC = () => {
  // Decide qué botón mostrar aquí. ¿Es un login/signup o algo más?
  // Ejemplo: Si el usuario estuviera logueado, mostraría su perfil/logout.
  // Por ahora, mantendré el botón de ejemplo, pero considera su propósito.
  const isLoggedIn = false; // Simulación

  return (
    <header className="bg-white border-b border-neutral-200 z-40 fixed top-0 left-0 right-0 h-16"> {/* Fondo blanco, borde sutil */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full">
        <div className="flex justify-between items-center h-full">
          {/* Logo y Título */}
          <Link to="/" className="flex items-center gap-2 flex-shrink-0">
            <img className="h-8 w-auto" src="/logo.png" alt="MewAI Logo" /> {/* Asegúrate que logo.png existe en /public */}
            <span className="text-lg font-semibold text-neutral-800">MewAI</span>
          </Link>

          {/* Navegación Principal (Opcional - Quizás pertenece más al Sidebar en un dashboard) */}
          {/* <nav className="hidden md:flex space-x-6">
            <Link to="/" className="text-sm font-medium text-neutral-600 hover:text-primary">
              Dashboard
            </Link>
            <a href="#" className="text-sm font-medium text-neutral-600 hover:text-primary">
              Marketplace
            </a>
            <a href="#" className="text-sm font-medium text-neutral-600 hover:text-primary">
              Learn
            </a>
            <a href="#" className="text-sm font-medium text-neutral-600 hover:text-primary">
              Resources
            </a>
          </nav> */}

          {/* Acciones de Usuario / Botón Principal */}
          <div className="flex items-center">
            {isLoggedIn ? (
              <Button variant="ghost">Mi Cuenta</Button> // Ejemplo
            ) : (
              <Button variant="primary" size="md">
                Empezar Gratis
              </Button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;