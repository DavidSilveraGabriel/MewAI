// tailwind.config.js
const colors = require('tailwindcss/colors');

module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // Asegúrate que esto cubre todos tus archivos
  ],
  theme: {
    extend: {
      colors: {
        // Paleta Principal (Basada en el azul del logo - ajusta el HSL según tu azul exacto)
        'primary': {
          light: 'hsl(205, 90%, 75%)', // Un azul más claro para hover/fondos sutiles
          DEFAULT: 'hsl(205, 85%, 55%)', // Tu azul principal
          dark: 'hsl(205, 80%, 45%)', // Un azul más oscuro para texto o hover intenso
        },
        // Paleta Neutra Minimalista
        'neutral': {
          50: '#FAFAFA',  // Casi blanco
          100: '#F5F5F5', // Gris muy claro (anterior xusai-gray-lightest?)
          200: '#E5E5E5', // Gris claro para bordes
          300: '#D4D4D4',
          400: '#A3A3A3', // Texto secundario
          500: '#737373',
          600: '#525252',
          700: '#404040', // Texto principal
          800: '#262626',
          900: '#171717', // Casi negro
        },
        // Puedes mantener los colores por defecto si los necesitas
        // o eliminarlos para forzar el uso de tu paleta
        // gray: colors.neutral, // Ejemplo: remapear gray a tu neutral
      },
      fontFamily: {
        // Opcional: Define una fuente moderna si no usas la 'sans' por defecto
        // sans: ['Inter', 'sans-serif'], // Ejemplo con Inter
      },
      boxShadow: {
        'subtle': '0 1px 3px 0 rgb(0 0 0 / 0.05), 0 1px 2px -1px rgb(0 0 0 / 0.05)', // Sombra muy suave
        'card': '0 4px 6px -1px rgb(0 0 0 / 0.07), 0 2px 4px -2px rgb(0 0 0 / 0.07)', // Sombra para cards
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'), // Plugin para mejorar estilos de formularios
    require('@tailwindcss/typography'), // Plugin para estilizar HTML generado (prose)
  ],
};
