/** @type {import('tailwindcss').Config} */
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", //  Adjust these paths to match your project structure
    "./public/index.html",        //  If you have an index.html
  ],
  theme: {
    extend: {
      colors: {
        'dark-blue-tech': '#00040f',
        'gray-100': '#f7f7f7',
        'gray-200': '#e5e5e5',
        'gray-300': '#d4d4d4',
        'gray-500': '#a3a3a3',
        'gray-700': '#525252',
        'gray-800': '#272727',
        'gray-900': '#171717',
        'blue-pastel': '#a7c957', // Un azul pastel como acento
        'xusai-blue': '#3B82F6', // Blue accent color from Xusai website
        'xusai-gray-lightest': '#F9FAFB', // Lightest gray background
        'xusai-gray-lighter': '#F3F4F6', // Lighter gray background
        'xusai-gray-light': '#E5E7EB', // Light gray border/background
        'xusai-gray-medium': '#D1D5DB', // Medium gray text
        'xusai-gray-dark': '#6B7280', // Dark gray text
        'xusai-gray-darker': '#374151', // Darker gray text
      },
      fontFamily: {
        'sans': ['"Helvetica Neue"', 'Helvetica', 'Arial', 'sans-serif'],
      },
      backgroundImage: {
        'tech-gradient': 'radial-gradient(circle, rgba(3,6,31,1) 0%, rgba(0,0,0,1) 100%)',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
