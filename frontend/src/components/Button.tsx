import React from 'react';

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
  isLoading?: boolean;
  type?: 'button' | 'submit' | 'reset';
  disabled?: boolean;
  className?: string;
}

const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  children,
  onClick,
  isLoading = false,
  type = 'button',
  disabled = false,
  className = '',
}) => {
  const baseStyles = 'font-medium rounded-lg focus:outline-none transition-colors';
  
  const variantStyles = {
    primary: 'bg-blue-pastel hover:bg-blue-pastel/80 text-gray-900 font-semibold', // Azul pastel más suave, sin sombra
    secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-700', // Grises más claros, sin sombra
    outline: 'border border-gray-300 hover:bg-gray-100 text-gray-700', // Outline más suave, sin sombra
  };

  const sizeStyles = {
    sm: 'py-1.5 px-3 text-sm',
    md: 'py-2 px-4 text-base',
    lg: 'py-2.5 px-6 text-lg',
  };

  const loadingStyles = isLoading ? 'opacity-70 cursor-not-allowed' : '';
  const disabledStyles = disabled ? 'opacity-50 cursor-not-allowed' : '';

  return (
    <button
      type={type}
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${loadingStyles} ${disabledStyles} ${className}`}
      onClick={onClick}
      disabled={isLoading || disabled}
    >
      {isLoading ? (
        <div className="flex items-center space-x-2">
          <svg className="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>Cargando...</span>
        </div>
      ) : (
        children
      )}
    </button>
  );
};

export default Button;
