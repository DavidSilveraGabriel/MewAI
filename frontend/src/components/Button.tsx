// src/components/Button.tsx
import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost'; // Añadido 'ghost'
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  isLoading?: boolean;
  className?: string;
  // onClick, type, disabled ahora vienen de React.ButtonHTMLAttributes
}

const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  children,
  isLoading = false,
  className = '',
  disabled,
  ...props // Resto de props del botón (onClick, type, etc.)
}) => {
  const baseStyles = 'inline-flex items-center justify-center font-medium rounded-md focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-150';

  // Paleta basada en tailwind.config.js
  const variantStyles = {
    primary: 'bg-primary hover:bg-primary-dark text-white focus-visible:ring-primary',
    secondary: 'bg-neutral-200 hover:bg-neutral-300 text-neutral-700 focus-visible:ring-neutral-400',
    outline: 'border border-neutral-300 hover:bg-neutral-100 text-neutral-700 focus-visible:ring-neutral-400 bg-white',
    ghost: 'hover:bg-neutral-100 text-neutral-700 focus-visible:ring-neutral-400', // Para acciones menos prominentes
  };

  const sizeStyles = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm', // Tamaño de texto base sm para un look más fino
    lg: 'px-6 py-2.5 text-base',
  };

  // Spinner color dinámico (ajustar según contraste)
  const spinnerColor = variant === 'primary' ? 'text-white' : 'text-primary';

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
      disabled={isLoading || disabled}
      {...props}
    >
      {isLoading ? (
        <>
          <svg
            className={`animate-spin -ml-1 mr-3 h-4 w-4 ${spinnerColor}`}
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {/* Considerar no mostrar texto o uno genérico */}
          <span>Procesando...</span>
        </>
      ) : (
        children
      )}
    </button>
  );
};

export default Button;