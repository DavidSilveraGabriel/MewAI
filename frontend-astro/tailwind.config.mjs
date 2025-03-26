import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  // darkMode: 'class', // Si quieres habilitar modo oscuro manualmente
  theme: {
    extend: {
      colors: {
        // Usa tus colores primario/neutral definidos previamente
        'primary': {
          light: 'hsl(205, 90%, 75%)',
          DEFAULT: 'hsl(205, 85%, 55%)', // Azul principal
          dark: 'hsl(205, 80%, 45%)',
          // Puedes añadir más tonos si los necesitas 50, 100... 900
        },
        'neutral': {
          50: '#FAFAFA',
          100: '#F5F5F5',
          200: '#E5E5E5',
          300: '#D4D4D4',
          400: '#A3A3A3',
          500: '#737373',
          600: '#525252',
          700: '#404040', // Texto principal
          800: '#262626',
          900: '#171717',
        },
      },
      fontFamily: {
         sans: ['Figtree', 'Inter', 'sans-serif'], // Define tus fuentes preferidas
      },
      boxShadow: {
        'subtle': '0 1px 3px 0 rgb(0 0 0 / 0.05), 0 1px 2px -1px rgb(0 0 0 / 0.05)',
        'card': '0 4px 6px -1px rgb(0 0 0 / 0.07), 0 2px 4px -2px rgb(0 0 0 / 0.07)',
      },
       // Adaptar variables de color para 'prose' si usas el plugin de tipografía
      typography: (theme) => ({
        DEFAULT: {
          css: {
            '--tw-prose-body': theme('colors.neutral[700]'),
            '--tw-prose-headings': theme('colors.neutral[900]'),
            '--tw-prose-lead': theme('colors.neutral[600]'),
            '--tw-prose-links': theme('colors.primary[DEFAULT]'),
            '--tw-prose-bold': theme('colors.neutral[900]'),
            // ... otros colores base ...
            '--tw-prose-invert-body': theme('colors.neutral[300]'),
            '--tw-prose-invert-headings': theme('colors.white'),
            // ... otros colores invertidos ...
          },
        },
      }),
    },
  },
  plugins: [
    forms,
    typography,
  ],
}