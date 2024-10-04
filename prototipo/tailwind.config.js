/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3BAFDA',  // Blu chiaro
        secondary: '#A7D129',  // Verde chiaro
        warning: '#FFCC00',  // Giallo avviso
        danger: '#FF6B6B',  // Rosso critico
        darkGray: '#4A4A4A',  // Grigio scuro per testi
      },
      fontFamily: {
        sans: ['Inter', 'Roboto', 'sans-serif'],
      },
    },
  },
  plugins: [],
}