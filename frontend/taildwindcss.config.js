/** @type {import('tailwindcss').Config} */
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'dark-blue-tech': '#00040f', // Definimos un color azul oscuro tecnológico
      },
      backgroundImage: {
        'tech-gradient': 'radial-gradient(circle, rgba(3,6,31,1) 0%, rgba(0,0,0,1) 100%)', // Degradado radial azul oscuro
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
