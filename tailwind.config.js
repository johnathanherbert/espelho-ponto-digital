/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js",
    "./**/*.py"  // para templates Django
  ],
  darkMode: 'class',
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
