// src/components/Header.tsx
import React from 'react';
import { Link } from 'react-router-dom'; // Import Link
import Button from './Button'; // Import Button

const Header: React.FC = () => {
  return (
    <header className="bg-xusai-gray-lightest shadow-md z-50 fixed top-0 w-full"> {/* Fixed header */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex items-center">
            <img className="h-8 w-auto" src="/logo.png" alt="MewAI Logo" />
            <h1 className="ml-2 text-xl font-semibold text-gray-800">MewAI</h1>
          </div>
          <nav className="hidden md:flex space-x-8">
            <Link to="/" className="text-xusai-gray-dark hover:text-xusai-gray-darker">
              Dashboard
            </Link>
            <a href="#" className="text-xusai-gray-dark hover:text-xusai-gray-darker">
              Marketplace
            </a>
            <a href="#" className="text-xusai-gray-dark hover:text-xusai-gray-darker">
              Learn
            </a>
            <a href="#" className="text-xusai-gray-dark hover:text-xusai-gray-darker">
              Resources
            </a>
          </nav>
          <div className="flex items-center">
            <Button variant="primary">
              Get started — it's free
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
